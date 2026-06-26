#!/usr/bin/env python3
"""
data_processor.py — 通用数据处理工具（纯标准库）
覆盖：过滤/排序/分组/聚合/统计/透视表/去重/合并/采样

用法：
  python data_processor.py filter data.csv --where "age>30" -o filtered.csv
  python data_processor.py sort data.csv --by age --desc
  python data_processor.py group data.csv --by department --agg avg:salary,count:id
  python data_processor.py stats data.csv --columns price,quantity
  python data_processor.py pivot data.csv --rows dept --cols month --values sales
  python data_processor.py dedup data.csv --by email -o clean.csv
  python data_processor.py merge users.csv orders.csv --on user_id -o joined.csv
  python data_processor.py sample data.csv --n 100 --random
  python data_processor.py fill data.csv --column age --value 0
  python data_processor.py transform data.csv --map "price=price*1.1" -o result.csv
"""

import sys
import os
import json
import csv
import io
import re
import math
import random
from collections import defaultdict, Counter
from typing import Any, Optional, Callable


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
                val = argv[i + 1]
                # 布尔标志
                if val.lower() in ('true', 'false'):
                    val = val.lower() == 'true'
                args[key] = val
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


# ─── 数据加载与输出 ──────────────────────────────────────────

class Dataset:
    """统一数据容器，支持 CSV / JSON / JSONL"""

    def __init__(self, rows: list[dict], fields: list[str] = None):
        self.rows = rows
        self.fields = fields or (list(rows[0].keys()) if rows else [])

    @classmethod
    def load(cls, source: str, encoding: str = 'utf-8') -> 'Dataset':
        """自动检测格式加载数据"""
        if not os.path.isfile(source):
            echo(f'❌ 文件不存在: {source}', fg='red')
            sys.exit(1)

        with open(source, 'r', encoding=encoding) as f:
            content = f.read().strip()

        # 检测格式
        if content.startswith('[') or content.startswith('{'):
            try:
                data = json.loads(content)
                if isinstance(data, list):
                    rows = data
                elif isinstance(data, dict):
                    rows = [data]
                else:
                    rows = []
                return cls(rows)
            except json.JSONDecodeError:
                pass

        if content.startswith('{'):
            # 可能是 JSONL
            rows = []
            for line in content.split('\n'):
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
            if rows:
                return cls(rows)

        # 默认 CSV
        reader = csv.DictReader(io.StringIO(content))
        rows = [row for row in reader]
        fields = list(reader.fieldnames) if reader.fieldnames else []
        return cls(rows, fields)

    def save(self, dest: str, fmt: str = None):
        """保存到文件，自动根据扩展名判断格式"""
        if not dest:
            echo(self.to_table(), end='')
            return

        ext = os.path.splitext(dest)[1].lower()
        d = os.path.dirname(dest)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

        if ext == '.json':
            with open(dest, 'w', encoding='utf-8') as f:
                json.dump(self.rows, f, ensure_ascii=False, indent=2)
        elif ext == '.jsonl':
            with open(dest, 'w', encoding='utf-8') as f:
                for row in self.rows:
                    f.write(json.dumps(row, ensure_ascii=False) + '\n')
        elif ext == '.csv' or ext is None:
            if not self.fields and self.rows:
                self.fields = list(self.rows[0].keys())
            with open(dest, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=self.fields)
                writer.writeheader()
                writer.writerows(self.rows)
        else:
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(str(self))
        echo(f'✅ 已写入 {len(self.rows)} 行 → {dest}', fg='green')

    def to_table(self, tablefmt: str = 'grid') -> str:
        """渲染为表格文本"""
        from scripts.table_format import tabulate as _tabulate
        if not self.rows:
            return '(空数据集)'
        if not self.fields:
            self.fields = list(self.rows[0].keys())
        # 截断长值用于显示
        display_rows = []
        for r in self.rows[:50]:
            dr = {}
            for k, v in r.items():
                s = str(v)
                dr[k] = s if len(s) <= 60 else s[:57] + '...'
            display_rows.append(dr)
        return _tabulate(display_rows, headers=self.fields, tablefmt=tablefmt)

    def copy(self) -> 'Dataset':
        return Dataset([dict(r) for r in self.rows], list(self.fields))


# ─── 表达式求值器（安全沙箱） ────────────────────────────────

class ExprEvaluator:
    """安全的数学/比较表达式求值"""

    SAFE_FUNCS = {
        'abs': abs, 'round': round, 'min': min, 'max': max,
        'sum': sum, 'len': len, 'float': float, 'int': int,
        'str': str, 'lower': lambda x: str(x).lower(),
        'upper': lambda x: str(x).upper(),
        'strip': lambda x: str(x).strip(),
        'startswith': lambda x, p: str(x).startswith(p),
        'endswith': lambda x, p: str(x).endswith(p),
        'contains': lambda x, sub: sub in str(x),
        'is_empty': lambda x: x is None or x == '',
        'is_number': lambda x: isinstance(x, (int, float)),
        'sqrt': math.sqrt, 'pow': pow,
        'log': math.log, 'log10': math.log10,
        'ceil': math.ceil, 'floor': math.floor,
    }

    @classmethod
    def eval(cls, expr: str, context: dict) -> Any:
        """
        安全求值表达式。
        支持：字段引用、比较运算、数学运算、逻辑运算、字符串方法
        例: "age > 30 and salary > 5000"
            "price * quantity > 1000"
            "name.startswith('张')"
        """
        # 注入上下文变量
        safe_dict = {'__builtins__': {}}
        safe_dict.update(cls.SAFE_FUNCS)
        safe_dict.update(context)

        # 替换常见写法
        expr = expr.strip()

        # 处理 None/null
        expr = re.sub(r'\bnull\b|\bNone\b', 'None', expr)

        # 处理字符串中的引号
        try:
            result = eval(expr, safe_dict)
            return result
        except Exception as e:
            raise ValueError(f'表达式解析失败: {expr} → {e}')

    @classmethod
    def eval_transform(cls, expr: str, row: dict) -> Any:
        """计算赋值表达式，如 'price=price*1.1' 或 'total=price*qty'"""
        if '=' in expr and not expr.startswith('='):
            # 赋值表达式
            parts = expr.split('=', 1)
            target = parts[0].strip()
            value_expr = parts[1].strip()
            return target, cls.eval(value_expr, row)
        else:
            # 纯表达式
            return None, cls.eval(expr, row)


# ══════════════════════════════════════════════════════════════
#  数据处理命令
# ══════════════════════════════════════════════════════════════

def cmd_filter(args):
    """过滤行"""
    src = args['_pos'][0] if args.get('_pos') else ''
    where_expr = args.get('where', '')
    enc = args.get('encoding', 'utf-8')
    limit = int(args.get('limit', 0))

    ds = Dataset.load(src, encoding=enc)
    if not where_expr:
        echo('⚠️ 请提供 --where 过滤条件', fg='yellow')
        return

    filtered = []
    for row in ds.rows:
        ctx = {k: _to_num(v) for k, v in row.items()}
        try:
            if ExprEvaluator.eval(where_expr, ctx):
                filtered.append(row)
        except ValueError:
            continue
        if limit and len(filtered) >= limit:
            break

    result = Dataset(filtered, ds.fields)
    echo(f'📊 过滤结果: {len(ds.rows)} → {len(filtered)} 行', fg='cyan')
    result.save(args.get('o'))


def cmd_sort(args):
    """排序"""
    src = args['_pos'][0] if args.get('_pos') else ''
    by_fields = args.get('by', '').split(',')
    desc = args.get('desc', False)
    enc = args.get('encoding', 'utf-8')

    ds = Dataset.load(src, encoding=enc)

    def sort_key(row):
        keys = []
        for f in by_fields:
            v = row.get(f.strip(), '')
            keys.append(_to_num_sort(v))
        return keys

    rows = sorted(ds.rows, key=sort_key, reverse=bool(desc))
    result = Dataset(rows, ds.fields)
    echo(f'📊 按 {by_fields} 排序完成 ({["升序", "降序"][bool(desc)]})', fg='cyan')
    result.save(args.get('o'))


def cmd_group(args):
    """分组聚合"""
    src = args['_pos'][0] if args.get('_pos') else ''
    by_field = args.get('by', '')
    agg_specs = args.get('agg', '').split(',')
    enc = args.get('encoding', 'utf-8')

    ds = Dataset.load(src, encoding=enc)
    groups: dict[str, list[dict]] = defaultdict(list)

    for row in ds.rows:
        key = str(row.get(by_field, ''))
        groups[key].append(row)

    # 解析聚合规则: func:field
    agg_funcs: list[tuple[str, str]] = []
    for spec in agg_specs:
        spec = spec.strip()
        if ':' in spec:
            fn, col = spec.split(':', 1)
            agg_funcs.append((fn.strip(), col.strip()))
        else:
            agg_funcs.append(('count', spec.strip()))

    result_rows = []
    for group_key, group_rows in groups.items():
        row_out = {by_field: group_key}
        for fn, col in agg_funcs:
            values = [_to_num(r.get(col, 0)) for r in group_rows]
            label = f'{fn}_{col}'
            if fn == 'count':
                row_out[label] = len(values)
            elif fn == 'sum':
                row_out[label] = sum(v for v in values if isinstance(v, (int, float)))
            elif fn == 'avg':
                nums = [v for v in values if isinstance(v, (int, float))]
                row_out[label] = round(sum(nums) / len(nums), 2) if nums else 0
            elif fn == 'min':
                nums = [v for v in values if isinstance(v, (int, float))]
                row_out[label] = min(nums) if nums else None
            elif fn == 'max':
                nums = [v for v in values if isinstance(v, (int, float))]
                row_out[label] = max(nums) if nums else None
            elif fn == 'first':
                row_out[label] = group_rows[0].get(col, '') if group_rows else ''
            elif fn == 'last':
                row_out[label] = group_rows[-1].get(col, '') if group_rows else ''
            elif fn == 'concat':
                row_out[label] = ', '.join(str(r.get(col, '')) for r in group_rows)
            elif fn == 'unique_count':
                row_out[label] = len(set(values))
        result_rows.append(row_out)

    fields = [by_field] + [f'{fn}_{col}' for fn, col in agg_funcs]
    result = Dataset(result_rows, fields)
    echo(f'📊 分组聚合: {len(groups)} 组, {len(result_rows)} 行', fg='cyan')
    result.save(args.get('o'))


def cmd_stats(args):
    """统计分析"""
    src = args['_pos'][0] if args.get('_pos') else ''
    columns = args.get('columns', '').split(',') if args.get('columns') else []
    enc = args.get('encoding', 'utf-8')

    ds = Dataset.load(src, encoding=enc)

    # 如果没指定列，分析所有数值列
    if not columns or columns == ['']:
        # 检测哪些列是数值型
        num_cols = []
        for col in ds.fields:
            sample_values = [_to_num(r.get(col)) for r in ds.rows[:100]]
            if any(isinstance(v, (int, float)) for v in sample_values if v != ''):
                num_cols.append(col)
        columns = num_cols
        if not columns:
            columns = ds.fields

    stats_data = []
    for col in columns:
        col = col.strip()
        values = []
        for r in ds.rows:
            v = _to_num(r.get(col, ''))
            if isinstance(v, (int, float)):
                values.append(v)

        if not values:
            stats_data.append({
                '列名': col, '数量': 0, '均值': '-', '标准差': '-',
                '最小值': '-', '最大值': '-', '中位数': '-', '总和': '-',
            })
            continue

        n = len(values)
        total = sum(values)
        mean = total / n
        variance = sum((v - mean) ** 2 for v in values) / n
        std_dev = math.sqrt(variance)
        sorted_vals = sorted(values)
        median = sorted_vals[n // 2]

        non_null = sum(1 for r in ds.rows if r.get(col, '') not in ('', None))

        stats_data.append({
            '列名': col, '非空数': non_null, '样本量': n,
            '均值': round(mean, 4), '标准差': round(std_dev, 4),
            '最小值': min(values), '最大值': max(values),
            '中位数': median, '总和': round(total, 4),
        })

    from scripts.table_format import tabulate
    print(tabulate(stats_data, tablefmt='grid'))

    # 可选导出
    if args.get('o'):
        with open(args['o'], 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, ensure_ascii=False, indent=2)
        echo(f'✅ 统计结果已写入: {args["o"]}', fg='green')


def cmd_pivot(args):
    """透视表"""
    src = args['_pos'][0] if args.get('_pos') else ''
    row_col = args.get('rows', '')
    col_col = args.get('cols', '')
    val_col = args.get('values', '')
    agg_fn = args.get('agg', 'sum')
    enc = args.get('encoding', 'utf-8')

    ds = Dataset.load(src, encoding=enc)

    pivot_data: dict[str, dict[str, Any]] = defaultdict(lambda: defaultdict(float))
    all_cols_set: set[str] = set()

    for row in ds.rows:
        r_key = str(row.get(row_col, ''))
        c_key = str(row.get(col_col, ''))
        val = _to_num(row.get(val_col, 0))
        all_cols_set.add(c_key)
        if agg_fn == 'sum':
            pivot_data[r_key][c_key] += val if isinstance(val, (int, float)) else 0
        elif agg_fn in ('avg', 'mean'):
            if not hasattr(pivot_data[r_key], '_counts'):
                pivot_data[r_key]._counts = defaultdict(int)
            pivot_data[r_key][c_key] = (
                (pivot_data[r_key].get(c_key, 0) * pivot_data[r_key]._counts[c_key] + val) /
                (pivot_data[r_key]._counts[c_key] + 1)
            )
            pivot_data[r_key]._counts[c_key] += 1
        elif agg_fn in ('first', 'last'):
            if agg_fn == 'first' and c_key not in pivot_data[r_key]:
                pivot_data[r_key][c_key] = val
            elif agg_fn == 'last':
                pivot_data[r_key][c_key] = val
        elif agg_fn == 'count':
            pivot_data[r_key][c_key] = pivot_data[r_key].get(c_key, 0) + 1

    all_cols = sorted(all_cols_set)
    result_fields = [row_col] + all_cols + ['总计']
    result_rows = []

    for r_key in sorted(pivot_data.keys()):
        row_out = {row_col: r_key}
        row_total = 0
        for c_key in all_cols:
            val = pivot_data[r_key].get(c_key, 0)
            if isinstance(val, float):
                val = round(val, 2)
            row_out[c_key] = val
            if isinstance(val, (int, float)):
                row_total += val
        row_out['总计'] = round(row_total, 2) if isinstance(row_total, float) else row_total
        result_rows.append(row_out)

    result = Dataset(result_rows, result_fields)
    echo(f'📊 透视表: {len(result_rows)} 行 × {len(all_cols)} 列', fg='cyan')
    result.save(args.get('o'))


def cmd_dedup(args):
    """去重"""
    src = args['_pos'][0] if args.get('_pos') else ''
    by_cols = args.get('by', '').split(',') if args.get('by') else []
    keep = args.get('keep', 'first')
    enc = args.get('encoding', 'utf-8')

    ds = Dataset.load(src, encoding=enc)
    seen: set[tuple] = set()
    deduped = []

    for row in ds.rows:
        if by_cols and by_cols != ['']:
            key = tuple(str(row.get(c.strip(), '')) for c in by_cols)
        else:
            key = tuple(sorted(row.items()))

        if key not in seen:
            seen.add(key)
            deduped.append(row)
        elif keep == 'last':
            # 先移除之前的同名项
            deduped = [r for r in deduped if (
                tuple(str(r.get(c.strip(), '')) for c in by_cols) if by_cols else sorted(r.items())
            ) != key]
            deduped.append(row)

    result = Dataset(deduped, ds.fields)
    echo(f'📊 去重: {len(ds.rows)} → {len(deduped)} 行 (-{len(ds.rows) - len(deduped)})', fg='cyan')
    result.save(args.get('o'))


def cmd_merge(args):
    """合并两个数据集"""
    src1 = args['_pos'][0] if len(args.get('_pos', [])) > 0 else ''
    src2 = args['_pos'][1] if len(args.get('_pos', [])) > 1 else ''
    on = args.get('on', '')
    how = args.get('how', 'inner')  # inner/left/right/outer
    enc = args.get('encoding', 'utf-8')

    ds1 = Dataset.load(src1, encoding=enc)
    ds2 = Dataset.load(src2, encoding=enc)

    on_cols = on.split(',') if on else []
    right_fields = [f for f in ds2.fields if f not in on_cols]

    merged = []
    matched_right: set[int] = set()

    for left_row in ds1.rows:
        for right_row in ds2.rows:
            match = True
            for c in on_cols:
                c = c.strip()
                if left_row.get(c) != right_row.get(c):
                    match = False
                    break
            if match:
                new_row = dict(left_row)
                for f in right_fields:
                    new_row[f'{f}_right'] = right_row.get(f)
                merged.append(new_row)
                matched_right.add(id(right_row))
                break
        else:
            if how in ('left', 'outer'):
                new_row = dict(left_row)
                for f in right_fields:
                    new_row[f'{f}_right'] = None
                merged.append(new_row)

    if how in ('right', 'outer'):
        for ri, right_row in enumerate(ds2.rows):
            if id(right_row) not in matched_right:
                new_row = {c: None for c in ds1.fields}
                for c in on_cols:
                    new_row[c] = right_row.get(c)
                for f in ds2.fields:
                    new_row[f] = right_row.get(f)
                merged.append(new_row)

    all_fields = ds1.fields + [f'{f}_right' for f in right_fields if f not in on_cols]
    result = Dataset(merged, all_fields)
    echo(f'📊 合并: {len(ds1.rows)} + {len(ds2.rows)} → {len(merged)} 行 [{how}]', fg='cyan')
    result.save(args.get('o'))


def cmd_sample(args):
    """采样"""
    src = args['_pos'][0] if args.get('_pos') else ''
    n = int(args.get('n', 10))
    ratio = args.get('ratio', None)
    random_flag = args.get('random', False)
    seed = args.get('seed', None)
    enc = args.get('encoding', 'utf-8')

    if seed:
        random.seed(int(seed))

    ds = Dataset.load(src, encoding=enc)

    if ratio:
        n = int(len(ds.rows) * float(ratio))

    if random_flag:
        sampled = random.sample(ds.rows, min(n, len(ds.rows)))
    else:
        sampled = ds.rows[:n]

    result = Dataset(sampled, ds.fields)
    echo(f'📊 采样: {len(ds.rows)} → {len(sampled)} 行 ({"随机" if random_flag else "头部"})', fg='cyan')
    result.save(args.get('o'))


def cmd_fill(args):
    """填充缺失值"""
    src = args['_pos'][0] if args.get('_pos') else ''
    column = args.get('column', '')
    value = args.get('value', '')
    strategy = args.get('strategy', 'literal')  # literal/mean/median/mode/forward/backward
    enc = args.get('encoding', 'utf-8')

    ds = Dataset.load(src, encoding=enc)
    filled = []

    # 计算填充值
    fill_value: Any = value
    if strategy == 'mean':
        vals = [_to_num(r.get(column, 0)) for r in ds.rows if isinstance(_to_num(r.get(column)), (int, float))]
        fill_value = round(sum(vals) / len(vals), 4) if vals else value
    elif strategy == 'median':
        vals = sorted([_to_num(r.get(column, 0)) for r in ds.rows if isinstance(_to_num(r.get(column)), (int, float))])
        fill_value = vals[len(vals) // 2] if vals else value
    elif strategy == 'mode':
        counter = Counter(str(r.get(column, '')) for r in ds.rows)
        fill_value = counter.most_common(1)[0][0] if counter else value

    last_val = None
    for row in ds.rows:
        r = dict(row)
        current = r.get(column)
        is_missing = current is None or current == '' or (isinstance(current, str) and current.strip() == '')

        if is_missing:
            if strategy == 'forward':
                r[column] = last_val if last_val is not None else fill_value
            elif strategy == 'backward':
                r[column] = fill_value  # 后向填充需要预扫描，简化为默认值
            else:
                r[column] = fill_value
        last_val = r.get(column)
        filled.append(r)

    result = Dataset(filled, ds.fields)
    missing_count = sum(1 for r in ds.rows if r.get(column) in (None, '', ''))
    echo(f'📊 填充: {missing_count} 个缺失值 → "{fill_value}" [{strategy}]', fg='cyan')
    result.save(args.get('o'))


def cmd_transform(args):
    """变换列（基于表达式）"""
    src = args['_pos'][0] if args.get('_pos') else ''
    map_exprs = args.get('map', '').split(',') if args.get('map') else []
    drop_cols = args.get('drop', '').split(',') if args.get('drop') else []
    rename_map: dict[str, str] = {}
    if args.get('rename'):
        for pair in args['rename'].split(','):
            if ':' in pair:
                old, new = pair.split(':', 1)
                rename_map[old.strip()] = new.strip()
    enc = args.get('encoding', 'utf-8')

    ds = Dataset.load(src, encoding=enc)
    transformed = []

    for row in ds.rows:
        r = dict(row)
        ctx = {k: _to_num(v) for k, v in r.items()}

        for expr in map_exprs:
            expr = expr.strip()
            try:
                target_name, value = ExprEvaluator.eval_transform(expr, ctx)
                if target_name:
                    r[target_name] = value
                    ctx[target_name] = _to_num(value)
            except Exception:
                continue

        # 重命名
        for old_name, new_name in rename_map.items():
            if old_name in r:
                r[new_name] = r.pop(old_name)

        # 删除列
        for dc in drop_cols:
            dc = dc.strip()
            r.pop(dc, None)

        transformed.append(r)

    # 更新字段列表
    new_fields = list(ds.fields)
    for expr in map_exprs:
        expr = expr.strip()
        if '=' in expr:
            target = expr.split('=')[0].strip()
            if target not in new_fields:
                new_fields.append(target)
    for old_name, new_name in rename_map.items():
        if old_name in new_fields:
            idx = new_fields.index(old_name)
            new_fields[idx] = new_name
    for dc in drop_cols:
        dc = dc.strip()
        if dc in new_fields:
            new_fields.remove(dc)

    result = Dataset(transformed, new_fields)
    echo(f'📊 变换完成: {len(transformed)} 行', fg='cyan')
    result.save(args.get('o'))


def cmd_stack(args):
    """纵向堆叠多个文件"""
    files = args.get('_pos', [])
    enc = args.get('encoding', 'utf-8')

    all_rows = []
    fields: list[str] = []
    for f in files:
        ds = Dataset.load(f, encoding=enc)
        if not fields:
            fields = list(ds.fields)
        all_rows.extend(ds.rows)

    result = Dataset(all_rows, fields)
    echo(f'📊 堆叠: {len(files)} 文件 → {len(all_rows)} 行', fg='cyan')
    result.save(args.get('o'))


def cmd_head_tail(args):
    """查看前/后 N 行"""
    src = args['_pos'][0] if args.get('_pos') else ''
    n = int(args.get('n', 10))
    mode = args.get('mode', 'head')
    enc = args.get('encoding', 'utf-8')

    ds = Dataset.load(src, encoding=enc)
    if mode == 'tail':
        rows = ds.rows[-n:]
    else:
        rows = ds.rows[:n]

    result = Dataset(rows, ds.fields)
    print(result.to_table())


def cmd_info(args):
    """数据集概览信息"""
    src = args['_pos'][0] if args.get('_pos') else ''
    enc = args.get('encoding', 'utf-8')

    ds = Dataset.load(src, encoding=enc)

    info_data = []
    for field in ds.fields:
        values = [r.get(field, '') for r in ds.rows]
        non_null = sum(1 for v in values if v not in ('', None))
        null_count = len(values) - non_null
        unique = len(set(str(v) for v in values))

        # 类型推断
        samples = [v for v in values if v not in ('', None)]
        numeric_samples = [_to_num(v) for v in samples if isinstance(_to_num(v), (int, float))]
        dtype = 'numeric' if len(numeric_samples) > len(samples) * 0.5 else 'text'

        info_data.append({
            '字段': field,
            '类型': dtype,
            '非空': non_null,
            '空值': null_count,
            '唯一值': unique,
        })

    from scripts.table_format import tabulate
    print(tabulate(info_data, tablefmt='grid'))
    echo(f'\n总行数: {len(ds.rows)}, 总字段: {len(ds.fields)}', fg='cyan')


# ─── 辅助函数 ─────────────────────────────────────────────────

def _to_num(v: Any) -> Any:
    """尝试转换为数字"""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        v_stripped = v.strip()
        if v_stripped == '':
            return None
        try:
            if '.' in v_stripped:
                return float(v_stripped)
            return int(v_stripped)
        except (ValueError, TypeError):
            return v
    return v


def _to_num_sort(v: Any) -> Any:
    """排序用的转换，保证 None 和空串排最后"""
    n = _to_num(v)
    if n is None or n == '' or (isinstance(n, str) and n.strip() == ''):
        return (1, '')  # 排后面
    if isinstance(n, (int, float)):
        return (0, n)
    return (0, str(n))


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'filter': cmd_filter,
    'sort': cmd_sort,
    'group': cmd_group,
    'stats': cmd_stats,
    'pivot': cmd_pivot,
    'dedup': cmd_dedup,
    'merge': cmd_merge,
    'sample': cmd_sample,
    'fill': cmd_fill,
    'transform': cmd_transform,
    'stack': cmd_stack,
    'head': cmd_head_tail,
    'tail': cmd_head_tail,
    'info': cmd_info,
}

ALIASES = {
    'grep': 'filter', 'order': 'sort',
    'groupby': 'group', 'aggregate': 'group',
    'statistics': 'stats', 'describe': 'info',
    'distinct': 'dedup', 'unique': 'dedup',
    'join': 'merge',
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
