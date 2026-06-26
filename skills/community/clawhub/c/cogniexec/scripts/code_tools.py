#!/usr/bin/env python3
"""
code_tools.py — 代码工具集（纯标准库）
覆盖：语法校验/依赖检查/Git辅助/代码格式化/代码搜索/TODO扫描/API提取

用法：
  python code_tools.py lint ./src --ext .py,.js
  python code_tools.py check-deps requirements.txt
  python code_tools.py find-todo ./src --tags FIXME,HACK,XXX
  python code_tools.py extract-api app.py --framework flask
  python code_tools.py count-lines ./project --by ext
  python code_tools.py git-log -n 10 --format short
  python code_tools.py git-branch --all
  python code_tools.py search-code "function.*pattern" ./src --ext .py
  python code_tools.py detect-lang ./unknown_file
  python code_tools.py check-imports module.py --missing-only
"""

import sys
import os
import re
import json
import ast
import tokenize
import io
from collections import Counter, defaultdict, OrderedDict
from typing import Optional, List, Dict, Tuple


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


def echo(text: str, fg: str = ''):
    print(color(text, fg))


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

# ─── Lint / 语法校验 ──────────────────────────────────────

def cmd_lint(args):
    """多语言语法检查（Python/JS/JSON/HTML/CSS）"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    ext_arg = args.get('ext', '.py')
    extensions = [e.strip() for e in ext_arg.split(',') if e.strip()]
    output = args.get('o', '')

    # 扫描文件
    files = []
    if os.path.isdir(src_dir):
        for root, dirs, filenames in os.walk(src_dir):
            dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules',
                                                        '.venv', 'dist', 'build')]
            for f in filenames:
                ext = os.path.splitext(f)[1].lower()
                if not extensions or ext in extensions:
                    files.append(os.path.join(root, f))
    elif os.path.isfile(src_dir):
        files.append(src_dir)

    if not files:
        echo('❌ 未找到文件', fg='red')
        return

    results = []
    total_errors = 0

    for idx, filepath in enumerate(files):
        sys.stderr.write(f'\r  检查中: {idx+1}/{len(files)}')
        sys.stderr.flush()
        ext = os.path.splitext(filepath)[1].lower()

        errors = []

        if ext == '.py':
            errors = _lint_python(filepath)
        elif ext in ('.js', '.ts', '.jsx', '.tsx'):
            errors = _lint_javascript(filepath)
        elif ext in ('.json', '.jsonl'):
            errors = _lint_json(filepath)
        elif ext in ('.html', '.htm'):
            errors = _lint_html(filepath)
        elif ext == '.css':
            errors = _lint_css(filepath)
        else:
            errors = [{'line': 0, 'col': 0,
                       'msg': f'未知文件类型: {ext}', 'level': 'info'}]

        file_result = {
            'file': filepath,
            'errors': len(errors),
            'status': '✅ OK' if not errors else f'❌ {len(errors)} issues',
        }
        if errors:
            file_result['details'] = errors[:20]  # 限制详情数量
        results.append(file_result)
        total_errors += len(errors)

    print()
    from scripts.table_format import tabulate
    ok_files = [r for r in results if r['errors'] == 0]
    err_files = [r for r in results if r['errors'] > 0]

    echo(f'📋 Lint 结果: {len(files)} 文件 | '
         f'{color(str(len(ok_files)), "green")} OK | '
         f'{color(str(len(err_files)), "red")} 有问题 | '
         f'{total_errors} 总问题',
         fg='cyan')

    # 显示有问题的文件
    if err_files:
        print('\n❌ 有问题的文件:')
        for r in err_files:
            echo(f'  {r["file"]}: {r["errors"]} 个问题', fg='red')
            if r.get('details'):
                for detail in r['details']:
                    lvl_color = 'red' if detail['level'] == 'error' else 'yellow'
                    echo(f'    L{detail["line"]}:{detail["col"]} [{detail["level"]}] {detail["msg"]}',
                         fg=lvl_color)

    if output:
        export = {'total_files': len(files), 'ok_files': len(ok_files),
                  'error_files': len(err_files), 'total_issues': total_errors,
                  'results': results}
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(export, f, ensure_ascii=False, indent=2)
        echo(f'\n📄 报告: {output}', fg='green')


def _lint_python(path: str) -> List[dict]:
    """Python 语法检查"""
    try:
        with open(path, 'rb') as f:
            source = f.read()
        try:
            ast.parse(source)
            return []
        except SyntaxError as e:
            return [{'line': e.lineno or 0, 'col': e.offset or 0,
                     'msg': str(e.msg), 'level': 'error'}]
    except Exception as e:
        return [{'line': 0, 'col': 0, 'msg': str(e), 'level': 'error'}]


def _lint_javascript(path: str) -> List[dict]:
    """JS/TS 基础检查（括号匹配、基本语法）"""
    errors = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        bracket_stack = []
        paren_stack = []
        brace_stack = []
        in_string = False
        string_char = ''

        for line_num, line in enumerate(lines, 1):
            i = 0
            while i < len(line):
                ch = line[i]

                # 字符串处理
                if not in_string and ch in ('"', "'", '`'):
                    in_string = True
                    string_char = ch
                    # 检查模板字符串
                    if ch == '`':
                        brace_stack.append(('`', line_num))
                elif in_string and ch == string_char:
                    # 检查转义
                    if i > 0 and line[i-1] != '\\':
                        in_string = False
                        string_char = ''
                    elif ch == '`' and brace_stack and brace_stack[-1][0] == '`':
                        brace_stack.pop()

                if in_string:
                    i += 1
                    continue

                if ch == '{':
                    brace_stack.append(('{', line_num))
                elif ch == '}':
                    if brace_stack and brace_stack[-1][0] != '`':
                        brace_stack.pop()
                    elif brace_stack:
                        pass  # template literal
                    else:
                        errors.append({'line': line_num, 'col': i,
                                       'msg': '不匹配的 }', 'level': 'warning'})
                elif ch == '(':
                    paren_stack.append(line_num)
                elif ch == ')':
                    if paren_stack:
                        paren_stack.pop()
                    else:
                        errors.append({'line': line_num, 'col': i,
                                       'msg': '不匹配的 )', 'level': 'warning'})
                elif ch == '[':
                    bracket_stack.append(line_num)
                elif ch == ']':
                    if bracket_stack:
                        bracket_stack.pop()
                    else:
                        errors.append({'line': line_num, 'col': i,
                                       'msg': '不匹配的 ]', 'level': 'warning'})

                i += 1

        # 未闭合括号
        if paren_stack:
            errors.append({'line': paren_stack[-1], 'col': 0,
                           'msg': '未闭合的 (', 'level': 'error'})
        if bracket_stack:
            errors.append({'line': bracket_stack[-1], 'col': 0,
                           'msg': '未闭合的 [', 'level': 'error'})
        open_braces = [b for b in brace_stack if b[0] == '{']
        if open_braces:
            errors.append({'line': open_braces[-1][1], 'col': 0,
                           'msg': '未闭合的 {', 'level': 'error'})

    except Exception as e:
        errors.append({'line': 0, 'col': 0, 'msg': str(e), 'level': 'error'})

    return errors[:30]


def _lint_json(path: str) -> List[dict]:
    """JSON 语法检查"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        if path.endswith('.jsonl'):
            for idx, line in enumerate(content.split('\n'), 1):
                line = line.strip()
                if line:
                    json.loads(line)
            return []
        json.loads(content)
        return []
    except json.JSONDecodeError as e:
        return [{'line': e.lineno or 0, 'col': e.colno or 0,
                 'msg': e.msg, 'level': 'error'}]
    except Exception as e:
        return [{'line': 0, 'col': 0, 'msg': str(e), 'level': 'error'}]


def _lint_html(path: str) -> List[dict]:
    """HTML 基础标签匹配检查"""
    errors = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查常见未闭合标签
        void_elements = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
                         'link', 'meta', 'param', 'source', 'track', 'wbr'}
        tag_stack = []

        tags = re.findall(r'<(/?)([\w-]+)[^>]*?(/?)>', content)
        for close_slash, tag_name, self_close in tags:
            tag_lower = tag_name.lower()
            if tag_lower in void_elements or self_close == '/':
                continue
            if close_slash == '/':
                if tag_stack and tag_stack[-1] == tag_lower:
                    tag_stack.pop()
                # 允许一些宽松情况
            else:
                tag_stack.append(tag_lower)

        if tag_stack:
            for t in tag_stack[:5]:
                errors.append({'line': 0, 'col': 0,
                               'msg': f'未闭合标签: <{t}>', 'level': 'warning'})

    except Exception as e:
        errors.append({'line': 0, 'col': 0, 'msg': str(e), 'level': 'error'})

    return errors[:15]


def _lint_css(path: str) -> List[dict]:
    """CSS 基础检查"""
    errors = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        brace_count = 0
        for line_no, line in enumerate(lines, 1):
            for ch in line:
                if ch == '{':
                    brace_count += 1
                elif ch == '}':
                    brace_count -= 1
        if brace_count > 0:
            errors.append({'line': 0, 'col': 0,
                           'msg': f'未闭合的花括号 (缺{brace_count}个}})', 'level': 'error'})
        elif brace_count < 0:
            errors.append({'line': 0, 'col': 0,
                           'msg': '多余的花括号 }}', 'level': 'error'})
    except Exception as e:
        errors.append({'line': 0, 'col': 0, 'msg': str(e), 'level': 'error'})
    return errors


# ─── TODO/FIXME 扫描 ────────────────────────────────────────

def cmd_find_todo(args):
    """扫描代码中的 TODO/FIXME/HACK 等标记"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    tags_raw = args.get('tags', 'TODO,FIXME,HACK,BUG,OPTIMIZE,REVIEW')
    tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
    case_sensitive = args.get('case', False)
    context_lines = int(args.get('context', 0))
    output = args.get('o', '')

    pattern_str = '|'.join(re.escape(t) for t in tags)
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.compile(pattern_str, flags)

    findings = []
    files_scanned = 0

    for root, dirs, filenames in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules',
                                                    '.venv', 'dist', 'build')]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            # 跳过二进制和无关文件
            if ext in ('.pyc', '.pyo', '.so', '.dll', '.exe', '.png', '.jpg',
                        '.gif', '.ico', '.woff', '.ttf', '.eot', '.zip'):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                files_scanned += 1

                for line_no, line in enumerate(lines, 1):
                    match = pattern.search(line)
                    if match:
                        tag_text = match.group()
                        # 提取 TODO 后面的描述
                        rest_of_line = line[match.end():].strip().rstrip()
                        # 提取 @assignee 或 () 内容
                        assignee = ''
                        desc = rest_of_line
                        m2 = re.match(r'\(([^)]*)\)\s*(.*)', rest_of_line)
                        if m2:
                            assignee = m2.group(1).strip()
                            desc = m2.group(2).strip()
                        elif '@' in rest_of_line[:20]:
                            m3 = re.match(r'@(\w+)\s*(.*)', rest_of_line)
                            if m3:
                                assignee = m3.group(1).strip()
                                desc = m3.group(2).strip()

                        finding = {
                            'file': fpath,
                            'line': line_no,
                            'tag': tag_text.upper(),
                            'text': desc[:120],
                            'assignee': assignee,
                            'context': line.rstrip()[:150],
                        }
                        if context_lines:
                            start = max(0, line_no - context_lines)
                            end = min(len(lines), line_no + context_lines + 1)
                            finding['code_context'] = ''.join(lines[start:end])
                        findings.append(finding)
            except (OSError, UnicodeDecodeError):
                continue

    from scripts.table_format import tabulate

    # 按标签分组统计
    tag_counts = Counter(f['tag'] for f in findings)
    echo(f'🔍 TODO 扫描: {src_dir}', fg='cyan', bold=True)
    echo(f'   文件数: {files_scanned} | 发现: {len(findings)} 条标记', fg='blue')

    if tag_counts:
        tag_rows = [[tag, count] for tag, count in tag_counts.most_common()]
        echo(f'\n📊 标签分布:', fg='cyan')
        print(tabulate(tag_rows, headers=['标签', '数量'], tablefmt='grid'))

    # 详细列表
    if findings:
        echo(f'\n📝 详情:', fg='cyan')
        rows = [{
            '标签': f['tag'],
            '行号': f['line'],
            '负责人': f['assignee'] or '-',
            '内容': f['text'][:60],
            '文件': os.path.basename(f['file']),
        } for f in sorted(findings, key=lambda x: (x['tag'], x['file'], x['line']))]
        print(tabulate(rows, tablefmt='grid'))
    else:
        echo('✅ 无 TODO 标记', fg='green')

    if output:
        export = {'scanned_files': files_scanned, 'total_findings': len(findings),
                  'tag_stats': dict(tag_counts), 'findings': findings}
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(export, f, ensure_ascii=False, indent=2)


# ─── API 提取 ──────────────────────────────────────────────

def cmd_extract_api(args):
    """从源码中提取 API 端点/函数定义"""
    source = args['_pos'][0] if args.get('_pos') else ''
    framework = args.get('framework', '').lower()  # flask, fastapi, express, django
    output = args.get('o', '')

    if not os.path.isfile(source):
        echo(f'❌ 文件不存在: {source}', fg='red')
        sys.exit(1)

    with open(source, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    apis = []

    # Flask 路由
    flask_patterns = [
        (r'@app\.route\([\'"]([^\'"]+)[\'"](?:\s*,\s*methods=\[([^\]]+)\])?', 'GET'),
        (r'@(\w+)\.route\([\'"]([^\'"]+)[\'"](?:\s*,\s*methods=\[([^\]]+)\])?', 'GET'),
    ]
    for pat, default_method in flask_patterns:
        for m in re.finditer(pat, content, re.MULTILINE):
            methods_str = m.group(3) if m.lastindex >= 3 else ''
            methods = [s.strip().strip('"\'') for s in methods_str.split(',')] \
                if methods_str else [default_method]
            apis.append({
                'method': ', '.join(methods) if methods else default_method,
                'path': m.group(2) if m.lastindex >= 2 else m.group(1),
                'framework': 'Flask',
            })

    # FastAPI / Flask-RESTful
    fastapi_pats = [
        r'@(?:app|router)\.(get|post|put|delete|patch|options|head)\([\'"]([^\'"]+)',
        r'@api\.resource\([\'"]([^\'"]+)',
    ]
    for pat in fastapi_pats:
        for m in re.finditer(pat, content, re.MULTILINE | re.IGNORECASE):
            apis.append({
                'method': m.group(1).upper(),
                'path': m.group(2) if m.lastindex >= 2 else m.group(1),
                'framework': framework.capitalize() or 'API',
            })

    # Express.js 风格
    express_pats = [
        r'(?:app|router)\.(get|post|put|delete|patch)\s*\([\'"]([^\'"]+)',
        r'(?:app|router)\.(use)\s*\([\'"]([^\'"]+)',
    ]
    for pat in express_pats:
        for m in re.finditer(pat, content, re.MULTILINE | re.IGNORECASE):
            apis.append({
                'method': m.group(1).upper(),
                'path': m.group(2),
                'framework': 'Express.js',
            })

    # Django URL patterns
    django_pats = [
        r"path\([\'\"]([^\'\"]+)[\'\"].*?(?:name=[\'\"]([^\'\"]+)[\'\"])?",
        r"url\(r?[\'\"]([^\'\"]+)[\'\"].*?(?:name=[\'\"]([^\'\"]+)[\'\"])?",
        r"re_path\(r?[\'\"]([^\'\"]+)[\'\"].*?",
    ]
    for pat in django_pats:
        for m in re.finditer(pat, content, re.MULTILINE):
            name = m.group(2) if m.lastindex >= 2 else ''
            apis.append({
                'method': '(Django)',
                'path': m.group(1),
                'name': name or '',
                'framework': 'Django',
            })

    # Python 函数定义 (通用 fallback)
    func_defs = re.finditer(
        r'^\s*(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)',
        content, re.MULTILINE
    )
    public_funcs = [m for m in func_defs
                     if not m.group(1).startswith('_') and m.group(1) != 'main']

    # 去重
    seen = set()
    unique_apis = []
    for api in apis:
        key = (api.get('method', ''), api.get('path', ''))
        if key not in seen:
            seen.add(key)
            unique_apis.append(api)

    # 输出
    from scripts.table_format import tabulate

    if unique_apis:
        echo(f'🔗 提取到的 API ({source}):', fg='cyan', bold=True)
        rows = [{
            '方法': a.get('method', ''),
            '路径': a.get('path', ''),
            '名称': a.get('name', '') or '-',
            '框架': a.get('framework', ''),
        } for a in unique_apis]
        print(tabulate(rows, tablefmt='grid'))
    else:
        echo('⚠️ 未检测到标准路由模式，尝试函数列表:', fg='yellow')
        if public_funcs:
            func_rows = [[f'  def {m.group(1)}({m.group(2)[:50]}...)']
                         for m in public_funcs[:30]]
            for row in func_rows:
                print(row[0])

    # 公共函数列表
    if public_funcs:
        echo(f'\n📋 公共函数 ({len(public_funcs)}):', fg='cyan')
        for f in public_funcs[:25]:
            sig = f.group(2)[:40]
            echo(f'  {f.group(1)}({sig})')

    if output:
        export = {'apis': unique_apis,
                  'functions': [{'name': m.group(1), 'args': m.group(2)}
                               for m in public_funcs]}
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(export, f, ensure_ascii=False, indent=2)


# ─── 行数统计 ──────────────────────────────────────────────

def cmd_count_lines(args):
    """代码行数统计"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    group_by = args.get('by', 'ext')  # ext, dir, type
    output = args.get('o', '')

    stats: dict[str, dict] = defaultdict(lambda: {
        'files': 0, 'lines': 0, 'code': 0, 'blank': 0, 'comment': 0, 'bytes': 0
    })
    total = {'files': 0, 'lines': 0, 'code': 0, 'bytes': 0}

    for root, dirs, filenames in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules',
                                                    '.venv', 'dist', 'build')]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            # 跳过二进制
            if ext in ('.pyc', '.pyo', '.so', '.dll', '.exe', '.png', '.jpg',
                        '.gif', '.ico', '.woff', '.ttf', '.eot', '.zip', '.bin'):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                total['files'] += 1
                fsize = os.path.getsize(fpath)

                code_lines = 0
                blank_lines = 0
                comment_lines = 0

                in_block_comment = False
                is_py = ext == '.py'

                for line in lines:
                    stripped = line.strip()
                    if not stripped:
                        blank_lines += 1
                    elif is_py and stripped.startswith('#'):
                        comment_lines += 1
                    elif ext in ('.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp',
                                  '.h', '.cs', '.go', '.rs', '.swift', '.kt'):
                        if in_block_comment:
                            comment_lines += 1
                            if '*/' in stripped:
                                in_block_comment = False
                        elif stripped.startswith('//'):
                            comment_lines += 1
                        elif stripped.startswith('/*'):
                            comment_lines += 1
                            if '*/' not in stripped:
                                in_block_comment = True
                        else:
                            code_lines += 1
                    elif ext in ('.html', '.css', '.scss', '.xml', '.svg'):
                        if '<!--' in stripped or '/*' in stripped or stripped.startswith('*'):
                            comment_lines += 1
                        else:
                            code_lines += 1
                    else:
                        code_lines += 1

                key = ext or '(no_ext)' if group_by == 'ext' else \
                      os.path.dirname(fpath) if group_by == 'dir' else ext
                stats[key]['files'] += 1
                stats[key]['lines'] += len(lines)
                stats[key]['code'] += code_lines
                stats[key]['blank'] += blank_lines
                stats[key]['comment'] += comment_lines
                stats[key]['bytes'] += fsize

                total['lines'] += len(lines)
                total['code'] += code_lines
                total['bytes'] += fsize

            except OSError:
                continue

    from scripts.table_format import tabulate
    echo(f'📊 代码统计: {src_dir}', fg='cyan', bold=True)

    if group_by == 'ext':
        rows = sorted([
            {
                '扩展名': k,
                '文件数': v['files'],
                '总行数': v['lines'],
                '代码行': v['code'],
                '注释行': v['comment'],
                '空行': v['blank'],
                '大小': _fmt_size(v['bytes']),
            }
            for k, v in stats.items()
        ], key=lambda x: x['总行数'], reverse=True)
    else:
        rows = []

    print(tabulate(rows, tablefmt='grid'))

    echo(f'\n总计: {total["files"]} 文件, {total["lines"]} 行 '
         f'(代码: {total["code"]}, 大小: {_fmt_size(total["bytes"])})', fg='cyan')

    if output:
        export = dict(stats), total
        with open(output, 'w', encoding='utf-8') as f:
            json.dump({'by_group': dict(stats), 'total': total}, f, ensure_ascii=False, indent=2)


# ─── Git 辅助 ────────────────────────────────────────────────

def cmd_git_log(args):
    """格式化 Git 日志输出"""
    n = int(args.get('n', 10))
    fmt = args.get('format', 'short')  # short, medium, oneline, json
    author = args.get('author', '')
    since = args.get('since', '')
    grep_msg = args.get('grep', '')

    import subprocess

    base_cmd = ['git', 'log', '-n', str(n)]
    if fmt == 'oneline':
        base_cmd.append('--oneline')
    elif fmt == 'medium':
        pass
    elif fmt == 'json':
        base_cmd.extend(['--pretty=format:%H|%an|%ae|%ad|%s'])
    else:  # short
        base_cmd.extend(['--pretty=format:%h %ad | %an | %s', '--date=short'])

    if author:
        base_cmd.extend(['--author', author])
    if since:
        base_cmd.extend(['--since', since])
    if grep_msg:
        base_cmd.extend(['--grep', grep_msg])

    try:
        result = subprocess.run(base_cmd, capture_output=True, text=True,
                                cwd=os.getcwd(), timeout=30)
        output_text = result.stdout.strip()

        if result.returncode != 0:
            echo(f'⚠️ Git 错误: {result.stderr.strip()}',
                 fg='yellow' if 'not a git repository' in result.stderr else 'red')
            if 'not a git repository' in result.stderr:
                return
    except FileNotFoundError:
        echo('❌ Git 未安装或不在 PATH 中', fg='red')
        return
    except subprocess.TimeoutExpired:
        echo('❌ Git 操作超时', fg='red')
        return

    if fmt == 'json':
        lines = output_text.split('\n')
        entries = []
        for line in lines:
            parts = line.split('|', 4)
            if len(parts) >= 5:
                entries.append({
                    'hash': parts[0],
                    'author': parts[1],
                    'email': parts[2],
                    'date': parts[3],
                    'message': parts[4],
                })
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        if args.get('o'):
            with open(args['o'], 'w', encoding='utf-8') as f:
                json.dump(entries, f, ensure_ascii=False, indent=2)
    else:
        print(output_text or '(无提交记录)')
        echo(f'\n共 {len(output_text.split(chr(10)))} 条提交' if output_text else '', fg='cyan')


def cmd_git_branch(args):
    """分支管理信息"""
    show_all = args.get('all', False)
    import subprocess

    cmd = ['git', 'branch']
    if show_all:
        cmd.append('-a')

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            echo(f'⚠️ {result.stderr.strip()}', fg='yellow')
            return

        branches = result.stdout.strip().split('\n')
        current = None
        branch_list = []
        for b in branches:
            b = b.strip()
            if b.startswith('* '):
                current = b[2:].strip()
                branch_list.append(f'* {color(current, "green")}')
            elif b:
                branch_list.append(f'  {b}')

        echo('📂 Git 分支:', fg='cyan', bold=True)
        if current:
            echo(f'   当前分支: {current}', fg='green', bold=True)
        for b in branch_list:
            print(b)
        echo(f'   共 {len(branches)} 个分支', fg='cyan')

    except Exception as e:
        echo(f'❌ {e}', fg='red')


# ─── 代码搜索 ────────────────────────────────────────────────

def cmd_search_code(args):
    """在代码中搜索正则表达式"""
    pattern = args['_pos'][0] if args.get('_pos') else ''
    src_dir = args['_pos'][1] if len(args.get('_pos', [])) > 1 else '.'
    ext_filter = args.get('ext', '')
    ignore_case = args.get('i', False)
    context_before = int(args.get('before', 2))
    context_after = int(args.get('after', 2))

    if not pattern:
        echo('⚠️ 请提供搜索模式', fg='yellow')
        return

    extensions = [e.strip() for e in ext_filter.split(',')] if ext_filter else []
    flags = re.IGNORECASE if ignore_case else 0
    compiled = re.compile(pattern, flags)

    matches = []
    files_searched = 0

    for root, dirs, filenames in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules',
                                                    '.venv', 'dist', 'build')]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if extensions and ext not in extensions:
                continue
            if ext in ('.pyc', '.png', '.jpg', '.gif', '.ico', '.woff', '.zip'):
                continue

            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                files_searched += 1

                for line_no, line in enumerate(lines, 1):
                    for m in compiled.finditer(line):
                        context_start = max(0, line_no - 1 - context_before)
                        context_end = min(len(lines), line_no + context_after)
                        matches.append({
                            'file': fpath,
                            'line': line_no,
                            'col': m.start() + 1,
                            'match': m.group()[:80],
                            'line_content': line.rstrip()[:120],
                            'context': ''.join(lines[context_start:context_end]),
                        })
            except (OSError, UnicodeDecodeError):
                continue

    from scripts.table_format import tabulate
    echo(f'🔍 搜索 "{pattern}" 在 {src_dir}:', fg='cyan', bold=True)
    echo(f'   扫描 {files_searched} 文件, 匹配 {len(matches)} 处', fg='blue')

    if matches:
        rows = [{
            '文件': os.path.basename(m['file']),
            '行': m['line'],
            '列': m['col'],
            '匹配': m['match'],
            '内容': m['line_content'].strip()[:60],
        } for m in matches[:100]]
        print(tabulate(rows, tablefmt='grid'))
        if len(matches) > 100:
            echo(f'  ... 还有 {len(matches)-100} 条', fg='yellow')
    else:
        echo('无匹配结果', fg='green')


# ─── 语言检测 ────────────────────────────────────────────────

LANG_SIGNATURES = {
    'Python': ['.py', ['import ', 'from ', 'def ', 'class ', '# ', '__init__']],
    'JavaScript': ['.js', ['const ', 'let ', 'var ', 'function ', '=>', 'require(']],
    'TypeScript': ['.ts', ['.tsx', ': ', 'interface ', 'type ', 'enum ']],
    'Java': ['.java', ['public class ', 'private ', 'protected ', '@Override']],
    'Go': ['.go', ['func ', 'package ', 'import "', ':= ', 'chan ']],
    'Rust': ['.rs', ['fn ', 'let mut ', 'impl ', 'pub fn ', 'use ']],
    'C': ['.c', ['#include<', '#include "', 'int main(', 'printf(', 'malloc(']],
    'C++': ['.cpp', ['#include<', 'std::', 'namespace ', 'cout<<', 'vector<']],
    'C#': ['.cs', ['using ', 'namespace ', 'public void ', 'class ', ': IEnumerable']],
    'Ruby': ['.rb', ['def ', 'end', 'require ', 'puts ', '@', '||']],
    'PHP': ['.php', ['<?php', '$', 'function ', 'echo ', 'namespace ']],
    'HTML': ['.html', ['.htm', '<!DOCTYPE html>', '<div ', '<script ', '<style ']],
    'CSS': ['.css', ['.scss', '.sass', '{', ': ', ';', '@media', '@import']],
    'Shell': ['.sh', ['.bash', '.zsh', '#!/', 'export ', 'if [', 'echo ', 'fi']],
    'SQL': ['.sql', ['SELECT ', 'FROM ', 'WHERE ', 'INSERT INTO', 'CREATE TABLE']],
    'YAML': ['.yml', ['.yaml', 'key:', '  subkey:', '"value"']],
    'JSON': ['.json', ['{"', '": "', '[{']],
    'Markdown': ['.md', ['# ', '## ', '**', '*[](', '```', '> ']],
}


def cmd_detect_lang(args):
    """检测文件编程语言"""
    target = args['_pos'][0] if args.get('_pos') else ''

    if os.path.isdir(target):
        # 目录模式：统计各语言占比
        lang_stats: dict[str, dict] = defaultdict(lambda: {'files': 0, 'lines': 0})
        for root, dirs, filenames in os.walk(target):
            dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
            for f in filenames:
                fpath = os.path.join(root, f)
                lang = _detect_language(fpath)
                if lang:
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                            lc = sum(1 for _ in fp)
                    except OSError:
                        lc = 0
                    lang_stats[lang]['files'] += 1
                    lang_stats[lang]['lines'] += lc

        from scripts.table_format import tabulate
        rows = sorted([
            {'语言': k, **v}
            for k, v in lang_stats.items()
        ], key=lambda x: x['lines'], reverse=True)
        print(tabulate(rows, tablefmt='grid'))
        total_lines = sum(v['lines'] for v in lang_stats.values())
        echo(f'总行数: {total_lines}', fg='cyan')

    elif os.path.isfile(target):
        lang = _detect_language(target)
        if lang:
            echo(f'📝 {target}', fg='cyan')
            echo(f'   语言: {lang}', fg='green')
            # 显示更多语言信息
            try:
                with open(target, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                echo(f'   行数: {len(lines)}', fg='blue')
                echo(f'   大小: {_fmt_size(os.path.getsize(target))}', fg='blue')
            except OSError:
                pass
        else:
            echo(f'⚠️ 无法识别: {target}', fg='yellow')


def _detect_language(filepath: str) -> Optional[str]:
    """单文件语言检测"""
    ext = os.path.splitext(filepath)[1].lower()

    # 先按扩展名快速判断
    scores: dict[str, float] = {}
    for lang, info in LANG_SIGNATURES.items():
        ext_list = info[0]
        if isinstance(ext_list, list):
            if ext in ext_list:
                scores[lang] = 5.0
                break
        elif ext == ext_list:
            scores[lang] = 5.0
            break

    # 如果扩展名不确定，用内容特征
    if len(scores) <= 1:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                sample = f.read(2048)
            for lang, info in LANG_SIGNATURES.items():
                features = info[1] if len(info) > 1 else []
                hit = sum(2 for feat in features if feat in sample)
                if hit > 0:
                    scores[lang] = scores.get(lang, 0) + hit
        except (OSError, UnicodeDecodeError):
            pass

    if not scores:
        return None
    return max(scores, key=scores.get)


# ─── 导入检查 ────────────────────────────────────────────────

def cmd_check_imports(args):
    """检查 Python 模块的导入依赖"""
    source = args['_pos'][0] if args.get('_pos') else ''
    missing_only = args.get('missing_only', False)
    output = args.get('o', '')

    if os.path.isfile(source):
        files = [source]
    elif os.path.isdir(source):
        files = []
        for root, dirs, filenames in os.walk(source):
            dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__')]
            for f in filenames:
                if f.endswith('.py'):
                    files.append(os.path.join(root, f))
    else:
        echo(f'❌ 路径不存在: {source}', fg='red')
        return

    all_imports: dict[str, List[Tuple[str, int]]] = {}
    local_modules: set = set()

    for filepath in files:
        try:
            tree = ast.parse(open(filepath, 'r', encoding='utf-8').read())
        except SyntaxError:
            continue
        basename = os.path.splitext(os.path.basename(filepath))[0]

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name.split('.')[0]
                    all_imports.setdefault(name, []).append((filepath, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    name = node.module.split('.')[0]
                    all_imports.setdefault(name, []).append((filepath, node.lineno))
                    if not node.level:  # 非相对导入
                        local_modules.add(name)

    # 标准库模块集合
    stdlib_modules = {
        'os', 'sys', 're', 'json', 'collections', 'itertools', 'functools',
        'datetime', 'math', 'random', 'hashlib', 'base64', 'urllib',
        'http', 'email', 'xml', 'html', 'csv', 'io', 'pathlib', 'tempfile',
        'subprocess', 'threading', 'multiprocessing', 'socket', 'ssl',
        'logging', 'argparse', 'configparser', 'unittest', 'typing',
        'abc', 'copy', 'pprint', 'textwrap', 'string', 'struct',
        'time', 'calendar', 'locale', 'codecs', 'unicodedata', 'difflib',
        'enum', 'numbers', 'decimal', 'fractions', 'operator', 'pickle',
        'shelve', 'sqlite3', 'zlib', 'gzip', 'bz2', 'lzma', 'tarfile',
        'zipfile', 'shutil', 'glob', 'fnmatch', 'stat', 'fileinput',
        'warnings', 'contextlib', 'dataclasses', 'types', 'inspect',
        'dis', 'weakref', 'gc', 'traceback', 'trace', 'profile', 'pstats',
        'timeit', 'unittest', 'doctest', 'pdb', 'cProfile', 'venv',
        'secrets', 'concurrent', 'asyncio', 'pathlib', 'enum',
    }

    results = {'stdlib': [], 'third_party': [], 'local': [], 'unknown': []}
    unknown_names = []

    for mod_name, locations in all_imports.items():
        if mod_name in stdlib_modules:
            if not missing_only:
                results['stdlib'].append({'module': mod_name, 'used_in': len(locations)})
        elif mod_name in local_modules:
            if not missing_only:
                results['local'].append({'module': mod_name, 'used_in': len(locations)})
        else:
            # 尝试导入以确认是否可安装（限制为安全的模块名）
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_.]*$', mod_name):
                continue
            try:
                import importlib
                importlib.import_module(mod_name)
                if not missing_only:
                    results['third_party'].append({
                        'module': mod_name, 'used_in': len(locations),
                        'installed': True
                    })
            except ImportError:
                results['third_party'].append({
                    'module': mod_name, 'used_in': len(locations),
                    'installed': False
                })
                unknown_names.append(mod_name)

    from scripts.table_format import tabulate
    echo(f'📦 导入分析: {source}', fg='cyan', bold=True)

    if not missing_only:
        for cat in ['stdlib', 'local']:
            cat_results = results[cat]
            if cat_results:
                echo(f'\n  {cat.replace("_", " ").title()} ({len(cat_results)}):', fg='blue')
                print(tabulate(cat_results, tablefmt='grid'))

    third_party = results['third_party']
    if third_party:
        installed = [t for t in third_party if t.get('installed')]
        missing = [t for t in third_party if not t.get('installed')]
        if installed and not missing_only:
            echo(f'\n  第三方已安装 ({len(installed)}):', fg='green')
            print(tabulate(installed, tablefmt='grid'))

    if missing:
        echo(f'\n  ⚠️ 缺失依赖 ({len(missing)}):', fg='red', bold=True)
        print(tabulate(missing, tablefmt='grid'))
        # 输出 pip install 命令
        pkg_names = [t['module'] for t in missing]
        echo(f'  安装命令: pip install {" ".join(pkg_names)}', fg='yellow')

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)


# ─── 工具函数 ─────────────────────────────────────────────────

def _fmt_size(b: int) -> str:
    for u in ['B', 'KB', 'MB', 'GB']:
        if b < 1024:
            return f'{b:.1f} {u}'
        b /= 1024
    return f'{b:.1f} TB'


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'lint': cmd_lint,
    'find-todo': cmd_find_todo,
    'extract-api': cmd_extract_api,
    'count-lines': cmd_count_lines,
    'git-log': cmd_git_log,
    'git-branch': cmd_git_branch,
    'search-code': cmd_search_code,
    'detect-lang': cmd_detect_lang,
    'check-imports': cmd_check_imports,
}

ALIASES = {
    'syntax-check': 'lint', 'validate': 'lint',
    'todo': 'find-todo', 'scan-todo': 'find-todo',
    'api': 'extract-api', 'routes': 'extract-api',
    'loc': 'count-lines', 'stats': 'count-lines', 'wc': 'count-lines',
    'log': 'git-log', 'git-log-short': lambda a: (a.__setitem__('format','short'), cmd_git_log(a))[1],
    'branch': 'git-branch', 'branches': 'git-branch',
    'grep': 'search-code', 'rg': 'search-code',
    'detect': 'detect-lang', 'language': 'detect-lang',
    'imports': 'check-imports', 'deps': 'check-imports',
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
