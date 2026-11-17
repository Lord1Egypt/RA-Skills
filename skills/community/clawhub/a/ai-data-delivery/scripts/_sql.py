"""Bounded single-dataset expressions; shared scope for aggregates and details.

This is not a general SQL parser. Unsupported functions, SQL clauses, undeclared
fields and row references outside an aggregate are refused explicitly.
"""
import math
import re
from _contract import quote

AGGREGATES = {'COUNT', 'SUM', 'AVG', 'MIN', 'MAX'}
SCALARS = {'ABS', 'ROUND', 'COALESCE', 'IFNULL', 'NULLIF', 'LENGTH', 'LOWER', 'UPPER',
           'TRIM', 'LTRIM', 'RTRIM', 'SUBSTR', 'SUBSTRING', 'REPLACE', 'CAST'}
WORDS = {'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'AND', 'OR', 'NOT', 'IN', 'IS', 'NULL',
         'TRUE', 'FALSE', 'BETWEEN', 'LIKE', 'GLOB', 'ESCAPE'}
TOKEN = re.compile(r"(?P<space>\s+)|(?P<string>'(?:''|[^'])*')|"
                   r'(?P<quoted>"(?:""|[^"])*"|`(?:``|[^`])*`|\[[^\]]*\])|'
                   r"(?P<number>(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)|"
                   r"(?P<id>[^\W\d]\w*)|(?P<op>\|\||<=|>=|!=|<>|==|<<|>>|[(),.+*/%<>=~&|\-])", re.UNICODE)


class ExpressionError(ValueError):
    def __init__(self, kind, message):
        super().__init__(message)
        self.kind = kind


def _tokens(sql):
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError('表达式必须是非空文本')
    if len(sql) > 20000:
        raise ValueError('表达式超过有界编译器限制')
    out, pos = [], 0
    while pos < len(sql):
        match = TOKEN.match(sql, pos)
        if not match:
            raise ValueError('不支持 SQL 注释、多语句、参数或此表达式语法')
        kind, value = match.lastgroup, match.group()
        if kind != 'space': out.append((kind, value))
        pos = match.end()
    if any(out[i][1] == out[i + 1][1] == '-' or
           (out[i][1], out[i + 1][1]) == ('/', '*') for i in range(len(out) - 1)):
        raise ValueError('不支持 SQL 注释')
    return out


def _identifier(token):
    kind, value = token
    return value[1:-1].replace('""', '"').replace('``', '`') if kind == 'quoted' else value


def analyze_expression(sql, ds, aggregate=False):
    """Return normalized SQL and referenced fields, or raise ValueError.

    Aggregate mode requires an aggregate and forbids row fields outside one.
    Row mode forbids all aggregates. Literals never become identifiers/functions.
    """
    tokens = _tokens(sql)
    declared = {f.get('name') for f in ds.get('fields', []) if isinstance(f, dict)}
    allowed = {ds.get('name'), ds.get('source')}
    normalized, pos = [], 0
    while pos < len(tokens):
        token = tokens[pos]
        if pos + 1 < len(tokens) and tokens[pos + 1][1] == '.':
            if token[0] == 'quoted':
                raise ValueError('不支持带引号的限定字段；请用当前数据集非限定字段')
            if token[0] != 'id' or token[1] not in allowed:
                raise ValueError(f'跨表/未知前缀 {token[1]}，单表编译拒绝')
            if pos + 2 >= len(tokens) or tokens[pos + 2][0] not in {'id', 'quoted'}:
                raise ValueError('限定字段不完整')
            normalized.append(tokens[pos + 2]); pos += 3
        else:
            normalized.append(token); pos += 1
    tokens = normalized
    used, free, found = set(), set(), [False]

    def end_paren(start, end):
        depth = 0
        for i in range(start, end):
            if tokens[i][1] == '(': depth += 1
            elif tokens[i][1] == ')':
                depth -= 1
                if depth == 0: return i
        raise ValueError('表达式括号不完整')

    def arguments(start, end):
        depth, begin, result = 0, start, []
        for i in range(start, end):
            value = tokens[i][1]
            if value == '(': depth += 1
            elif value == ')': depth -= 1
            elif value == ',' and depth == 0:
                result.append((begin, i)); begin = i + 1
        result.append((begin, end))
        if any(a == b for a, b in result): raise ValueError('函数参数不能为空')
        return result

    def walk(start, end, inside=False, commas=False, depth=0):
        if depth > 60: raise ValueError('表达式嵌套超过有界编译器限制')
        i = start
        while i < end:
            kind, value = tokens[i]; upper = value.upper()
            if kind == 'id' and i + 1 < end and tokens[i + 1][1] == '(' and upper not in WORDS:
                close = end_paren(i + 1, end)
                args = arguments(i + 2, close)
                if upper in AGGREGATES:
                    if not aggregate or inside:
                        raise ExpressionError('invalid_aggregate', '过滤中或聚合内部不能再使用聚合函数')
                    if len(args) != 1:
                        raise ExpressionError('invalid_aggregate', f'{upper} 仅支持单参数聚合，不能作为逐行多参数函数')
                    found[0] = True
                    a, b = args[0]
                    if tokens[a][1].upper() == 'DISTINCT': a += 1
                    if a == b: raise ValueError('聚合缺少字段')
                    if b - a == 1 and tokens[a][1] == '*':
                        if upper != 'COUNT' or a != args[0][0]: raise ValueError('仅 COUNT(*) 支持星号')
                    else: walk(a, b, True, depth=depth + 1)
                elif upper in SCALARS:
                    if upper == 'CAST':
                        if len(args) != 1 or close < i + 5 or tokens[close - 2][1].upper() != 'AS' or tokens[close - 1][1].upper() not in {'INTEGER', 'INT', 'REAL', 'TEXT', 'NUMERIC', 'BLOB', 'FLOAT', 'DOUBLE'}:
                            raise ValueError('CAST 仅支持显式 SQLite 基本类型')
                        walk(i + 2, close - 2, inside, depth=depth + 1)
                    else:
                        for a, b in args: walk(a, b, inside, depth=depth + 1)
                else: raise ValueError(f'不支持函数 {value}；请使用已声明的有界单表表达式')
                i = close + 1; continue
            if value == '(':
                close = end_paren(i, end)
                walk(i + 1, close, inside, commas=i > start and tokens[i - 1][1].upper() == 'IN', depth=depth + 1)
                i = close + 1; continue
            if value == ')' or (value == ',' and not commas):
                raise ValueError('表达式必须产生一个值，不能包含多列或不配对括号')
            if kind == 'id' and upper in WORDS: pass
            elif kind in {'id', 'quoted'}:
                name = _identifier(tokens[i])
                clauses = {'SELECT', 'FROM', 'JOIN', 'UNION', 'PRAGMA', 'ATTACH', 'GROUP', 'HAVING',
                           'ORDER', 'LIMIT', 'OFFSET', 'WINDOW', 'OVER', 'WITH', 'RETURNING', 'INTO',
                           'WHERE', 'FILTER', 'COLLATE', 'AS', 'DISTINCT'}
                if kind == 'id' and upper in clauses:
                    raise ValueError(f'不支持 SQL 子句：{name}')
                if name not in declared:
                    raise ExpressionError('unknown_field', f'未声明字段：{name}')
                used.add(name)
                if not inside: free.add(name)
            elif value == '.': raise ValueError('不支持跨表或多段限定名')
            i += 1

    walk(0, len(tokens))
    if aggregate and (not found[0] or free):
        raise ExpressionError('invalid_aggregate', '标量指标必须使用聚合；不能混入聚合外字段' + ('：' + ', '.join(sorted(free)) if free else ''))
    return {'sql': ' '.join(value for _, value in tokens), 'fields': sorted(used)}


def _literal(value):
    if value is None: raise ValueError('filters.values 中 NULL 需用显式 extra_where IS NULL 口径')
    if isinstance(value, bool): return str(int(value))
    if isinstance(value, (int, float)):
        if not math.isfinite(value): raise ValueError('过滤值必须是有限数值')
        return str(value)
    if not isinstance(value, str): raise ValueError('过滤值仅支持文本、布尔或有限数值')
    return "'" + value.replace("'", "''") + "'"


def _scope(mt, ds):
    wheres, used = [], set()
    for item in mt.get('filters', []) or []:
        if not isinstance(item, dict) or not isinstance(item.get('values'), list) or not item['values']:
            raise ValueError('空或无效 filters.values 不能静默丢弃')
        field = analyze_expression(item['field'], ds)
        used.update(field['fields'])
        wheres.append(field['sql'] + ' IN (' + ','.join(map(_literal, item['values'])) + ')')
    if mt.get('extra_where'):
        extra = analyze_expression(mt['extra_where'], ds)
        used.update(extra['fields']); wheres.append(extra['sql'])
    return ' AND '.join(f'({item})' for item in wheres), used


def compile_scope(mt, ds):
    """Shared fixed filter; returns (WHERE expression without WHERE, error)."""
    try: return _scope(mt, ds)[0], None
    except (ValueError, KeyError, TypeError, AttributeError) as exc: return None, str(exc)


def _compile(mt, ds):
    if not ds or not ds.get('source'): raise ValueError('无数据集 source')
    if mt.get('join_path') or mt.get('joins'):
        raise ValueError('不支持跨表编译；请提供经验证的单表/视图映射')
    if mt.get('expr'): select = mt['expr']
    elif (mt.get('numerator') or {}).get('expr') and (mt.get('denominator') or {}).get('expr'):
        num, den = mt['numerator']['expr'], mt['denominator']['expr']
        policy = mt.get('on_zero_denominator', 'null')
        if policy == 'null': select = f'({num}) * 1.0 / NULLIF(({den}), 0)'
        elif policy == 'zero': select = f'COALESCE(({num}) * 1.0 / NULLIF(({den}), 0), 0)'
        elif policy == 'error': select = f"CASE WHEN ({den}) = 0 THEN 'ZERO_DENOMINATOR' ELSE ({num}) * 1.0 / ({den}) END"
        else: raise ValueError(f'on_zero_denominator 非法：{policy!r}（∈ null/zero/error）')
    else: raise ValueError('缺 expr 或完整分子分母')
    if mt.get('type') not in {'count', 'sum', 'avg', 'min', 'max', 'ratio'}:
        raise ValueError('本地编译器只支持单表标量聚合指标')
    expression = analyze_expression(select, ds, aggregate=True)
    scope, used = _scope(mt, ds)
    sql = f"SELECT {expression['sql']} AS v FROM {quote(ds['source'])}"
    if scope: sql += ' WHERE ' + scope
    return sql, sorted(used | set(expression['fields']))


def compile_single(mt, ds, names=()):
    """Compatibility API used by workbench, patch_model and reconcile_paths."""
    try: return _compile(mt, ds)[0], None
    except (ValueError, KeyError, TypeError, AttributeError) as exc: return None, str(exc)


def metric_dependencies(mt, ds):
    """Execution fields from the same validation used to compile the metric."""
    try: return {'fields': _compile(mt, ds)[1], 'error': None, 'error_kind': None}
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        return {'fields': [], 'error': str(exc), 'error_kind': getattr(exc, 'kind', 'unsupported')}
