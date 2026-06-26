#!/usr/bin/env python3
"""
jq_tool.py — JSON 路径查询与变换工具（纯标准库，类似 jq）
覆盖：路径提取/过滤/排序/格式化/多文件合并/扁平化/键提取

用法：
  python jq_tool.py get data.json "$.users[0].name"
  python jq_tool.py get data.json "$.data.*.id" --format flat
  python jq_tool.py filter data.json --where "age>30" -o filtered.json
  python jq_tool.py sort data.json --by "price" --desc
  python jq_tool.py keys data.json
  python jq_tool.py flatten data.json "$.items"
  python jq_tool.py merge a.json b.json c.json -o merged.json
  python jq_tool.py format data.json --indent 2 --sort-keys
  python jq_tool.py validate data.json
"""

import sys
import os
import json
import re
from typing import Any, Optional


# ─── CLI ──────────────────────────────────────────────────────

def parse_args(argv=None):
    argv = argv or sys.argv[1:]
    if not argv or '-h' in argv or '--help' in argv:
        print(__doc__)
        sys.exit(0)
    cmd = argv[0]
    args = {'_cmd': cmd, '_pos': []}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a.startswith('-'):
            key = a.lstrip('-').replace('-', '_')
            if i + 1 < len(argv) and not argv[i+1].startswith('-'):
                args[key] = argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            args['_pos'].append(a)
            i += 1
    return args


def color(text: str, fg: str = '') -> str:
    codes = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'cyan': 36}
    code = codes.get(fg, '')
    if not code:
        return text
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return f'\033[{code}m{text}\033[0m'
    return text


def echo(text: str, fg: str = '', bold=False):
    print(color(text, fg))


# ══════════════════════════════════════════════════════════════
#  JSONPath 引擎
# ══════════════════════════════════════════════════════════════

class JsonPath:
    """简易 JSONPath 解析器，支持常用路径语法"""

    # 路径分词正则
    _TOKEN_RE = re.compile(r'\$|\.|\*|\.\.|\[([^\]]+)\]|\[\?\((.+?)\)\]|\.(\w+)')

    def __init__(self, path_str):
        self.path_str = path_str.strip()
        self.tokens = self._tokenize()

    def _tokenize(self):
        """将路径字符串拆分为 token 列表"""
        tokens = []
        path = self.path_str

        # 处理根 $
        if path.startswith('$'):
            tokens.append(('root',))
            path = path[1:]

        while path:
            if path.startswith('..'):
                tokens.append(('recursive',))
                path = path[2:]
            elif path.startswith('['):
                # 找到匹配的 ]
                end = self._find_bracket(path)
                expr = path[1:end]
                if expr.startswith('?(') and expr.endswith(')'):
                    tokens.append(('filter', expr[2:-1]))
                else:
                    tokens.append(('index', expr))
                path = path[end + 1:]
            elif path.startswith('.'):
                if len(path) > 1 and path[1] == '.':
                    continue
                path = path[1:]
                if path and (path[0].isalpha() or path[0] == '_'):
                    m = re.match(r'^\w+', path)
                    if m:
                        tokens.append(('key', m.group()))
                        path = path[m.end():]
                elif path == '*':
                    tokens.append(('wildcard',))
                    path = path[1:]
            elif path.startswith('*'):
                tokens.append(('wildcard',))
                path = path[1:]
            elif path and (path[0].isalpha() or path[0] == '_'):
                m = re.match(r'^\w+', path)
                if m:
                    tokens.append(('key', m.group()))
                    path = m[m.end():]
            else:
                break
        return tokens

    def _find_bracket(self, s):
        """找到匹配的 ] 位置，处理嵌套"""
        depth = 0
        for i, ch in enumerate(s):
            if ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0:
                    return i
        return len(s) - 1

    def find(self, data):
        """执行路径查找，返回所有匹配结果"""
        results = []
        self._match(data, self.tokens, 0, results)
        return results

    def _match(self, data, tokens, idx, results):
        """递归匹配 token"""
        if idx >= len(tokens):
            results.append(data)
            return

        tok_type = tokens[idx][0]

        if tok_type == 'root':
            self._match(data, tokens, idx + 1, results)

        elif tok_type == 'key':
            key = tokens[idx][1]
            if isinstance(data, dict) and key in data:
                self._match(data[key], tokens, idx + 1, results)

        elif tok_type == 'wildcard':
            if isinstance(data, dict):
                for v in data.values():
                    self._match(v, tokens, idx + 1, results)
            elif isinstance(data, list):
                for item in data:
                    self._match(item, tokens, idx + 1, results)

        elif tok_type == 'index':
            expr = tokens[idx][1]
            if isinstance(data, list):
                indices = self._parse_indices(expr, len(data))
                for i in indices:
                    if 0 <= i < len(data):
                        self._match(data[i], tokens, idx + 1, results)

        elif tok_type == 'filter':
            cond = tokens[idx][1]
            if isinstance(data, list):
                for item in data:
                    if self._eval_filter(cond, item):
                        self._match(item, tokens, idx + 1, results)

        elif tok_type == 'recursive':
            # 递归下降
            self._descend(data, tokens, idx + 1, results)

    def _descend(self, data, tokens, idx, results):
        """递归遍历所有层级"""
        self._match(data, tokens, idx, results)
        if isinstance(data, dict):
            for v in data.values():
                self._descend(v, tokens, idx, results)
        elif isinstance(data, list):
            for item in data:
                self._descend(item, tokens, idx, results)

    def _parse_indices(self, expr, length):
        """解析索引表达式：数字、冒号范围、逗号分隔"""
        result = set()
        parts = expr.split(',')
        for part in parts:
            part = part.strip()
            if ':' in part:
                nums = [int(x.strip()) if x.strip() else None for x in part.split(':')]
                start = nums[0] if nums[0] is not None else 0
                end = nums[1] if nums[1] is not None else length
                step = nums[2] if len(nums) > 2 and nums[2] is not None else 1
                for i in range(start, min(end, length), step):
                    result.add(i)
            else:
                try:
                    idx = int(part)
                    if idx < 0:
                        idx += length
                    result.add(idx)
                except ValueError:
                    pass
        return sorted(result)

    def _eval_filter(self, cond, item):
        """简单过滤表达式评估（支持 @.key op value 格式）"""
        # 支持: @.age > 30, @.name == "Alice", @.active == true
        m = re.match(r"@\.(\w+)\s*(>=|<=|!=|>|<|==)\s*(.+)", cond.strip())
        if m and isinstance(item, dict):
            key, op, val_str = m.groups()
            if key not in item:
                return False
            left = item[key]
            right = self._parse_value(val_str.strip())
            try:
                if op == '>': return left > right
                elif op == '<': return left < right
                elif op == '>=': return left >= right
                elif op == '<=': return left <= right
                elif op == '==': return left == right
                elif op != '': return left != right
            except TypeError:
                return False
        return True

    def _parse_value(self, s):
        """解析值字符串为 Python 对象"""
        s = s.strip().strip('"').strip("'")
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        elif s.lower() == 'null' or s == '':
            return None
        try:
            if '.' in s:
                return float(s)
            return int(s)
        except ValueError:
            return s


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

def _load_json(path_or_stdin='-') -> Any:
    """加载 JSON 文件或从 stdin 读取"""
    if path_or_stdin == '-':
        return json.load(sys.stdin)
    with open(path_or_stdin, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_json(data, output_path, indent=2, sort_keys=False, compact=False):
    """保存 JSON 到文件或 stdout"""
    if compact:
        text = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    else:
        text = json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=sort_keys)

    if output_path:
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
            f.write('\n')
    else:
        print(text)


def _get_input_file(args):
    """获取输入文件路径"""
    pos = args.get('_pos', [])
    if not pos or pos[0] == '-':
        echo('❌ 缺少 JSON 文件路径', 'red')
        sys.exit(1)
    filepath = pos[0]
    if not os.path.exists(filepath):
        echo(f'❌ 文件不存在: {filepath}', 'red')
        sys.exit(1)
    return filepath


# ─── get: JSONPath 查询 ─────────────────────────────────────

def cmd_get(args):
    """使用 JSONPath 提取数据"""
    filepath = _get_input_file(args)
    pos = args.get('_pos', [])

    if len(pos) < 2:
        echo('❌ 缺少 JSONPath 表达式', 'red')
        sys.exit(1)

    path_expr = pos[1]
    fmt = args.get('format', '')
    raw_mode = args.get('raw')
    indent = int(args.get('indent', 2))

    try:
        data = _load_json(filepath)
        jp = JsonPath(path_expr)
        results = jp.find(data)

        if not results:
            if raw_mode:
                sys.exit(1)
            echo('(空结果)', 'yellow')
            return

        # 单个结果直接输出，多个结果包装成数组
        if len(results) == 1:
            output = results[0]
        else:
            output = results

        if fmt == 'flat':
            # 扁平输出每行一个值
            items = results if len(results) > 1 else [results[0]]
            for item in items:
                if isinstance(item, (dict, list)):
                    print(json.dumps(item, ensure_ascii=False))
                else:
                    print(item)
        elif raw_mode:
            # 原始输出（适合管道）
            print(json.dumps(output, ensure_ascii=False, separators=(',', ':')))
        else:
            _save_json(output, args.get('o'), indent=indent,
                       sort_keys=args.get('sort_keys'))

    except Exception as e:
        echo(f'❌ 查询失败: {e}', 'red')
        sys.exit(1)


# ─── filter: 过滤数组元素 ──────────────────────────────────

def cmd_filter(args):
    """按条件过滤 JSON 数组中的元素"""
    filepath = _get_input_file(args)
    where_clause = args.get('where')
    negate = args.get('invert')
    limit_val = args.get('limit')

    if not where_clause:
        echo('❌ 请指定过滤条件: --where "field op value"', 'red')
        sys.exit(1)

    try:
        data = _load_json(filepath)

        # 支持对顶层对象内的数组进行过滤，也支持顶层是数组
        target = data
        if isinstance(target, dict):
            # 尝试找到第一个数组字段
            for k, v in target.items():
                if isinstance(v, list):
                    target = v
                    break

        if not isinstance(target, list):
            echo('❌ 数据不是数组类型，无法过滤', 'red')
            sys.exit(1)

        jp = JsonPath(f"$[?({where_clause})]")
        results = jp.find({'$': target})

        if negate:
            original_set = id_set(target)
            filtered_set = id_set(results)
            results = [item for item in target if id(item) not in filtered_set]

        if limit_val:
            results = results[:int(limit_val)]

        _save_json(results, args.get('o'), indent=int(args.get('indent', 2)))
        echo(f'✅ 过滤完成: {len(results)} / {len(target)} 条', 'green')

    except Exception as e:
        echo(f'❌ 过滤失败: {e}', 'red')
        sys.exit(1)


# ─── sort: 排序 ────────────────────────────────────────────

def cmd_sort(args):
    """对 JSON 数组排序"""
    filepath = _get_input_file(args)
    by_field = args.get('by')
    desc = args.get('desc')

    if not by_field:
        echo('❌ 请指定排序字段: --by field_name', 'red')
        sys.exit(1)

    try:
        data = _load_json(filepath)

        target = data
        if isinstance(target, dict):
            for k, v in target.items():
                if isinstance(v, list):
                    target = v
                    break

        if not isinstance(target, list):
            echo('❌ 数据不是数组类型', 'red')
            sys.exit(1)

        reverse = bool(desc)
        sorted_data = sorted(
            target,
            key=lambda x: (_get_nested(x, by_field),),
            reverse=reverse
        )

        _save_json(sorted_data, args.get('o'), indent=int(args.get('indent', 2)))
        echo(f'✅ 排序完成: 按 {by_field} ({("降序" if desc else "升序")})', 'green')

    except Exception as e:
        echo(f'❌ 排序失败: {e}', 'red')
        sys.exit(1)


# ─── keys: 提取键名 ────────────────────────────────────────

def cmd_keys(args):
    """提取 JSON 对象的所有键路径"""
    filepath = _get_input_file(args)
    prefix = args.get('prefix', '$')
    depth = int(args.get('depth', '99'))
    leaf_only = args.get('leaves')

    try:
        data = _load_json(filepath)
        keys_list = []

        def walk(obj, path=''):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_path = f'{path}.{k}' if path else k
                    current_depth = new_path.count('.')
                    if not leaf_only or not isinstance(v, (dict, list)):
                        keys_list.append(new_path)
                    if current_depth < depth:
                        walk(v, new_path)
            elif isinstance(obj, list) and obj:
                for idx, v in enumerate(obj):
                    new_path = f'{path}[{idx}]'
                    current_depth = new_path.count('.') + new_path.count('[')
                    if not leaf_only or not isinstance(v, (dict, list)):
                        keys_list.append(new_path)
                    if current_depth < depth:
                        walk(v, new_path)

        walk(data)
        _save_json(keys_list, args.get('o'))

    except Exception as e:
        echo(f'❌ 提取键失败: {e}', 'red')


# ─── flatten: 扁平化嵌套结构 ───────────────────────────────

def cmd_flatten(args):
    """将嵌套 JSON 扁平化为单层"""
    filepath = _get_input_file(args)
    pos = args.get('_pos', [])
    path_expr = pos[1] if len(pos) > 1 else None
    separator = args.get('sep', '.')
    max_depth = int(args.get('max_depth', '10'))

    try:
        data = _load_json(filepath)

        if path_expr:
            jp = JsonPath(path_expr)
            found = jp.find(data)
            if found:
                data = found[0] if len(found) == 1 else found

        flattened = {}

        def flatten_obj(obj, parent_key=''):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_key = f'{parent_key}{separator}{k}' if parent_key else k
                    if isinstance(v, (dict, list)) and parent_key.count(separator) < max_depth:
                        flatten_obj(v, new_key)
                    else:
                        flattened[new_key] = v
            elif isinstance(obj, list):
                for idx, v in enumerate(obj):
                    new_key = f'{parent_key}[{idx}]'
                    if isinstance(v, (dict, list)) and parent_key.count(separator) < max_depth:
                        flatten_obj(v, new_key)
                    else:
                        flattened[new_key] = v

        flatten_obj(data)
        _save_json(flattened, args.get('o'), indent=int(args.get('indent', 2)))
        echo(f'✅ 扁平化完成: {len(flattened)} 个键', 'green')

    except Exception as e:
        echo(f'❌ 扁平化失败: {e}', 'red')


# ─── merge: 合并多个 JSON ─────────────────────────────────

def cmd_merge(args):
    """深度合并多个 JSON 文件"""
    pos = args.get('_pos', [])
    files = [f for f in pos if os.path.exists(f)]

    if not files:
        echo('❌ 未提供有效的 JSON 文件', 'red')
        sys.exit(1)

    strategy = args.get('strategy', 'deep')   # deep / shallow / append_arrays

    try:
        result = {}
        for fp in files:
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if strategy == 'deep':
                result = _deep_merge(result, data)
            elif strategy == 'shallow':
                result.update(data)
            elif strategy == 'append_arrays':
                result = _merge_append(result, data)

        _save_json(result, args.get('o'), indent=int(args.get('indent', 2)),
                   sort_keys=args.get('sort_keys'))
        echo(f'✅ 合并完成: {len(files)} 个文件 → {args.get("o") or "stdout"}', 'green')

    except Exception as e:
        echo(f'❌ 合并失败: {e}', 'red')


# ─── format: 格式化/美化 JSON ─────────────────────────────

def cmd_format(args):
    """格式化 JSON（美化、压缩、排序键）"""
    filepath = _get_input_file(args)

    try:
        data = _load_json(filepath)

        compact = args.get('compress') or args.get('compact')
        sort_keys = args.get('sort_keys')
        indent = int(args.get('indent', '4') if not compact else '0')

        _save_json(data, args.get('o'),
                   indent=0 if compact else indent,
                   sort_keys=bool(sort_keys),
                   compact=bool(compact))

    except Exception as e:
        echo(f'❌ 格式化失败: {e}', 'red')


# ─── validate: 验证 JSON ───────────────────────────────────

def cmd_validate(args):
    """验证 JSON 文件是否合法"""
    filepath = _get_input_file(args)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        data = json.loads(content)

        # 统计信息
        size = len(content.encode('utf-8'))
        type_name = type(data).__name__
        count = _count_nodes(data)

        echo(f'✅ JSON 合法', 'green')
        echo(f'   类型: {type_name}', 'cyan')
        echo(f'   大小: {_format_size(size)}', 'cyan')
        echo(f'   节点数: {count}', 'cyan')

        # 检查常见问题
        issues = []
        if '\\/' in content:
            issues.append('包含不必要的转义斜杠 \\/')
        if '\\n' in content and '"\\n"' in content:
            issues.append('可能混用了转义换行和字面换行')

        if issues:
            echo('   ⚠️  建议:', 'yellow')
            for issue in issues:
                echo(f'      - {issue}', 'yellow')

    except json.JSONDecodeError as e:
        echo(f'❌ JSON 不合法', 'red')
        echo(f'   行 {e.lineno}, 列 {e.colno}: {e.msg}', 'red')
        sys.exit(1)


# ─── 辅助函数 ──────────────────────────────────────────────

def _deep_merge(base, override):
    """深度合并两个字典"""
    result = base.copy()
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def _merge_append(base, override):
    """合并时追加数组"""
    result = base.copy()
    for k, v in override.items():
        if k in result and isinstance(result[k], list) and isinstance(v, list):
            result[k] = result[k] + v
        elif k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _merge_append(result[k], v)
        else:
            result[k] = v
    return result


def _get_nested(obj, path):
    """获取嵌套对象的值（支持点号路径）"""
    keys = path.split('.')
    current = obj
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return ''
    return current


def id_set(items):  # noqa: E743
    """基于 id 的集合"""
    return {id(x) for x in items}


def _count_nodes(obj):
    """递归统计节点数"""
    if isinstance(obj, dict):
        return sum(_count_nodes(v) for v in obj.values()) + len(obj)
    elif isinstance(obj, list):
        return sum(_count_nodes(i) for i in obj)
    return 1


def _format_size(size_bytes):
    """格式化大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(size_bytes) < 1024.0:
            return f'{size_bytes:.1f} {unit}'
        size_bytes /= 1024.0
    return f'{size_bytes:.1f} TB'


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'get': cmd_get,
    'filter': cmd_filter,
    'sort': cmd_sort,
    'keys': cmd_keys,
    'flatten': cmd_flatten,
    'merge': cmd_merge,
    'format': cmd_format,
    'validate': cmd_validate,
}

ALIASES = {
    'query': 'get', 'q': 'get', 'select': 'get',
    'grep': 'filter', 'where': 'filter',
    'order': 'sort', 'orderby': 'sort',
    'list-keys': 'keys', 'paths': 'keys', 'schema': 'keys',
    'flat': 'flatten', 'unroll': 'flatten',
    'join': 'merge', 'combine': 'merge', 'cat': 'merge',
    'pretty': 'format', 'beautify': 'format',
    'minify': 'format', 'compact': 'format',
    'check': 'validate', 'verify': 'validate', 'lint': 'validate',
}


def main():
    args = parse_args()
    cmd = args['_cmd']
    cmd = ALIASES.get(cmd, cmd)

    if cmd not in COMMANDS:
        available = ', '.join(sorted(set(list(COMMANDS.keys()) + list(ALIASES.keys()))))
        echo(f'❌ 未知命令: {cmd}', 'red')
        echo(f'可用命令: {available}', 'cyan')
        sys.exit(1)

    COMMANDS[cmd](args)


if __name__ == '__main__':
    main()
