#!/usr/bin/env python3
"""EditorConfig Linter — validate .editorconfig and check file compliance."""

import sys
import os
import re
import json
import fnmatch
from dataclasses import dataclass, field
from typing import Optional


# ── EditorConfig parser ─────────────────────────────────────────────

VALID_PROPERTIES = {
    'root', 'indent_style', 'indent_size', 'tab_width', 'end_of_line',
    'charset', 'trim_trailing_whitespace', 'insert_final_newline',
    'max_line_length',
}

VALID_VALUES = {
    'indent_style': {'tab', 'space'},
    'end_of_line': {'lf', 'crlf', 'cr'},
    'charset': {'utf-8', 'utf-8-bom', 'latin1', 'utf-16be', 'utf-16le'},
    'trim_trailing_whitespace': {'true', 'false'},
    'insert_final_newline': {'true', 'false'},
    'root': {'true', 'false'},
}


@dataclass
class EditorConfigSection:
    glob: str
    line: int
    properties: dict = field(default_factory=dict)


@dataclass
class Issue:
    severity: str
    message: str
    line: int = 0
    file: str = ""
    rule: str = ""
    fix: str = ""


def parse_editorconfig(filepath: str) -> tuple:
    """Parse .editorconfig file, return (sections, issues)."""
    sections = []
    issues = []
    current_section = None
    is_root = False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return [], [Issue('error', str(e), file=filepath)]

    for i, raw_line in enumerate(lines, 1):
        line = raw_line.strip()

        # Skip empty lines and comments
        if not line or line.startswith('#') or line.startswith(';'):
            continue

        # Section header
        m = re.match(r'^\[(.+)\]$', line)
        if m:
            glob_pattern = m.group(1).strip()
            current_section = EditorConfigSection(glob=glob_pattern, line=i)
            sections.append(current_section)
            continue

        # Property
        if '=' in line:
            key, _, value = line.partition('=')
            key = key.strip().lower()
            value = value.strip().lower()

            # root = true at top level
            if key == 'root' and current_section is None:
                is_root = value == 'true'
                continue

            if current_section is None:
                if key != 'root':
                    issues.append(Issue('warning', f"Property '{key}' outside of section",
                                       i, filepath, 'property-outside-section'))
                continue

            # Validate property name
            if key not in VALID_PROPERTIES:
                issues.append(Issue('warning', f"Unknown property: {key}",
                                   i, filepath, 'unknown-property'))

            # Validate property value
            if key in VALID_VALUES and value != 'unset':
                if value not in VALID_VALUES[key]:
                    issues.append(Issue('error',
                        f"Invalid value for {key}: '{value}' (valid: {', '.join(sorted(VALID_VALUES[key]))})",
                        i, filepath, 'invalid-value'))

            # indent_size validation
            if key == 'indent_size' and value not in ('tab', 'unset'):
                if not value.isdigit() or int(value) < 1 or int(value) > 16:
                    issues.append(Issue('error',
                        f"Invalid indent_size: '{value}' (expected 1-16 or 'tab')",
                        i, filepath, 'invalid-indent-size'))

            # tab_width validation
            if key == 'tab_width' and value != 'unset':
                if not value.isdigit() or int(value) < 1 or int(value) > 16:
                    issues.append(Issue('error',
                        f"Invalid tab_width: '{value}' (expected 1-16)",
                        i, filepath, 'invalid-tab-width'))

            # max_line_length validation
            if key == 'max_line_length' and value not in ('off', 'unset'):
                if not value.isdigit() or int(value) < 1:
                    issues.append(Issue('error',
                        f"Invalid max_line_length: '{value}'",
                        i, filepath, 'invalid-max-line-length'))

            current_section.properties[key] = value

    # Check for missing root = true
    if not is_root:
        issues.append(Issue('info', "Missing 'root = true' — editors will search parent directories",
                           0, filepath, 'missing-root'))

    # Check for duplicate sections
    seen_globs = {}
    for sec in sections:
        if sec.glob in seen_globs:
            issues.append(Issue('warning',
                f"Duplicate section [{sec.glob}] (first at line {seen_globs[sec.glob]})",
                sec.line, filepath, 'duplicate-section'))
        else:
            seen_globs[sec.glob] = sec.line

    return sections, issues


def glob_to_regex(pattern: str) -> str:
    """Convert EditorConfig glob to regex."""
    # EditorConfig uses a subset of glob patterns
    result = ''
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == '*':
            if i + 1 < len(pattern) and pattern[i + 1] == '*':
                result += '.*'
                i += 2
                if i < len(pattern) and pattern[i] == '/':
                    i += 1
            else:
                result += '[^/]*'
                i += 1
        elif c == '?':
            result += '[^/]'
            i += 1
        elif c == '{':
            j = pattern.index('}', i) if '}' in pattern[i:] else len(pattern)
            alternatives = pattern[i + 1:j].split(',')
            result += '(?:' + '|'.join(re.escape(a.strip()) for a in alternatives) + ')'
            i = j + 1
        elif c == '[':
            j = pattern.index(']', i) if ']' in pattern[i:] else len(pattern)
            result += pattern[i:j + 1]
            i = j + 1
        elif c in '.+^$|()\\':
            result += '\\' + c
            i += 1
        else:
            result += c
            i += 1
    return result


def match_file(filepath: str, sections: list) -> dict:
    """Get effective EditorConfig properties for a file."""
    props = {}
    basename = os.path.basename(filepath)

    for sec in sections:
        pattern = sec.glob
        # If no slash in pattern, match against basename only
        if '/' not in pattern:
            try:
                regex = glob_to_regex(pattern)
                if re.fullmatch(regex, basename):
                    props.update(sec.properties)
            except Exception:
                if fnmatch.fnmatch(basename, pattern):
                    props.update(sec.properties)
        else:
            try:
                regex = glob_to_regex(pattern)
                if re.fullmatch(regex, filepath) or re.search(regex, filepath):
                    props.update(sec.properties)
            except Exception:
                pass

    return props


# ── File compliance checking ────────────────────────────────────────

def check_file_compliance(filepath: str, props: dict) -> list:
    """Check a single file against EditorConfig properties."""
    issues = []

    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
    except Exception:
        return issues

    # Skip binary files
    if b'\x00' in raw[:8192]:
        return issues

    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError:
        if props.get('charset') == 'utf-8':
            issues.append(Issue('error', 'File is not valid UTF-8',
                               file=filepath, rule='charset'))
        return issues

    lines = content.split('\n')

    # charset check
    charset = props.get('charset')
    if charset == 'utf-8-bom':
        if not raw.startswith(b'\xef\xbb\xbf'):
            issues.append(Issue('warning', 'Missing UTF-8 BOM',
                               file=filepath, rule='charset',
                               fix='Add UTF-8 BOM at start of file'))
    elif charset == 'utf-8':
        if raw.startswith(b'\xef\xbb\xbf'):
            issues.append(Issue('warning', 'Unexpected UTF-8 BOM (charset=utf-8 means no BOM)',
                               file=filepath, rule='charset',
                               fix='Remove UTF-8 BOM'))

    # end_of_line check
    eol = props.get('end_of_line')
    if eol:
        if eol == 'lf' and b'\r\n' in raw:
            issues.append(Issue('warning', 'File uses CRLF but end_of_line=lf',
                               file=filepath, rule='end_of_line',
                               fix='Convert line endings to LF'))
        elif eol == 'crlf' and b'\r\n' not in raw and b'\n' in raw:
            issues.append(Issue('warning', 'File uses LF but end_of_line=crlf',
                               file=filepath, rule='end_of_line',
                               fix='Convert line endings to CRLF'))
        elif eol == 'cr' and b'\r\n' in raw:
            issues.append(Issue('warning', 'File uses CRLF but end_of_line=cr',
                               file=filepath, rule='end_of_line'))

    # trim_trailing_whitespace
    if props.get('trim_trailing_whitespace') == 'true':
        for i, line in enumerate(lines, 1):
            if line.rstrip() != line and line.rstrip('\r') != line.rstrip('\r').rstrip():
                stripped = line.rstrip('\r\n')
                if stripped != stripped.rstrip():
                    issues.append(Issue('warning', f'Trailing whitespace on line {i}',
                                       i, filepath, 'trim_trailing_whitespace'))
                    if len(issues) > 50:
                        issues.append(Issue('info', '...truncated (>50 trailing whitespace violations)',
                                           file=filepath, rule='trim_trailing_whitespace'))
                        break

    # insert_final_newline
    if props.get('insert_final_newline') == 'true':
        if content and not content.endswith('\n'):
            issues.append(Issue('warning', 'Missing final newline',
                               file=filepath, rule='insert_final_newline',
                               fix='Add newline at end of file'))
    elif props.get('insert_final_newline') == 'false':
        if content and content.endswith('\n'):
            issues.append(Issue('info', 'File ends with newline but insert_final_newline=false',
                               file=filepath, rule='insert_final_newline'))

    # indent_style
    indent_style = props.get('indent_style')
    indent_size = props.get('indent_size')
    if indent_style:
        tab_lines = 0
        space_lines = 0
        wrong_indent = 0
        for i, line in enumerate(lines, 1):
            if not line.strip():
                continue
            leading = line[:len(line) - len(line.lstrip())]
            if not leading:
                continue
            if '\t' in leading:
                tab_lines += 1
            if ' ' in leading and '\t' not in leading:
                space_lines += 1
            # Mixed indentation on same line
            if '\t' in leading and ' ' in leading:
                # Allow spaces after tabs (alignment)
                stripped_tabs = leading.lstrip('\t')
                if '\t' in stripped_tabs:
                    wrong_indent += 1

        if indent_style == 'space' and tab_lines > 0:
            issues.append(Issue('warning',
                f'{tab_lines} line(s) use tab indentation but indent_style=space',
                file=filepath, rule='indent_style'))
        elif indent_style == 'tab' and space_lines > 0 and tab_lines == 0:
            issues.append(Issue('warning',
                f'{space_lines} line(s) use space indentation but indent_style=tab',
                file=filepath, rule='indent_style'))

        if wrong_indent > 0:
            issues.append(Issue('warning',
                f'{wrong_indent} line(s) have mixed tabs and spaces',
                file=filepath, rule='mixed-indentation'))

    # max_line_length
    max_len = props.get('max_line_length')
    if max_len and max_len != 'off':
        try:
            limit = int(max_len)
            long_lines = []
            for i, line in enumerate(lines, 1):
                stripped = line.rstrip('\r\n')
                if len(stripped) > limit:
                    long_lines.append(i)
            if long_lines:
                if len(long_lines) <= 5:
                    for ln in long_lines:
                        issues.append(Issue('warning',
                            f'Line {ln} exceeds max_line_length ({limit})',
                            ln, filepath, 'max_line_length'))
                else:
                    issues.append(Issue('warning',
                        f'{len(long_lines)} lines exceed max_line_length ({limit})',
                        file=filepath, rule='max_line_length'))
        except ValueError:
            pass

    return issues


# ── File discovery ──────────────────────────────────────────────────

DEFAULT_EXCLUDES = {
    '.git', 'node_modules', '__pycache__', '.venv', 'venv',
    '.tox', '.eggs', '*.egg-info', 'dist', 'build', '.cache',
    '.mypy_cache', '.pytest_cache', 'coverage', '.next', '.nuxt',
}

CHECKABLE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.css', '.scss', '.less',
    '.html', '.htm', '.xml', '.json', '.yaml', '.yml', '.toml',
    '.md', '.rst', '.txt', '.cfg', '.ini', '.conf',
    '.sh', '.bash', '.zsh', '.fish',
    '.java', '.kt', '.scala', '.go', '.rs', '.c', '.h', '.cpp', '.hpp',
    '.rb', '.php', '.pl', '.lua', '.r', '.R',
    '.swift', '.m', '.cs', '.fs', '.vb',
    '.sql', '.graphql', '.proto',
    '.vue', '.svelte', '.astro',
    '.tf', '.hcl',
    '.dockerfile', '.editorconfig', '.gitignore', '.gitattributes',
    '.env', '.env.example',
}


def discover_files(path: str, excludes: set, max_files: int) -> list:
    """Discover checkable files in path."""
    files = []
    if os.path.isfile(path):
        return [path]

    for root, dirs, fnames in os.walk(path):
        # Filter excluded dirs
        dirs[:] = [d for d in dirs if d not in excludes and not d.startswith('.')]
        for fname in fnames:
            _, ext = os.path.splitext(fname)
            if ext.lower() in CHECKABLE_EXTENSIONS or fname in ('.editorconfig', 'Makefile', 'Dockerfile'):
                files.append(os.path.join(root, fname))
                if len(files) >= max_files:
                    return files
    return files


def find_editorconfig(start_path: str) -> Optional[str]:
    """Search for .editorconfig from start_path upward."""
    path = os.path.abspath(start_path)
    if os.path.isfile(path):
        path = os.path.dirname(path)

    while True:
        ec = os.path.join(path, '.editorconfig')
        if os.path.isfile(ec):
            return ec
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent


# ── Fix mode ────────────────────────────────────────────────────────

def fix_file(filepath: str, props: dict) -> list:
    """Fix EditorConfig violations in a file. Returns list of fixes applied."""
    fixes = []
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
    except Exception:
        return fixes

    if b'\x00' in raw[:8192]:
        return fixes

    modified = False

    # end_of_line fix
    eol = props.get('end_of_line')
    if eol:
        if eol == 'lf' and b'\r\n' in raw:
            raw = raw.replace(b'\r\n', b'\n')
            fixes.append('Converted CRLF to LF')
            modified = True
        elif eol == 'crlf' and b'\r\n' not in raw and b'\n' in raw:
            raw = raw.replace(b'\n', b'\r\n')
            fixes.append('Converted LF to CRLF')
            modified = True

    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError:
        return fixes

    # trim_trailing_whitespace
    if props.get('trim_trailing_whitespace') == 'true':
        new_lines = []
        changed = False
        for line in content.split('\n'):
            stripped = line.rstrip()
            if stripped != line.rstrip('\r'):
                changed = True
            new_lines.append(stripped)
        if changed:
            content = '\n'.join(new_lines)
            fixes.append('Trimmed trailing whitespace')
            modified = True

    # insert_final_newline
    if props.get('insert_final_newline') == 'true':
        if content and not content.endswith('\n'):
            content += '\n'
            fixes.append('Added final newline')
            modified = True

    # charset (BOM)
    charset = props.get('charset')
    if charset == 'utf-8':
        if content.startswith('\ufeff'):
            content = content[1:]
            fixes.append('Removed UTF-8 BOM')
            modified = True

    if modified:
        encoding = 'utf-8'
        if eol == 'crlf':
            raw_out = content.encode(encoding).replace(b'\n', b'\r\n')
        else:
            raw_out = content.encode(encoding)

        if charset == 'utf-8-bom':
            raw_out = b'\xef\xbb\xbf' + raw_out

        with open(filepath, 'wb') as f:
            f.write(raw_out)

    return fixes


# ── Output formatting ───────────────────────────────────────────────

def format_text(issues_by_file: dict, total_files: int) -> str:
    lines = []
    total_issues = 0

    for filepath, issues in sorted(issues_by_file.items()):
        if not issues:
            continue
        lines.append(f"\n📄 {filepath}")
        lines.append("─" * 60)
        for i in issues:
            icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[i.severity]
            loc = f"line {i.line}" if i.line else ""
            rule_str = f" [{i.rule}]" if i.rule else ""
            lines.append(f"  {icon} {i.message}{rule_str} {loc}")
            if i.fix:
                lines.append(f"     Fix: {i.fix}")
        total_issues += len(issues)

    if not total_issues:
        lines.append("✅ All files comply with EditorConfig rules")

    lines.append(f"\n{'═' * 60}")
    errors = sum(1 for issues in issues_by_file.values()
                 for i in issues if i.severity == 'error')
    warnings = sum(1 for issues in issues_by_file.values()
                   for i in issues if i.severity == 'warning')
    infos = sum(1 for issues in issues_by_file.values()
                for i in issues if i.severity == 'info')
    files_with_issues = sum(1 for issues in issues_by_file.values() if issues)
    lines.append(f"Checked {total_files} files, {files_with_issues} with issues")
    lines.append(f"Total: {errors} errors, {warnings} warnings, {infos} info")
    return '\n'.join(lines)


def format_json_output(issues_by_file: dict, total_files: int) -> str:
    output = {
        'total_files': total_files,
        'files': {}
    }
    for filepath, issues in sorted(issues_by_file.items()):
        if issues:
            output['files'][filepath] = [{
                'severity': i.severity,
                'message': i.message,
                'line': i.line,
                'rule': i.rule,
                'fix': i.fix
            } for i in issues]
    return json.dumps(output, indent=2)


def format_markdown(issues_by_file: dict, total_files: int) -> str:
    lines = ["# EditorConfig Compliance Report\n"]
    files_with_issues = sum(1 for issues in issues_by_file.values() if issues)
    lines.append(f"Checked **{total_files}** files, **{files_with_issues}** with issues.\n")

    for filepath, issues in sorted(issues_by_file.items()):
        if not issues:
            continue
        lines.append(f"## {filepath}\n")
        lines.append("| Severity | Rule | Message | Line |")
        lines.append("|----------|------|---------|------|")
        for i in issues:
            msg = i.message.replace('|', '\\|')
            lines.append(f"| {i.severity} | {i.rule} | {msg} | {i.line or '-'} |")
        lines.append("")

    return '\n'.join(lines)


# ── Main ────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print("Usage: editorconfig-linter.py <command> <path> [options]")
        print("\nCommands:")
        print("  validate  Validate .editorconfig syntax")
        print("  check     Check files against .editorconfig rules")
        print("  show      Show effective config for a file")
        print("  fix       Auto-fix violations")
        print("\nOptions:")
        print("  --editorconfig PATH  Path to .editorconfig")
        print("  --format text|json|markdown  Output format")
        print("  --strict  Exit 1 on any finding")
        print("  --exclude PATTERN  Exclude pattern (repeatable)")
        print("  --max-files N  Max files to check")
        sys.exit(0)

    command = args[0]
    if command not in ('validate', 'check', 'show', 'fix'):
        print(f"Unknown command: {command}")
        sys.exit(2)

    path = args[1] if len(args) > 1 and not args[1].startswith('--') else '.'
    ec_path = None
    fmt = 'text'
    strict = False
    excludes = set(DEFAULT_EXCLUDES)
    max_files = 1000

    i = 2
    while i < len(args):
        if args[i] == '--editorconfig' and i + 1 < len(args):
            ec_path = args[i + 1]; i += 2
        elif args[i] == '--format' and i + 1 < len(args):
            fmt = args[i + 1]; i += 2
        elif args[i] == '--strict':
            strict = True; i += 1
        elif args[i] == '--exclude' and i + 1 < len(args):
            excludes.add(args[i + 1]); i += 2
        elif args[i] == '--max-files' and i + 1 < len(args):
            max_files = int(args[i + 1]); i += 2
        else:
            i += 1

    if command == 'validate':
        ec_file = ec_path or path
        if not os.path.isfile(ec_file):
            ec_file = os.path.join(ec_file, '.editorconfig') if os.path.isdir(ec_file) else ec_file
        sections, issues = parse_editorconfig(ec_file)
        issues_by_file = {ec_file: issues}

        if fmt == 'json':
            print(format_json_output(issues_by_file, 1))
        elif fmt == 'markdown':
            print(format_markdown(issues_by_file, 1))
        else:
            print(format_text(issues_by_file, 1))

        if any(i.severity == 'error' for i in issues):
            sys.exit(1)
        if strict and issues:
            sys.exit(1)

    elif command == 'check':
        if not ec_path:
            ec_path = find_editorconfig(path)
        if not ec_path:
            print("No .editorconfig found")
            sys.exit(2)

        sections, ec_issues = parse_editorconfig(ec_path)
        files = discover_files(path, excludes, max_files)
        issues_by_file = {}

        for filepath in files:
            rel_path = os.path.relpath(filepath, os.path.dirname(ec_path))
            props = match_file(rel_path, sections)
            if props:
                file_issues = check_file_compliance(filepath, props)
                if file_issues:
                    issues_by_file[filepath] = file_issues

        if fmt == 'json':
            print(format_json_output(issues_by_file, len(files)))
        elif fmt == 'markdown':
            print(format_markdown(issues_by_file, len(files)))
        else:
            print(format_text(issues_by_file, len(files)))

        has_errors = any(i.severity == 'error'
                        for issues in issues_by_file.values() for i in issues)
        has_warnings = any(i.severity == 'warning'
                          for issues in issues_by_file.values() for i in issues)
        if has_errors:
            sys.exit(1)
        if strict and has_warnings:
            sys.exit(1)

    elif command == 'show':
        if not ec_path:
            ec_path = find_editorconfig(path)
        if not ec_path:
            print("No .editorconfig found")
            sys.exit(2)

        sections, _ = parse_editorconfig(ec_path)
        rel_path = os.path.relpath(path, os.path.dirname(ec_path))
        props = match_file(rel_path, sections)

        if fmt == 'json':
            print(json.dumps({'file': path, 'properties': props}, indent=2))
        else:
            print(f"Effective EditorConfig for: {path}")
            print(f"Using: {ec_path}")
            print("─" * 40)
            if props:
                for k, v in sorted(props.items()):
                    print(f"  {k} = {v}")
            else:
                print("  (no matching rules)")

    elif command == 'fix':
        if not ec_path:
            ec_path = find_editorconfig(path)
        if not ec_path:
            print("No .editorconfig found")
            sys.exit(2)

        sections, _ = parse_editorconfig(ec_path)
        files = discover_files(path, excludes, max_files)
        total_fixes = 0

        for filepath in files:
            rel_path = os.path.relpath(filepath, os.path.dirname(ec_path))
            props = match_file(rel_path, sections)
            if props:
                fixes = fix_file(filepath, props)
                if fixes:
                    total_fixes += len(fixes)
                    print(f"  Fixed {filepath}: {', '.join(fixes)}")

        print(f"\n✅ Applied {total_fixes} fix(es) across {len(files)} file(s)")


if __name__ == '__main__':
    main()
