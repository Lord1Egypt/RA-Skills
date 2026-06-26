#!/usr/bin/env python3
"""Changelog Linter — validate CHANGELOG.md against Keep a Changelog spec.

Pure Python stdlib. No dependencies.
"""
import sys, re, json, argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_SECTIONS = ['Added', 'Changed', 'Deprecated', 'Removed', 'Fixed', 'Security']
SECTION_ORDER = {s: i for i, s in enumerate(VALID_SECTIONS)}

SEMVER_RE = re.compile(r'^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?(?:\+([a-zA-Z0-9.]+))?$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
VERSION_HEADER_RE = re.compile(r'^##\s+\[([^\]]+)\](?:\s*-\s*(.+))?$')
SECTION_HEADER_RE = re.compile(r'^###\s+(.+)$')
LINK_REF_RE = re.compile(r'^\[([^\]]+)\]:\s*(.+)$')


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
# Parser
# ---------------------------------------------------------------------------

def parse_changelog(text):
    """Parse changelog into structured data."""
    lines = text.splitlines()
    result = {
        'title': None,
        'title_line': 0,
        'description': '',
        'versions': [],
        'link_refs': {},
    }

    i = 0
    # find title
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('# '):
            result['title'] = line[2:].strip()
            result['title_line'] = i + 1
            i += 1
            break
        if line:  # non-empty non-title line
            break
        i += 1

    # collect description (lines before first ## )
    desc_lines = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('## '):
            break
        desc_lines.append(line)
        i += 1
    result['description'] = '\n'.join(desc_lines).strip()

    # parse versions
    current_version = None
    current_section = None

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # version header
        vm = VERSION_HEADER_RE.match(stripped)
        if vm:
            if current_version:
                result['versions'].append(current_version)
            current_version = {
                'name': vm.group(1),
                'date': vm.group(2).strip() if vm.group(2) else None,
                'line': i + 1,
                'sections': {},
                'raw_sections': [],
            }
            current_section = None
            i += 1
            continue

        # section header
        sm = SECTION_HEADER_RE.match(stripped)
        if sm and current_version is not None:
            section_name = sm.group(1).strip()
            current_section = section_name
            if section_name not in current_version['sections']:
                current_version['sections'][section_name] = []
            current_version['raw_sections'].append({
                'name': section_name,
                'line': i + 1,
            })
            i += 1
            continue

        # list item
        if stripped.startswith('- ') or stripped.startswith('* '):
            if current_version and current_section:
                current_version['sections'][current_section].append({
                    'text': stripped[2:].strip(),
                    'bullet': stripped[0],
                    'line': i + 1,
                })
            i += 1
            continue

        # link reference
        lm = LINK_REF_RE.match(stripped)
        if lm:
            result['link_refs'][lm.group(1)] = {
                'url': lm.group(2).strip(),
                'line': i + 1,
            }
            i += 1
            continue

        i += 1

    if current_version:
        result['versions'].append(current_version)

    return result, lines


# ---------------------------------------------------------------------------
# Linters
# ---------------------------------------------------------------------------

def lint_structure(parsed, lines):
    """Rules 1-5: structural checks."""
    issues = []

    # missing title
    if not parsed['title']:
        issues.append(Issue('missing-title', 'error', 'File should start with `# Changelog`', 1))
    elif 'changelog' not in parsed['title'].lower():
        issues.append(Issue('missing-title', 'warning',
            f'Title is `{parsed["title"]}` — expected `Changelog`', parsed['title_line']))

    # missing description
    if not parsed['description']:
        issues.append(Issue('missing-description', 'info',
            'No description paragraph after title (recommended by spec)', parsed.get('title_line', 1)))

    # no versions
    if not parsed['versions']:
        issues.append(Issue('no-versions', 'warning', 'No version entries found', 1))
        return issues

    # empty version
    for v in parsed['versions']:
        if v['name'].lower() == 'unreleased':
            continue
        if not v['sections'] or all(len(items) == 0 for items in v['sections'].values()):
            issues.append(Issue('empty-version', 'warning',
                f'Version {v["name"]} has no change entries', v['line']))

    # unreleased missing
    has_unreleased = any(v['name'].lower() == 'unreleased' for v in parsed['versions'])
    if not has_unreleased:
        issues.append(Issue('unreleased-missing', 'info',
            'No [Unreleased] section (recommended by spec)', 1))

    return issues


def lint_versions(parsed):
    """Rules 6-9: version validation."""
    issues = []
    seen = {}
    semver_list = []

    for v in parsed['versions']:
        name = v['name']
        if name.lower() == 'unreleased':
            continue

        # invalid version
        if not SEMVER_RE.match(name):
            issues.append(Issue('invalid-version', 'error',
                f'Version `{name}` does not follow semver (MAJOR.MINOR.PATCH)', v['line']))
        else:
            m = SEMVER_RE.match(name)
            semver_list.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), v['line'], name))

        # invalid date
        date = v.get('date')
        if date:
            # strip any surrounding brackets or extra text
            date_clean = date.strip()
            if not DATE_RE.match(date_clean):
                issues.append(Issue('invalid-date', 'error',
                    f'Version {name} has invalid date: `{date_clean}` (expected YYYY-MM-DD)', v['line']))
        elif name.lower() != 'unreleased':
            issues.append(Issue('invalid-date', 'warning',
                f'Version {name} has no release date', v['line']))

        # duplicate version
        if name in seen:
            issues.append(Issue('duplicate-version', 'error',
                f'Version {name} appears twice (lines {seen[name]} and {v["line"]})', v['line']))
        seen[name] = v['line']

    # version order (should be descending)
    for i in range(len(semver_list) - 1):
        curr = semver_list[i][:3]
        nxt = semver_list[i + 1][:3]
        if curr < nxt:
            issues.append(Issue('version-order', 'warning',
                f'Version {semver_list[i][4]} should come after {semver_list[i+1][4]} (descending order)',
                semver_list[i][3]))

    return issues


def lint_sections(parsed):
    """Rules 10-12: section validation."""
    issues = []

    for v in parsed['versions']:
        prev_order = -1
        for rs in v['raw_sections']:
            name = rs['name']

            # invalid section
            if name not in VALID_SECTIONS:
                issues.append(Issue('invalid-section', 'warning',
                    f'Section `{name}` under {v["name"]} is not a standard type '
                    f'(expected: {", ".join(VALID_SECTIONS)})', rs['line']))

            # empty section
            items = v['sections'].get(name, [])
            if len(items) == 0:
                issues.append(Issue('empty-section', 'warning',
                    f'Section `{name}` under {v["name"]} has no entries', rs['line']))

            # section order
            if name in SECTION_ORDER:
                order = SECTION_ORDER[name]
                if order < prev_order:
                    issues.append(Issue('section-order', 'info',
                        f'Section `{name}` under {v["name"]} is out of recommended order', rs['line']))
                prev_order = order

    return issues


def lint_formatting(parsed, lines):
    """Rules 13-16: formatting checks."""
    issues = []

    # missing link refs
    for v in parsed['versions']:
        if v['name'] not in parsed['link_refs']:
            issues.append(Issue('missing-link-ref', 'warning',
                f'Version {v["name"]} has no link reference at bottom of file', v['line']))

    # broken link refs
    for name, ref in parsed['link_refs'].items():
        url = ref['url']
        if not url or url == '#' or not (url.startswith('http') or url.startswith('..')):
            issues.append(Issue('broken-link-ref', 'warning',
                f'Link reference for `{name}` has suspicious URL: `{url}`', ref['line']))

    # inconsistent bullets
    bullets = set()
    for v in parsed['versions']:
        for section_items in v['sections'].values():
            for item in section_items:
                bullets.add(item['bullet'])
    if len(bullets) > 1:
        issues.append(Issue('inconsistent-bullets', 'info',
            f'Mixed bullet styles found: {", ".join(repr(b) for b in bullets)} — pick one'))

    # trailing whitespace
    tw_count = 0
    first_tw = 0
    for i, line in enumerate(lines):
        if line != line.rstrip():
            tw_count += 1
            if not first_tw:
                first_tw = i + 1
    if tw_count > 0:
        issues.append(Issue('trailing-whitespace', 'info',
            f'{tw_count} line(s) with trailing whitespace (first at line {first_tw})', first_tw))

    return issues


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_lint(filepath, strict=False, fmt='text'):
    text = Path(filepath).read_text(encoding='utf-8', errors='replace')
    parsed, lines = parse_changelog(text)

    issues = []
    issues.extend(lint_structure(parsed, lines))
    issues.extend(lint_versions(parsed))
    issues.extend(lint_sections(parsed))
    issues.extend(lint_formatting(parsed, lines))

    output_issues(filepath, issues, fmt)
    return exit_code(issues, strict)


def cmd_versions(filepath, fmt='text'):
    text = Path(filepath).read_text(encoding='utf-8', errors='replace')
    parsed, _ = parse_changelog(text)

    versions = []
    for v in parsed['versions']:
        total = sum(len(items) for items in v['sections'].values())
        versions.append({
            'name': v['name'],
            'date': v.get('date'),
            'changes': total,
            'sections': list(v['sections'].keys()),
        })

    if fmt == 'json':
        print(json.dumps(versions, indent=2))
    else:
        for v in versions:
            date_str = v['date'] or 'no date'
            print(f"  {v['name']:20s} {date_str:12s} {v['changes']:3d} changes  [{', '.join(v['sections'])}]")
    return 0


def cmd_order(filepath, fmt='text'):
    text = Path(filepath).read_text(encoding='utf-8', errors='replace')
    parsed, _ = parse_changelog(text)
    issues = lint_versions(parsed)
    order_issues = [i for i in issues if i.rule == 'version-order']
    output_issues(filepath, order_issues, fmt)
    return 1 if order_issues else 0


def cmd_links(filepath, fmt='text'):
    text = Path(filepath).read_text(encoding='utf-8', errors='replace')
    parsed, lines = parse_changelog(text)
    issues = lint_formatting(parsed, lines)
    link_issues = [i for i in issues if i.rule in ('missing-link-ref', 'broken-link-ref')]
    output_issues(filepath, link_issues, fmt)
    return 1 if link_issues else 0


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
            print(f'{filepath}:{iss.line} {iss.severity} [{iss.rule}] {iss.message}')
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
    parser = argparse.ArgumentParser(description='Changelog Linter — Keep a Changelog validator')
    sub = parser.add_subparsers(dest='command', required=True)

    p_lint = sub.add_parser('lint', help='Lint changelog (all rules)')
    p_lint.add_argument('file', help='Path to CHANGELOG.md')
    p_lint.add_argument('--strict', action='store_true')
    p_lint.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    p_ver = sub.add_parser('versions', help='List versions')
    p_ver.add_argument('file', help='Path to CHANGELOG.md')
    p_ver.add_argument('--format', choices=['text', 'json'], default='text')

    p_ord = sub.add_parser('order', help='Check version ordering')
    p_ord.add_argument('file', help='Path to CHANGELOG.md')
    p_ord.add_argument('--format', choices=['text', 'json'], default='text')

    p_lnk = sub.add_parser('links', help='Check link references')
    p_lnk.add_argument('file', help='Path to CHANGELOG.md')
    p_lnk.add_argument('--format', choices=['text', 'json'], default='text')

    args = parser.parse_args()
    fmt = getattr(args, 'format', 'text')

    if args.command == 'lint':
        sys.exit(cmd_lint(args.file, args.strict, fmt))
    elif args.command == 'versions':
        sys.exit(cmd_versions(args.file, fmt))
    elif args.command == 'order':
        sys.exit(cmd_order(args.file, fmt))
    elif args.command == 'links':
        sys.exit(cmd_links(args.file, fmt))


if __name__ == '__main__':
    main()
