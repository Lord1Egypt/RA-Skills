#!/usr/bin/env python3
"""Dockerignore Linter — lint, audit, and optimize .dockerignore files.

Pure Python stdlib. No dependencies.
"""
import sys, os, re, json, argparse, fnmatch
from pathlib import Path

# ---------------------------------------------------------------------------
# Issue model
# ---------------------------------------------------------------------------

class Issue:
    def __init__(self, rule, severity, message, line=0):
        self.rule = rule
        self.severity = severity
        self.message = message
        self.line = line

    def to_dict(self):
        return {'rule': self.rule, 'severity': self.severity,
                'message': self.message, 'line': self.line}

# ---------------------------------------------------------------------------
# Known patterns by category
# ---------------------------------------------------------------------------

SECURITY_PATTERNS = {
    '.env': ('missing-env', '`.env` not excluded — may contain secrets'),
    '.env.*': ('missing-env', '`.env.*` not excluded — may contain environment-specific secrets'),
    '*.pem': ('missing-secrets', '`*.pem` not excluded — may contain private keys'),
    '*.key': ('missing-secrets', '`*.key` not excluded — may contain private keys'),
    'id_rsa': ('missing-secrets', '`id_rsa` not excluded — SSH private key'),
    '.ssh': ('missing-secrets', '`.ssh` not excluded — SSH config and keys'),
    '.git': ('missing-git', '`.git` not excluded — exposes repo history and potential secrets'),
    '.gitconfig': ('missing-git', '`.gitconfig` not excluded'),
    '*.p12': ('missing-secrets', '`*.p12` not excluded — certificate file'),
    '*.pfx': ('missing-secrets', '`*.pfx` not excluded — certificate file'),
    '.npmrc': ('missing-credentials', '`.npmrc` not excluded — may contain auth tokens'),
    '.pypirc': ('missing-credentials', '`.pypirc` not excluded — may contain PyPI credentials'),
    'credentials': ('missing-credentials', '`credentials` not excluded — may contain cloud credentials'),
    '.aws': ('missing-credentials', '`.aws` not excluded — AWS credentials directory'),
    '.gcloud': ('missing-credentials', '`.gcloud` not excluded — Google Cloud credentials'),
    'docker-compose*.yml': ('missing-docker', '`docker-compose*.yml` not excluded'),
    'docker-compose*.yaml': ('missing-docker', '`docker-compose*.yaml` not excluded'),
}

OPTIMIZATION_PATTERNS = {
    'node_modules': ('missing-deps', '`node_modules` not excluded — large dependency directory'),
    '__pycache__': ('missing-deps', '`__pycache__` not excluded — Python bytecode cache'),
    '.venv': ('missing-deps', '`.venv` not excluded — Python virtual environment'),
    'venv': ('missing-deps', '`venv` not excluded — Python virtual environment'),
    'vendor': ('missing-deps', '`vendor` not excluded — vendored dependencies'),
    'target': ('missing-deps', '`target` not excluded — Rust/Java build output'),
    '*.pyc': ('missing-build', '`*.pyc` not excluded — Python bytecode'),
    '*.o': ('missing-build', '`*.o` not excluded — compiled object files'),
    '*.class': ('missing-build', '`*.class` not excluded — Java class files'),
    'dist': ('missing-build', '`dist` not excluded — build output'),
    'build': ('missing-build', '`build` not excluded — build output'),
    '*.log': ('missing-logs', '`*.log` not excluded — log files'),
    'logs': ('missing-logs', '`logs/` not excluded — log directory'),
    'coverage': ('missing-test', '`coverage` not excluded — test coverage data'),
    '.nyc_output': ('missing-test', '`.nyc_output` not excluded — NYC coverage output'),
    'htmlcov': ('missing-test', '`htmlcov` not excluded — Python coverage HTML'),
    '.coverage': ('missing-test', '`.coverage` not excluded — Python coverage data'),
}

IDE_PATTERNS = {
    '.vscode': ('missing-ide', '`.vscode` not excluded — IDE config'),
    '.idea': ('missing-ide', '`.idea` not excluded — JetBrains IDE config'),
    '*.swp': ('missing-ide', '`*.swp` not excluded — Vim swap files'),
    '*.swo': ('missing-ide', '`*.swo` not excluded — Vim swap files'),
    '.DS_Store': ('missing-ide', '`.DS_Store` not excluded — macOS metadata'),
    'Thumbs.db': ('missing-ide', '`Thumbs.db` not excluded — Windows metadata'),
}

PROJECT_TEMPLATES = {
    'node': [
        'node_modules', 'npm-debug.log*', '.npm', '.env', '.env.*',
        'dist', 'build', 'coverage', '.nyc_output', '*.log',
        '.git', '.gitignore', '.vscode', '.idea', '*.swp',
        'docker-compose*.yml', 'Dockerfile*', '.dockerignore',
        '*.pem', '*.key', '.npmrc', '.DS_Store', 'Thumbs.db',
        '*.md', 'LICENSE', '.editorconfig', '.eslintrc*', '.prettierrc*',
        'tests', '__tests__', '*.test.js', '*.spec.js',
    ],
    'python': [
        '__pycache__', '*.pyc', '*.pyo', '.venv', 'venv', '.env', '.env.*',
        'dist', 'build', '*.egg-info', '.eggs', 'htmlcov', '.coverage',
        '.git', '.gitignore', '.vscode', '.idea', '*.swp',
        'docker-compose*.yml', 'Dockerfile*', '.dockerignore',
        '*.pem', '*.key', '.pypirc', '.DS_Store', 'Thumbs.db',
        '*.md', 'LICENSE', '.editorconfig', '.mypy_cache', '.pytest_cache',
        '.tox', '.nox', 'tests', '*.log',
    ],
    'go': [
        'vendor', '.env', '.env.*', '*.test', 'coverage.out',
        '.git', '.gitignore', '.vscode', '.idea', '*.swp',
        'docker-compose*.yml', 'Dockerfile*', '.dockerignore',
        '*.pem', '*.key', '.DS_Store', 'Thumbs.db',
        '*.md', 'LICENSE', '.editorconfig', '*.log',
    ],
    'rust': [
        'target', '.env', '.env.*', '*.log',
        '.git', '.gitignore', '.vscode', '.idea', '*.swp',
        'docker-compose*.yml', 'Dockerfile*', '.dockerignore',
        '*.pem', '*.key', '.DS_Store', 'Thumbs.db',
        '*.md', 'LICENSE', '.editorconfig',
    ],
    'java': [
        'target', 'build', '.gradle', '*.class', '*.jar', '*.war',
        '.env', '.env.*', '*.log', 'logs',
        '.git', '.gitignore', '.vscode', '.idea', '*.swp',
        'docker-compose*.yml', 'Dockerfile*', '.dockerignore',
        '*.pem', '*.key', '.DS_Store', 'Thumbs.db',
        '*.md', 'LICENSE', '.editorconfig',
    ],
    'ruby': [
        'vendor/bundle', '.bundle', '.env', '.env.*', '*.log', 'log',
        'coverage', 'tmp', 'pkg',
        '.git', '.gitignore', '.vscode', '.idea', '*.swp',
        'docker-compose*.yml', 'Dockerfile*', '.dockerignore',
        '*.pem', '*.key', '.DS_Store', 'Thumbs.db',
        '*.md', 'LICENSE', '.editorconfig',
    ],
    'generic': [
        '.git', '.gitignore', '.env', '.env.*',
        '*.log', 'logs', '.vscode', '.idea', '*.swp',
        '.DS_Store', 'Thumbs.db',
        'docker-compose*.yml', 'Dockerfile*', '.dockerignore',
        '*.pem', '*.key', '*.p12', '*.pfx',
        '.npmrc', '.pypirc', 'credentials',
        '*.md', 'LICENSE',
    ],
}


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_dockerignore(text):
    """Parse .dockerignore into list of (line_num, pattern, is_negation, raw)."""
    entries = []
    for i, line in enumerate(text.splitlines()):
        raw = line
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        is_negation = stripped.startswith('!')
        pattern = stripped[1:] if is_negation else stripped
        entries.append({
            'line': i + 1,
            'pattern': pattern,
            'negation': is_negation,
            'raw': raw,
        })
    return entries


def pattern_matches(pattern, target):
    """Check if a dockerignore pattern matches a target pattern."""
    if pattern == target:
        return True
    # handle ** prefix
    if pattern.startswith('**/'):
        pattern = pattern[3:]
    if target.startswith('**/'):
        target = target[3:]
    # strip trailing slashes
    pattern = pattern.rstrip('/')
    target = target.rstrip('/')
    if pattern == target:
        return True
    try:
        return fnmatch.fnmatch(target, pattern) or fnmatch.fnmatch(target, f'**/{pattern}')
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Linters
# ---------------------------------------------------------------------------

def lint_syntax(entries, raw_text):
    """Rules 1-4: syntax checks."""
    issues = []

    if not entries:
        issues.append(Issue('empty-file', 'warning', '.dockerignore is empty', 1))
        return issues

    seen = {}
    for entry in entries:
        pat = entry['pattern']

        # duplicate
        key = pat.rstrip('/')
        if key in seen:
            issues.append(Issue('duplicate-pattern', 'info',
                f'Duplicate pattern `{pat}` (first at line {seen[key]})', entry['line']))
        else:
            seen[key] = entry['line']

        # negation conflict check
        if entry['negation']:
            # check if the negated pattern was previously excluded
            for prev in entries:
                if prev['line'] >= entry['line']:
                    break
                if not prev['negation'] and pattern_matches(prev['pattern'], pat):
                    issues.append(Issue('negation-conflict', 'info',
                        f'Negation `!{pat}` overrides exclusion of `{prev["pattern"]}` — ensure this is intentional',
                        entry['line']))
                    break

    return issues


def lint_security(entries):
    """Rules 5-10: security checks."""
    issues = []
    excluded = set()
    for entry in entries:
        if not entry['negation']:
            excluded.add(entry['pattern'].rstrip('/'))

    for target, (rule, msg) in SECURITY_PATTERNS.items():
        matched = False
        for excl in excluded:
            if pattern_matches(excl, target):
                matched = True
                break
        if not matched:
            issues.append(Issue(rule, 'warning', msg))

    # also check IDE
    for target, (rule, msg) in IDE_PATTERNS.items():
        matched = False
        for excl in excluded:
            if pattern_matches(excl, target):
                matched = True
                break
        if not matched:
            issues.append(Issue(rule, 'info', msg))

    return issues


def lint_optimization(entries):
    """Rules 11-14: optimization checks."""
    issues = []
    excluded = set()
    for entry in entries:
        if not entry['negation']:
            excluded.add(entry['pattern'].rstrip('/'))

    for target, (rule, msg) in OPTIMIZATION_PATTERNS.items():
        matched = False
        for excl in excluded:
            if pattern_matches(excl, target):
                matched = True
                break
        if not matched:
            issues.append(Issue(rule, 'info', msg))

    return issues


def lint_best_practices(entries, raw_lines):
    """Rules 15-18: best practice checks."""
    issues = []

    for entry in entries:
        pat = entry['pattern']
        raw = entry['raw']

        # too broad
        if pat == '*' and not entry['negation']:
            issues.append(Issue('too-broad', 'warning',
                'Pattern `*` excludes everything — use specific patterns or add `!` negations',
                entry['line']))

        # inline comment (# after pattern)
        if ' #' in raw and not raw.strip().startswith('#'):
            issues.append(Issue('commented-pattern', 'warning',
                f'Inline comment detected — .dockerignore treats `#` as literal after pattern start',
                entry['line']))

        # trailing space
        if raw.rstrip('\n\r') != raw.rstrip():
            pass  # already stripped
        if entry['raw'].endswith(' ') or entry['raw'].endswith('\t'):
            issues.append(Issue('trailing-space', 'info',
                f'Pattern on line {entry["line"]} has trailing whitespace',
                entry['line']))

        # readme excluded
        lower = pat.lower().rstrip('/')
        if lower in ('readme.md', 'readme', 'readme.rst', 'docs', 'doc') and not entry['negation']:
            issues.append(Issue('readme-excluded', 'info',
                f'`{pat}` is excluded — docs are usually harmless in images and useful for debugging',
                entry['line']))

    return issues


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_lint(filepath, strict=False, fmt='text'):
    text = Path(filepath).read_text(encoding='utf-8', errors='replace')
    entries = parse_dockerignore(text)
    lines = text.splitlines()

    issues = []
    issues.extend(lint_syntax(entries, text))
    issues.extend(lint_security(entries))
    issues.extend(lint_optimization(entries))
    issues.extend(lint_best_practices(entries, lines))

    output_issues(filepath, issues, fmt)
    return exit_code(issues, strict)


def cmd_security(filepath, fmt='text'):
    text = Path(filepath).read_text(encoding='utf-8', errors='replace')
    entries = parse_dockerignore(text)
    issues = lint_security(entries)
    output_issues(filepath, issues, fmt)
    return exit_code(issues, False)


def cmd_suggest(project_type='generic', fmt='text'):
    patterns = PROJECT_TEMPLATES.get(project_type, PROJECT_TEMPLATES['generic'])
    if fmt == 'json':
        print(json.dumps({'project_type': project_type, 'patterns': patterns}, indent=2))
    else:
        print(f'# .dockerignore for {project_type} project')
        print(f'# Generated by dockerignore-linter\n')
        categories = {
            'deps': '# Dependencies',
            'build': '# Build output',
            'env': '# Environment & secrets',
            'vcs': '# Version control',
            'ide': '# IDE & editor',
            'docker': '# Docker',
            'misc': '# Other',
        }
        for pat in patterns:
            print(pat)
    return 0


def cmd_context(directory, dockerignore=None, fmt='text'):
    dirpath = Path(directory)
    if not dirpath.is_dir():
        print(f'Error: {directory} is not a directory', file=sys.stderr)
        return 1

    # find .dockerignore
    di_path = Path(dockerignore) if dockerignore else dirpath / '.dockerignore'
    exclude_patterns = []
    if di_path.exists():
        text = di_path.read_text(encoding='utf-8', errors='replace')
        entries = parse_dockerignore(text)
        exclude_patterns = [(e['pattern'], e['negation']) for e in entries]

    # walk directory
    included = []
    excluded_files = []
    total_size = 0
    excluded_size = 0

    for root, dirs, files in os.walk(directory):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, directory)
            try:
                size = os.path.getsize(full)
            except OSError:
                size = 0

            is_excluded = False
            for pat, neg in exclude_patterns:
                if neg:
                    if _matches(rel, pat):
                        is_excluded = False
                elif _matches(rel, pat):
                    is_excluded = True

            if is_excluded:
                excluded_files.append((rel, size))
                excluded_size += size
            else:
                included.append((rel, size))
                total_size += size

    if fmt == 'json':
        print(json.dumps({
            'directory': str(directory),
            'included_count': len(included),
            'included_size': total_size,
            'excluded_count': len(excluded_files),
            'excluded_size': excluded_size,
            'top_included': sorted(included, key=lambda x: -x[1])[:20],
        }, indent=2))
    else:
        print(f'Docker build context: {directory}')
        print(f'  Included: {len(included)} files ({_human_size(total_size)})')
        print(f'  Excluded: {len(excluded_files)} files ({_human_size(excluded_size)})')
        print(f'\nTop 20 largest included files:')
        for rel, size in sorted(included, key=lambda x: -x[1])[:20]:
            print(f'  {_human_size(size):>10s}  {rel}')

    return 0


def _matches(path, pattern):
    """Check if path matches dockerignore pattern."""
    parts = path.replace('\\', '/').split('/')
    pattern = pattern.rstrip('/')
    # direct match
    if fnmatch.fnmatch(path, pattern):
        return True
    # match any component
    for part in parts:
        if fnmatch.fnmatch(part, pattern):
            return True
    # match with **/ prefix
    if fnmatch.fnmatch(path, f'**/{pattern}'):
        return True
    return False


def _human_size(size):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if size < 1024:
            return f'{size:.1f} {unit}'
        size /= 1024
    return f'{size:.1f} TB'


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def output_issues(filepath, issues, fmt):
    if fmt == 'json':
        print(json.dumps({
            'file': str(filepath),
            'issues': [i.to_dict() for i in issues],
            'summary': {
                'errors': sum(1 for i in issues if i.severity == 'error'),
                'warnings': sum(1 for i in issues if i.severity == 'warning'),
                'info': sum(1 for i in issues if i.severity == 'info'),
            }
        }, indent=2))
    elif fmt == 'markdown':
        print(f'## {filepath}\n')
        print('| Severity | Rule | Line | Message |')
        print('|----------|------|------|---------|')
        for iss in sorted(issues, key=lambda x: x.line):
            sev = {'error': ':red_circle:', 'warning': ':warning:', 'info': ':information_source:'}.get(iss.severity, '')
            print(f'| {sev} {iss.severity} | `{iss.rule}` | {iss.line} | {iss.message} |')
        errs = sum(1 for i in issues if i.severity == 'error')
        warns = sum(1 for i in issues if i.severity == 'warning')
        infos = sum(1 for i in issues if i.severity == 'info')
        print(f'\n**{len(issues)} issues** ({errs} errors, {warns} warnings, {infos} info)')
    else:
        for iss in sorted(issues, key=lambda x: x.line):
            ln = f':{iss.line}' if iss.line else ''
            print(f'{filepath}{ln} {iss.severity} [{iss.rule}] {iss.message}')
        errs = sum(1 for i in issues if i.severity == 'error')
        warns = sum(1 for i in issues if i.severity == 'warning')
        print(f'\n{len(issues)} issues ({errs} errors, {warns} warnings)')


def exit_code(issues, strict=False):
    if any(i.severity == 'error' for i in issues):
        return 1
    if strict and any(i.severity == 'warning' for i in issues):
        return 1
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Dockerignore Linter')
    sub = parser.add_subparsers(dest='command', required=True)

    p_lint = sub.add_parser('lint', help='Lint .dockerignore (all rules)')
    p_lint.add_argument('file', help='Path to .dockerignore')
    p_lint.add_argument('--strict', action='store_true')
    p_lint.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    p_sec = sub.add_parser('security', help='Security audit')
    p_sec.add_argument('file', help='Path to .dockerignore')
    p_sec.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    p_sug = sub.add_parser('suggest', help='Suggest patterns for project type')
    p_sug.add_argument('--project-type', choices=['node', 'python', 'go', 'rust', 'java', 'ruby', 'generic'], default='generic')
    p_sug.add_argument('--format', choices=['text', 'json'], default='text')

    p_ctx = sub.add_parser('context', help='Analyze Docker build context')
    p_ctx.add_argument('directory', help='Project directory')
    p_ctx.add_argument('--dockerignore', help='Path to .dockerignore (default: <dir>/.dockerignore)')
    p_ctx.add_argument('--format', choices=['text', 'json'], default='text')

    args = parser.parse_args()
    fmt = getattr(args, 'format', 'text')

    if args.command == 'lint':
        sys.exit(cmd_lint(args.file, args.strict, fmt))
    elif args.command == 'security':
        sys.exit(cmd_security(args.file, fmt))
    elif args.command == 'suggest':
        sys.exit(cmd_suggest(args.project_type, fmt))
    elif args.command == 'context':
        sys.exit(cmd_context(args.directory, args.dockerignore, fmt))


if __name__ == '__main__':
    main()
