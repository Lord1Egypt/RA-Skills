#!/usr/bin/env python3
"""
format_converter.py — 通用格式转换工具（纯标准库）
覆盖：JSON/YAML/TOML/INI/CSV/ENV/日期 等格式互转
（Base64/URL/Unicode 编解码 → crypto_utils.py；Markdown→HTML → text_utils.py）

用法：
  python format_converter.py json2yaml input.json -o output.yaml
  python format_converter.py yaml2json input.yaml
  python format_converter.py csv2json data.csv --encoding utf-8-sig
  python format_converter.py ini2json config.ini
  python format_converter.py date-format "2024-01-15" --from-fmt "%Y-%m-%d" --to-fmt "%Y年%m月%d日"
  python format_converter.py json2env config.json -o .env
  python format_converter.py generate-env .env.example -o .env
"""

import sys
import os
import json
import csv
import re
import configparser
import io
import hashlib
import datetime
from typing import Any, Optional, Union

# ─── CLI 参数解析 ─────────────────────────────────────────────

def parse_args(argv=None):
    """简易参数解析"""
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
    """终端彩色输出（兼容 Windows）"""
    codes = {
        'red': 31, 'green': 32, 'yellow': 33,
        'blue': 34, 'cyan': 36, 'white': 37,
    }
    code = codes.get(fg, '')
    if not code:
        return text
    # 检测是否在支持颜色的终端
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return f'\033[{code}m{text}\033[0m'
    return text


def echo(text: str, fg: str = '', bold: bool = False):
    out = color(text, fg)
    if bold:
        out = color(out, '')  # 保持原样，Windows 下不额外处理
    print(out)


# ─── YAML 解析器（纯标准库实现） ──────────────────────────────

class SimpleYAMLParser:
    """轻量 YAML 解析器，覆盖常用场景"""

    @staticmethod
    def loads(s: str) -> Any:
        lines = s.split('\n')
        return SimpleYAMLParser._parse_block(lines, 0, 0)[0]

    @staticmethod
    def _parse_block(lines: list, start: int, base_indent: int) -> tuple:
        result = None
        if isinstance(result, dict):
            result = {}
        elif isinstance(result, list):
            result = []
        else:
            result = {}

        i = start
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # 跳过空行和注释
            if not stripped or stripped.startswith('#'):
                i += 1
                continue

            # 计算缩进
            indent = len(line) - len(line.lstrip())

            # 缩进减少则结束当前块
            if indent < base_indent:
                break

            # 处理列表项
            if stripped.startswith('- ') and isinstance(result, dict):
                result = []
                # 重新解析当前行作为列表首项
                continue

            if stripped.startswith('- '):
                val_str = stripped[2:].strip()
                value = SimpleYAMLParser._parse_value(val_str)
                if isinstance(value, dict) and ':' in val_str and not val_str.startswith('{'):
                    # 内联字典
                    pass
                if not isinstance(result, list):
                    result = []
                result.append(value)
                i += 1
                continue

            # 处理键值对
            if ':' in stripped:
                colon_idx = stripped.index(':')
                key = stripped[:colon_idx].strip()
                val_part = stripped[colon_idx + 1:].strip()

                if not val_part or val_part.startswith('#'):
                    # 值在下一行或嵌套块
                    sub_result, i = SimpleYAMLParser._parse_block(lines, i + 1, indent + 2)
                    if isinstance(result, dict):
                        result[key] = sub_result if sub_result is not None else {}
                    else:
                        result.append({key: sub_result})
                    continue
                else:
                    value = SimpleYAMLParser._parse_value(val_part)
                    if isinstance(result, dict):
                        result[key] = value
                    else:
                        result.append({key: value})
            i += 1

        return result, i

    @staticmethod
    def _parse_value(s: str) -> Any:
        s = s.strip()
        if not s:
            return None
        # 去除行内注释
        if ' #' in s:
            s = s[:s.index(' #')].strip()
        # 字符串引号
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            return s[1:-1]
        # 布尔
        if s.lower() in ('true', 'yes', 'on'):
            return True
        if s.lower() in ('false', 'no', 'off'):
            return False
        # null
        if s.lower() in ('null', '~', ''):
            return None
        # 数字
        try:
            if '.' in s:
                return float(s)
            return int(s)
        except ValueError:
            pass
        return s

    @staticmethod
    def dumps(data: Any, indent: int = 0) -> str:
        lines = []
        prefix = ' ' * indent
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (dict, list)) and v:
                    lines.append(f'{prefix}{k}:')
                    lines.append(SimpleYAML.dumps(v, indent + 2))
                elif v is None:
                    lines.append(f'{prefix}{k}: null')
                elif isinstance(v, bool):
                    lines.append(f'{prefix}{k}: {"true" if v else "false"}')
                elif isinstance(v, str):
                    if '\n' in v or ':' in v or "'" in v:
                        lines.append(f"{prefix}{k}: '{v}'")
                    else:
                        lines.append(f'{prefix}{k}: {v}')
                else:
                    lines.append(f'{prefix}{k}: {v}')
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    lines.append(f'{prefix}-')
                    for k, v in item.items():
                        lines.append(f'{prefix}  {k}: {SimpleYAML._scalar_str(v)}')
                elif isinstance(item, (list,)):
                    lines.append(f'{prefix}-')
                    lines.append(SimpleYAML.dumps(item, indent + 2).rstrip())
                else:
                    lines.append(f'{prefix}- {SimpleYAML._scalar_str(item)}')
        else:
            return f'{prefix}{SimpleYAML._scalar_str(data)}'
        return '\n'.join(lines)


# 别名
SimpleYAML = SimpleYAMLParser


def _yaml_loads(s: str) -> Any:
    """尝试标准库 yaml，回退到简单解析器"""
    try:
        import yaml
        return yaml.safe_load(s)
    except ImportError:
        return SimpleYAML.loads(s)


def _yaml_dumps(data: Any) -> str:
    try:
        import yaml
        return yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except ImportError:
        return SimpleYAML.dumps(data)


# ─── TOML 解析器（纯标准库） ─────────────────────────────────

class SimpleTOMLParser:
    """轻量 TOML 解析器"""

    @staticmethod
    def loads(s: str) -> dict:
        result: dict[str, Any] = {}
        current_section = result
        current_path: list[str] = []

        for line in s.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # [section] 或 [section.sub]
            m = re.match(r'^\[([^\]]+)\]$', line)
            if m:
                parts = m.group(1).split('.')
                current_section = result
                current_path = parts
                for p in parts:
                    if p not in current_section:
                        current_section[p] = {}
                    current_section = current_section[p]
                continue

            # key = value
            if '=' in line:
                idx = line.index('=')
                key = line[:idx].strip()
                val_str = line[idx + 1:].strip()
                current_section[key] = SimpleTOMLParser._parse_val(val_str)

        return result

    @staticmethod
    def _parse_val(s: str) -> Any:
        s = s.strip()
        # 字符串
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            return s[1:-1]
        # 三引号多行
        if s.startswith('"""'):
            return s[3:-3]
        # 布尔
        if s.lower() == 'true':
            return True
        if s.lower() == 'false':
            return False
        # 数组
        if s.startswith('['):
            inner = s[1:-1].strip()
            if not inner:
                return []
            items = SimpleTOMLParser._split_array(inner)
            return [SimpleTOMLParser._parse_val(i.strip()) for i in items]
        # 数字
        try:
            if '.' in s:
                return float(s)
            return int(s)
        except ValueError:
            pass
        # ISO日期
        if re.match(r'^\d{4}-\d{2}-\d{2}', s):
            return s
        return s

    @staticmethod
    def _split_array(s: str) -> list:
        items = []
        depth = 0
        current = ''
        for ch in s:
            if ch in '[(':
                depth += 1
            elif ch in '])':
                depth -= 1
            elif ch == ',' and depth == 0:
                items.append(current.strip())
                current = ''
                continue
            current += ch
        if current.strip():
            items.append(current.strip())
        return items

    @staticmethod
    def dumps(data: dict) -> str:
        lines = ['# Generated by format_converter.py\n']

        def _dump(d: dict, prefix=''):
            for k, v in d.items():
                full_key = f'{prefix}.{k}' if prefix else k
                if isinstance(v, dict) and v:
                    lines.append(f'[{full_key}]')
                    _dump(v, full_key)
                    lines.append('')
                elif isinstance(v, list):
                    formatted = ', '.join(SimpleTOML._val_str(i) for i in v)
                    lines.append(f'{k} = [{formatted}]')
                else:
                    lines.append(f'{k} = {SimpleTOML._val_str(v)}')

        _dump(data)
        return '\n'.join(lines)


SimpleTOML = SimpleTOMLParser


def _toml_loads(s: str) -> dict:
    try:
        import tomllib  # Python 3.11+
        return tomllib.loads(s)
    except ImportError:
        try:
            import toml
            return toml.loads(s)
        except ImportError:
            return SimpleTOML.loads(s)


def _toml_dumps(data: dict) -> str:
    try:
        import tomllib
        raise ImportError("tomllib only supports loading")
    except ImportError:
        try:
            import tomli_w
            return tomli_w.dumps(data)
        except ImportError:
            return SimpleTOML.dumps(data)


def _val_str(v: Any) -> str:
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, str):
        escaped = v.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    if v is None:
        return '""'
    if isinstance(v, list):
        items = [_val_str(i) for i in v]
        return '[' + ', '.join(items) + ']'
    return str(v)


# 绑定到类上
SimpleTOML._val_str = staticmethod(_val_str)
SimpleYAML._scalar_str = staticmethod(_val_str)


# ─── ENV 文件解析 ─────────────────────────────────────────────

def env_load(s: str) -> dict:
    """解析 .env 格式文件"""
    result = {}
    for line in s.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        idx = line.index('=')
        key = line[:idx].strip()
        val = line[idx + 1:].strip().strip('"').strip("'")
        result[key] = val
    return result


def env_dump(data: dict) -> str:
    lines = ['# Auto-generated by format_converter.py\n']
    for k, v in data.items():
        lines.append(f'{k}={v}')
    return '\n'.join(lines)


# ══════════════════════════════════════════════════════════════
#  转换函数
# ══════════════════════════════════════════════════════════════

def read_input(source: str) -> str:
    """读取输入（文件路径或直接字符串）"""
    if os.path.isfile(source):
        with open(source, 'r', encoding='utf-8') as f:
            return f.read()
    return source


def write_output(dest: Optional[str], content: str):
    """写入输出"""
    if dest:
        dir_name = os.path.dirname(dest)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(content)
        echo(f'✅ 已写入: {dest}', fg='green')
    else:
        print(content)


# ─── JSON 相关转换 ────────────────────────────────────────────

def cmd_json2yaml(args):
    inp = args['_pos'][0] if args.get('_pos') else '-'
    data = json.loads(read_input(inp))
    write_output(args.get('o'), _yaml_dumps(data))


def cmd_yaml2json(args):
    inp = args['_pos'][0] if args.get('_pos') else '-'
    data = _yaml_loads(read_input(inp))
    output = json.dumps(data, ensure_ascii=False, indent=2)
    write_output(args.get('o'), output)


def cmd_json2toml(args):
    inp = args['_pos'][0] if args.get('_pos') else '-'
    data = json.loads(read_input(inp))
    write_output(args.get('o'), _toml_dumps(data))


def cmd_toml2json(args):
    inp = args['_pos'][0] if args.get('_pos') else '-'
    data = _toml_loads(read_input(inp))
    output = json.dumps(data, ensure_ascii=False, indent=2)
    write_output(args.get('o'), output)


def cmd_json2ini(args):
    inp = args['_pos'][0] if args.get('_pos') else '-'
    data = json.loads(read_input(inp))
    cp = configparser.ConfigParser()
    for section, values in data.items():
        cp[section] = {}
        if isinstance(values, dict):
            for k, v in values.items():
                cp[section][k] = str(v)
    buf = io.StringIO()
    cp.write(buf)
    write_output(args.get('o'), buf.getvalue())


def cmd_ini2json(args):
    inp = args['_pos'][0] if args.get('_pos') else '-'
    cp = configparser.ConfigParser()
    cp.read_string(read_input(inp))
    result = {s: dict(cp.items(s)) for s in cp.sections()}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    write_output(args.get('o'), output)


def cmd_json2csv(args):
    """JSON → CSV（要求 JSON 是对象数组格式）"""
    inp = args['_pos'][0] if args.get('_pos') else '-'
    raw = json.loads(read_input(inp))
    rows = raw if isinstance(raw, list) else [raw]
    if not rows:
        echo('⚠️ 无数据', fg='yellow')
        return
    headers = list(rows[0].keys()) if isinstance(rows[0], dict) else ['value']
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
    write_output(args.get('o'), buf.getvalue())


def cmd_csv2json(args):
    inp = args['_pos'][0] if args.get('_pos') else '-'
    enc = args.get('encoding', 'utf-8')
    content = read_input(inp)
    reader = csv.DictReader(io.StringIO(content))
    rows = [row for row in reader]
    output = json.dumps(rows, ensure_ascii=False, indent=2)
    write_output(args.get('o'), output)


def cmd_json2env(args):
    inp = args['_pos'][0] if args.get('_pos') else '-'
    data = json.loads(read_input(inp))
    flat = _flatten_dict(data)
    write_output(args.get('o'), env_dump(flat))


def cmd_env2json(args):
    inp = args['_pos'][0] if args.get('_pos') else '-'
    data = env_load(read_input(inp))
    output = json.dumps(data, ensure_ascii=False, indent=2)
    write_output(args.get('o'), output)


# ─── Base64 / URL 编码（已迁移至 crypto_utils.py，请使用：crypto_utils.py base64-encode/decode / url-encode/decode）───
# Unicode 编解码（已移除，使用 text_utils.py convert-encoding 或 Python 内置）


# ─── 日期时间格式化 ───────────────────────────────────────────

def cmd_date_format(args):
    target = args['_pos'][0] if args.get('_pos') else 'now'
    from_fmt = args.get('from_fmt', '%Y-%m-%d %H:%M:%S')
    to_fmt = args.get('to_fmt', '%Y-%m-%d %H:%M:%S')
    tz_str = args.get('tz', '')

    if target.lower() == 'now':
        dt = datetime.datetime.now()
    else:
        try:
            dt = datetime.datetime.strptime(target, from_fmt)
        except ValueError:
            # 尝试常见格式
            for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y%m%d',
                        '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S',
                        '%b %d %Y', '%B %d, %Y',
                        '%a, %d %b %Y %H:%M:%S'):
                try:
                    dt = datetime.datetime.strptime(target, fmt)
                    break
                except ValueError:
                    continue
            else:
                echo(f'❌ 无法解析日期: {target}', fg='red')
                sys.exit(1)

    if tz_str:
        try:
            import zoneinfo
            dt = dt.replace(tzinfo=zoneinfo.ZoneInfo(tz_str))
        except ImportError:
            echo('⚠️ Python 3.9+ 才有时区支持', fg='yellow')

    result = dt.strftime(to_fmt)
    print(result)
    if args.get('o'):
        with open(args['o'], 'w', encoding='utf-8') as f:
            f.write(result)


def cmd_timestamp(args):
    """日期 ↔ Unix 时间戳互转"""
    target = args['_pos'][0] if args.get('_pos') else 'now'

    if target == 'now':
        ts = datetime.datetime.now().timestamp()
        print(int(ts))
        return

    try:
        ts = float(target)
        dt = datetime.datetime.fromtimestamp(ts)
        print(dt.strftime('%Y-%m-%d %H:%M:%S'))
    except ValueError:
        # 尝试解析为日期
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S',
                     '%Y/%m/%d %H:%M:%S'):
            try:
                dt = datetime.datetime.strptime(target, fmt)
                print(int(dt.timestamp()))
                break
            except ValueError:
                continue
        else:
            echo(f'❌ 无法解析: {target}', fg='red')


def cmd_duration_calc(args):
    """计算两个日期之间的差值"""
    if len(args.get('_pos', [])) < 2:
        echo('用法: duration-cal <date1> <date2>', fg='yellow')
        return
    d1_str, d2_str = args['_pos'][0], args['_pos'][1]
    unit = args.get('unit', 'days')

    for d_str in [d1_str, d2_str]:
        pass
    # 尝试多种格式
    parsed = []
    for d_str in [d1_str, d2_str]:
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S',
                     '%Y/%m/%d', '%Y%m%d'):
            try:
                parsed.append(datetime.datetime.strptime(d_str, fmt))
                break
            except ValueError:
                continue
        else:
            parsed.append(None)

    if None in parsed:
        echo(f'❌ 无法解析日期', fg='red')
        return

    delta = parsed[1] - parsed[0]
    units = {
        'days': delta.days,
        'hours': delta.total_seconds() / 3600,
        'minutes': delta.total_seconds() / 60,
        'seconds': delta.total_seconds(),
        'weeks': delta.days / 7,
    }
    val = units.get(unit, delta.days)
    echo(f'⏱️ 差值: {val:.2f} {unit}', fg='cyan')


# ─── .env 文件生成 ───────────────────────────────────────────

def cmd_generate_env(args):
    """从模板生成 .env 文件"""
    template = args['_pos'][0] if args.get('_pos') else ''
    output = args.get('o', '.env')
    fill_defaults = args.get('defaults', True)

    if not template or not os.path.isfile(template):
        echo('⚠️ 请提供模板文件路径', fg='yellow')
        echo('   用法: format_converter.py generate-env .env.example [-o .env]', fg='cyan')
        return

    with open(template, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    env_lines = ['# Auto-generated from ' + os.path.basename(template)]
    missing_keys = []

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            env_lines.append(line.rstrip())
            continue

        if '=' in stripped:
            eq_idx = stripped.index('=')
            key = stripped[:eq_idx].strip()
            val = stripped[eq_idx+1:].strip()

            existing_val = os.environ.get(key, '')
            is_placeholder = val.upper() in (
                '', 'YOUR_', 'CHANGE_ME', 'TODO', 'PLACEHOLDER',
                '<>', '""', "''", 'xxx', 'none', 'null', 'N/A'
            ) or any(p in val.upper() for p in
                      ['CHANGE', 'TODO', 'YOUR', 'SECRET', 'PASSWORD', 'KEY', 'TOKEN'])

            if is_placeholder and fill_defaults:
                if existing_val:
                    env_lines.append(f'{key}={existing_val}')
                else:
                    env_lines.append(f'{key}=')
                    missing_keys.append(key)
            elif existing_val and fill_defaults:
                env_lines.append(f'{key}={existing_val}')
            else:
                env_lines.append(stripped)
        else:
            env_lines.append(stripped)

    dest = output
    with open(dest, 'w', encoding='utf-8') as f:
        f.write('\n'.join(env_lines) + '\n')

    if missing_keys:
        echo(f'⚠️ 生成了 {dest}，以下 {len(missing_keys)} 个键需要填写:', fg='yellow')
        for k in missing_keys:
            echo(f'  {k}', fg='yellow')
    else:
        echo(f'✅ {dest} 已生成 (全部已填充)', fg='green')


def cmd_json_pretty(args):
    """JSON 美化 / 压缩"""
    inp = args['_pos'][0] if args.get('_pos') else '-'
    compress = args.get('compress', False)
    data = json.loads(read_input(inp))
    if compress:
        output = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    else:
        output = json.dumps(data, ensure_ascii=False, indent=2)
    write_output(args.get('o'), output)


# ─── 辅助函数 ─────────────────────────────────────────────────

def _flatten_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    """扁平化嵌套字典为 .env 风格的键"""
    items: dict[str, Any] = {}
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.update(_flatten_dict(v, new_key, sep))
        else:
            items[new_key] = str(v)
    return items


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'json2yaml': cmd_json2yaml,
    'yaml2json': cmd_yaml2json,
    'json2toml': cmd_json2toml,
    'toml2json': cmd_toml2json,
    'json2ini': cmd_json2ini,
    'ini2json': cmd_ini2json,
    'json2csv': cmd_json2csv,
    'csv2json': cmd_csv2json,
    'json2env': cmd_json2env,
    'env2json': cmd_env2json,
    'generate-env': cmd_generate_env,
    'date-format': cmd_date_format,
    'timestamp': cmd_timestamp,
    'duration-calc': cmd_duration_calc,
    'json-pretty': cmd_json_pretty,
}

ALIASES = {
    'j2y': 'json2yaml', 'y2j': 'yaml2json',
    'j2t': 'json2toml', 't2j': 'toml2json',
    'j2i': 'json2ini', 'i2j': 'ini2json',
    'j2c': 'json2csv', 'c2j': 'csv2json',
    'j2e': 'json2env', 'e2j': 'env2json',
    'ts': 'timestamp', 'date': 'date-format',
    'env': 'generate-env', 'dotenv': 'generate-env',
}


def main():
    args = parse_args()
    cmd = args['_cmd']
    cmd = ALIASES.get(cmd, cmd)

    if cmd not in COMMANDS:
        available = ', '.join(sorted(set(list(COMMANDS.keys()) + list(ALIASES.keys()))))
        echo(f'❌ 未知命令: {cmd}', fg='red')
        echo(f'可用命令: {available}', fg='cyan')
        sys.exit(1)

    COMMANDS[cmd](args)


if __name__ == '__main__':
    main()
