#!/usr/bin/env python3
"""
Codebase Stats — Project metrics, complexity analysis, and health indicators.

Analyzes: lines of code, file counts, language distribution, function complexity,
code-to-comment ratio, test coverage indicators, dependency counts, and tech debt signals.

No external dependencies — pure Python stdlib.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


# Language detection by extension
LANG_MAP = {
    '.py': 'Python', '.pyw': 'Python',
    '.js': 'JavaScript', '.mjs': 'JavaScript', '.cjs': 'JavaScript',
    '.ts': 'TypeScript', '.tsx': 'TypeScript', '.jsx': 'JavaScript',
    '.java': 'Java',
    '.go': 'Go',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.c': 'C', '.h': 'C',
    '.cpp': 'C++', '.cc': 'C++', '.cxx': 'C++', '.hpp': 'C++',
    '.cs': 'C#',
    '.swift': 'Swift',
    '.kt': 'Kotlin', '.kts': 'Kotlin',
    '.scala': 'Scala',
    '.r': 'R', '.R': 'R',
    '.lua': 'Lua',
    '.pl': 'Perl', '.pm': 'Perl',
    '.sh': 'Shell', '.bash': 'Shell', '.zsh': 'Shell',
    '.sql': 'SQL',
    '.html': 'HTML', '.htm': 'HTML',
    '.css': 'CSS', '.scss': 'SCSS', '.less': 'LESS',
    '.json': 'JSON',
    '.yaml': 'YAML', '.yml': 'YAML',
    '.toml': 'TOML',
    '.xml': 'XML',
    '.md': 'Markdown', '.mdx': 'Markdown',
    '.vue': 'Vue',
    '.svelte': 'Svelte',
    '.dart': 'Dart',
    '.ex': 'Elixir', '.exs': 'Elixir',
    '.erl': 'Erlang',
    '.zig': 'Zig',
    '.nim': 'Nim',
    '.v': 'V',
    '.sol': 'Solidity',
    '.tf': 'Terraform', '.hcl': 'HCL',
    '.proto': 'Protobuf',
}

# Directories to skip
SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', '.next', '.nuxt', 'dist', 'build',
    'target', 'vendor', '.venv', 'venv', 'env', '.env', '.tox', '.mypy_cache',
    '.pytest_cache', 'coverage', '.coverage', 'htmlcov', '.idea', '.vscode',
    'bin', 'obj', '.gradle', '.cache', 'tmp', '.tmp',
}

# Comment patterns per language
COMMENT_PATTERNS = {
    'Python': (r'^\s*#', r'"""', r"'''"),
    'JavaScript': (r'^\s*//', r'/\*', r'\*/'),
    'TypeScript': (r'^\s*//', r'/\*', r'\*/'),
    'Java': (r'^\s*//', r'/\*', r'\*/'),
    'Go': (r'^\s*//', r'/\*', r'\*/'),
    'Rust': (r'^\s*//', r'/\*', r'\*/'),
    'Ruby': (r'^\s*#', r'=begin', r'=end'),
    'PHP': (r'^\s*(//|#)', r'/\*', r'\*/'),
    'C': (r'^\s*//', r'/\*', r'\*/'),
    'C++': (r'^\s*//', r'/\*', r'\*/'),
    'C#': (r'^\s*//', r'/\*', r'\*/'),
    'Shell': (r'^\s*#', None, None),
    'SQL': (r'^\s*--', r'/\*', r'\*/'),
}

# Function definition patterns
FUNC_PATTERNS = {
    'Python': r'^\s*def\s+(\w+)',
    'JavaScript': r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
    'TypeScript': r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
    'Java': r'(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+(\w+)\s*\(',
    'Go': r'^func\s+(?:\([^)]+\)\s+)?(\w+)',
    'Rust': r'^(?:pub\s+)?fn\s+(\w+)',
    'Ruby': r'^\s*def\s+(\w+)',
    'PHP': r'(?:public|private|protected|static|\s)*function\s+(\w+)',
    'C': r'^[\w\s\*]+\s+(\w+)\s*\([^;]*$',
    'C++': r'^[\w\s\*:]+\s+(\w+)\s*\([^;]*$',
    'C#': r'(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+(\w+)\s*\(',
}


def should_skip(path):
    """Check if path should be skipped."""
    parts = Path(path).parts
    return any(p in SKIP_DIRS for p in parts)


def get_language(filepath):
    """Detect language from file extension."""
    ext = Path(filepath).suffix.lower()
    return LANG_MAP.get(ext)


def count_lines(filepath, lang):
    """Count code lines, comment lines, and blank lines."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except (OSError, PermissionError):
        return 0, 0, 0

    code = 0
    comments = 0
    blank = 0
    in_block = False

    patterns = COMMENT_PATTERNS.get(lang, (None, None, None))
    line_pat, block_start, block_end = patterns

    for line in lines:
        stripped = line.strip()

        if not stripped:
            blank += 1
            continue

        if in_block:
            comments += 1
            if block_end and re.search(block_end, stripped):
                in_block = False
            continue

        if block_start and re.search(block_start, stripped):
            comments += 1
            if block_end and not re.search(block_end, stripped):
                in_block = True
            continue

        if line_pat and re.match(line_pat, stripped):
            comments += 1
            continue

        code += 1

    return code, comments, blank


def analyze_complexity(filepath, lang):
    """Estimate function-level complexity (simplified cyclomatic)."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            lines = content.split('\n')
    except (OSError, PermissionError):
        return []

    func_pat = FUNC_PATTERNS.get(lang)
    if not func_pat:
        return []

    functions = []
    current_func = None
    func_start = 0
    indent_level = 0

    # Complexity keywords
    complexity_keywords = re.compile(
        r'\b(if|elif|else if|elseif|for|while|do|switch|case|catch|except|'
        r'&&|\|\||and |or |\?|ternary)\b'
    )

    for i, line in enumerate(lines):
        match = re.search(func_pat, line)
        if match:
            # Save previous function
            if current_func:
                functions.append(current_func)

            fname = next((g for g in match.groups() if g), 'anonymous')
            current_func = {
                'name': fname,
                'line': i + 1,
                'complexity': 1,  # Base complexity
                'length': 0,
            }
            func_start = i

        if current_func:
            current_func['length'] = i - func_start + 1
            # Count complexity keywords
            current_func['complexity'] += len(complexity_keywords.findall(line))

    if current_func:
        functions.append(current_func)

    return functions


def detect_test_files(root):
    """Detect test file patterns."""
    test_patterns = [
        r'test[_.]', r'[_.]test\.', r'spec[_.]', r'[_.]spec\.',
        r'__tests__', r'tests/', r'test/',
    ]
    test_files = 0
    total_files = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            lang = get_language(fname)
            if not lang or lang in ('JSON', 'YAML', 'TOML', 'XML', 'Markdown'):
                continue
            total_files += 1
            fp = os.path.join(dirpath, fname).lower()
            if any(re.search(p, fp) for p in test_patterns):
                test_files += 1

    return test_files, total_files


def detect_deps(root):
    """Count dependencies from common manifest files."""
    deps = {}

    # package.json
    pkg = os.path.join(root, 'package.json')
    if os.path.isfile(pkg):
        try:
            with open(pkg) as f:
                data = json.load(f)
            deps['npm'] = {
                'dependencies': len(data.get('dependencies', {})),
                'devDependencies': len(data.get('devDependencies', {})),
            }
        except (json.JSONDecodeError, OSError):
            pass

    # requirements.txt
    req = os.path.join(root, 'requirements.txt')
    if os.path.isfile(req):
        try:
            with open(req) as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
            deps['pip'] = {'packages': len(lines)}
        except OSError:
            pass

    # go.mod
    gomod = os.path.join(root, 'go.mod')
    if os.path.isfile(gomod):
        try:
            with open(gomod) as f:
                content = f.read()
            requires = re.findall(r'^\s+\S+', content, re.MULTILINE)
            deps['go'] = {'modules': len(requires)}
        except OSError:
            pass

    # Cargo.toml
    cargo = os.path.join(root, 'Cargo.toml')
    if os.path.isfile(cargo):
        try:
            with open(cargo) as f:
                content = f.read()
            in_deps = False
            count = 0
            for line in content.split('\n'):
                if re.match(r'\[.*dependencies.*\]', line):
                    in_deps = True
                    continue
                if line.startswith('['):
                    in_deps = False
                if in_deps and '=' in line:
                    count += 1
            deps['cargo'] = {'crates': count}
        except OSError:
            pass

    return deps


def detect_tech_debt(root, all_files_content):
    """Detect tech debt signals."""
    signals = []

    # TODO/FIXME/HACK/XXX counts
    todo_count = 0
    fixme_count = 0
    hack_count = 0

    for filepath, content in all_files_content.items():
        for line in content.split('\n'):
            upper = line.upper()
            if 'TODO' in upper:
                todo_count += 1
            if 'FIXME' in upper:
                fixme_count += 1
            if 'HACK' in upper or 'XXX' in upper:
                hack_count += 1

    if todo_count > 0:
        signals.append(f'{todo_count} TODOs')
    if fixme_count > 0:
        signals.append(f'{fixme_count} FIXMEs')
    if hack_count > 0:
        signals.append(f'{hack_count} HACKs/XXXs')

    return signals


def scan_project(root, max_files=10000):
    """Scan the project and collect all metrics."""
    stats = {
        'root': os.path.abspath(root),
        'languages': defaultdict(lambda: {'files': 0, 'code': 0, 'comments': 0, 'blank': 0}),
        'total_files': 0,
        'total_code': 0,
        'total_comments': 0,
        'total_blank': 0,
        'largest_files': [],
        'complex_functions': [],
        'file_count': 0,
    }

    all_content = {}
    file_sizes = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for fname in filenames:
            filepath = os.path.join(dirpath, fname)
            rel = os.path.relpath(filepath, root)

            if should_skip(rel):
                continue

            lang = get_language(fname)
            if not lang:
                continue

            stats['file_count'] += 1
            if stats['file_count'] > max_files:
                break

            code, comments, blank = count_lines(filepath, lang)
            total = code + comments + blank

            stats['languages'][lang]['files'] += 1
            stats['languages'][lang]['code'] += code
            stats['languages'][lang]['comments'] += comments
            stats['languages'][lang]['blank'] += blank

            stats['total_files'] += 1
            stats['total_code'] += code
            stats['total_comments'] += comments
            stats['total_blank'] += blank

            file_sizes.append((rel, total))

            # Read content for tech debt
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                all_content[rel] = content
            except (OSError, PermissionError):
                pass

            # Complexity analysis for code files
            if lang in FUNC_PATTERNS:
                funcs = analyze_complexity(filepath, lang)
                for func in funcs:
                    func['file'] = rel
                    stats['complex_functions'].append(func)

    # Top largest files
    file_sizes.sort(key=lambda x: x[1], reverse=True)
    stats['largest_files'] = file_sizes[:10]

    # Top complex functions
    stats['complex_functions'].sort(key=lambda x: x['complexity'], reverse=True)
    stats['complex_functions'] = stats['complex_functions'][:15]

    # Test coverage indicator
    test_files, source_files = detect_test_files(root)
    stats['test_files'] = test_files
    stats['source_files'] = source_files

    # Dependencies
    stats['dependencies'] = detect_deps(root)

    # Tech debt
    stats['tech_debt'] = detect_tech_debt(root, all_content)

    stats['scanned_at'] = datetime.now().isoformat()

    return stats


def format_terminal(stats):
    """Format stats for terminal output."""
    lines = []
    lines.append(f"\n{'='*65}")
    lines.append(f"  CODEBASE STATISTICS")
    lines.append(f"{'='*65}")
    lines.append(f"  Project: {stats['root']}")
    lines.append(f"  Files:   {stats['total_files']:,}")
    lines.append(f"  Code:    {stats['total_code']:,} lines")
    lines.append(f"  Comments:{stats['total_comments']:,} lines")
    lines.append(f"  Blank:   {stats['total_blank']:,} lines")
    total = stats['total_code'] + stats['total_comments'] + stats['total_blank']
    lines.append(f"  Total:   {total:,} lines")

    if stats['total_code'] > 0:
        ratio = stats['total_comments'] / stats['total_code'] * 100
        lines.append(f"  Comment ratio: {ratio:.1f}%")

    lines.append(f"\n  {'─'*50}")
    lines.append(f"  LANGUAGES")
    lines.append(f"  {'─'*50}")

    sorted_langs = sorted(stats['languages'].items(), key=lambda x: x[1]['code'], reverse=True)
    for lang, data in sorted_langs[:15]:
        pct = (data['code'] / stats['total_code'] * 100) if stats['total_code'] > 0 else 0
        bar_len = int(pct / 3)
        bar = '█' * bar_len
        lines.append(f"  {lang:<15} {data['code']:>8,} lines  {data['files']:>4} files  {pct:5.1f}% {bar}")

    if stats['complex_functions']:
        lines.append(f"\n  {'─'*50}")
        lines.append(f"  MOST COMPLEX FUNCTIONS")
        lines.append(f"  {'─'*50}")
        for func in stats['complex_functions'][:10]:
            lines.append(f"  {func['name']:<30} complexity:{func['complexity']:>3}  lines:{func['length']:>4}  {func['file']}:{func['line']}")

    if stats['largest_files']:
        lines.append(f"\n  {'─'*50}")
        lines.append(f"  LARGEST FILES")
        lines.append(f"  {'─'*50}")
        for fname, size in stats['largest_files']:
            lines.append(f"  {size:>6,} lines  {fname}")

    # Test coverage indicator
    if stats['source_files'] > 0:
        lines.append(f"\n  {'─'*50}")
        lines.append(f"  TEST COVERAGE INDICATOR")
        lines.append(f"  {'─'*50}")
        ratio = (stats['test_files'] / stats['source_files'] * 100) if stats['source_files'] > 0 else 0
        lines.append(f"  Test files: {stats['test_files']} / {stats['source_files']} source files ({ratio:.0f}%)")

    # Dependencies
    if stats['dependencies']:
        lines.append(f"\n  {'─'*50}")
        lines.append(f"  DEPENDENCIES")
        lines.append(f"  {'─'*50}")
        for mgr, counts in stats['dependencies'].items():
            parts = ', '.join(f'{k}: {v}' for k, v in counts.items())
            lines.append(f"  {mgr}: {parts}")

    # Tech debt
    if stats['tech_debt']:
        lines.append(f"\n  {'─'*50}")
        lines.append(f"  TECH DEBT SIGNALS")
        lines.append(f"  {'─'*50}")
        for signal in stats['tech_debt']:
            lines.append(f"  - {signal}")

    lines.append(f"\n{'='*65}")
    return '\n'.join(lines)


def format_markdown(stats):
    """Format stats as markdown."""
    lines = []
    lines.append('# Codebase Statistics\n')

    total = stats['total_code'] + stats['total_comments'] + stats['total_blank']
    ratio = (stats['total_comments'] / stats['total_code'] * 100) if stats['total_code'] > 0 else 0

    lines.append('| Metric | Value |')
    lines.append('|--------|-------|')
    lines.append(f'| Files | {stats["total_files"]:,} |')
    lines.append(f'| Code Lines | {stats["total_code"]:,} |')
    lines.append(f'| Comment Lines | {stats["total_comments"]:,} |')
    lines.append(f'| Blank Lines | {stats["total_blank"]:,} |')
    lines.append(f'| Total Lines | {total:,} |')
    lines.append(f'| Comment Ratio | {ratio:.1f}% |')
    lines.append('')

    lines.append('## Language Distribution\n')
    lines.append('| Language | Code Lines | Files | % |')
    lines.append('|----------|-----------|-------|---|')
    sorted_langs = sorted(stats['languages'].items(), key=lambda x: x[1]['code'], reverse=True)
    for lang, data in sorted_langs[:15]:
        pct = (data['code'] / stats['total_code'] * 100) if stats['total_code'] > 0 else 0
        lines.append(f'| {lang} | {data["code"]:,} | {data["files"]} | {pct:.1f}% |')
    lines.append('')

    if stats['complex_functions']:
        lines.append('## Most Complex Functions\n')
        lines.append('| Function | Complexity | Lines | File |')
        lines.append('|----------|-----------|-------|------|')
        for func in stats['complex_functions'][:10]:
            lines.append(f'| `{func["name"]}` | {func["complexity"]} | {func["length"]} | `{func["file"]}:{func["line"]}` |')
        lines.append('')

    if stats['largest_files']:
        lines.append('## Largest Files\n')
        lines.append('| Lines | File |')
        lines.append('|-------|------|')
        for fname, size in stats['largest_files']:
            lines.append(f'| {size:,} | `{fname}` |')
        lines.append('')

    if stats['tech_debt']:
        lines.append('## Tech Debt Signals\n')
        for signal in stats['tech_debt']:
            lines.append(f'- {signal}')
        lines.append('')

    return '\n'.join(lines)


def format_json_output(stats):
    """Format as JSON."""
    output = {
        'root': stats['root'],
        'total_files': stats['total_files'],
        'total_code': stats['total_code'],
        'total_comments': stats['total_comments'],
        'total_blank': stats['total_blank'],
        'comment_ratio': round(stats['total_comments'] / max(stats['total_code'], 1) * 100, 1),
        'languages': dict(stats['languages']),
        'largest_files': [{'file': f, 'lines': s} for f, s in stats['largest_files']],
        'complex_functions': stats['complex_functions'][:10],
        'test_files': stats['test_files'],
        'source_files': stats['source_files'],
        'dependencies': stats['dependencies'],
        'tech_debt': stats['tech_debt'],
        'scanned_at': stats['scanned_at'],
    }
    return json.dumps(output, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='Codebase Stats — project metrics, complexity analysis, and health indicators'
    )
    parser.add_argument('path', nargs='?', default='.',
                        help='Path to project root (default: current directory)')
    parser.add_argument('--format', '-f', choices=['terminal', 'markdown', 'json'],
                        default='terminal', help='Output format (default: terminal)')
    parser.add_argument('--output', '-o', help='Write report to file')
    parser.add_argument('--max-files', type=int, default=10000,
                        help='Maximum files to scan (default: 10000)')
    parser.add_argument('--language', '-l',
                        help='Filter to specific language (e.g., Python, JavaScript)')

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    stats = scan_project(args.path, args.max_files)

    # Filter by language if specified
    if args.language:
        filtered = {k: v for k, v in stats['languages'].items()
                    if k.lower() == args.language.lower()}
        if not filtered:
            print(f"Language '{args.language}' not found in project", file=sys.stderr)
            sys.exit(1)
        stats['languages'] = defaultdict(lambda: {'files': 0, 'code': 0, 'comments': 0, 'blank': 0}, filtered)

    if args.format == 'terminal':
        output = format_terminal(stats)
    elif args.format == 'markdown':
        output = format_markdown(stats)
    else:
        output = format_json_output(stats)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
