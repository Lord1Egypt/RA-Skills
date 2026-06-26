#!/usr/bin/env python3
import argparse
import re
import sys
from dataclasses import dataclass

HEADER_RE = re.compile(
    r'^(?P<type>feat|fix|refactor|perf|docs|test|build|ci|chore|style|revert)'
    r'(?:\((?P<scope>[a-z0-9][a-z0-9-]*)\))?'
    r'(?P<breaking>!)?: '
    r'(?P<desc>.+)$'
)
FOOTER_RE = re.compile(r'^(BREAKING CHANGE|BREAKING-CHANGE|[A-Za-z0-9-]+):\s+.+$')

SEMVER = {
    'feat': 'minor',
    'fix': 'patch',
    'perf': 'patch',
    'refactor': 'none',
    'docs': 'none',
    'test': 'none',
    'build': 'none',
    'ci': 'none',
    'chore': 'none',
    'style': 'none',
    'revert': 'depends',
}


@dataclass
class Result:
    valid: bool
    errors: list[str]
    semver: str | None = None


def read_message(args: argparse.Namespace) -> str:
    if args.message is not None:
        return args.message
    if args.message_file is not None:
        with open(args.message_file, 'r', encoding='utf-8') as f:
            return f.read()
    if args.stdin:
        return sys.stdin.read()
    raise SystemExit('Provide --message, --message-file, or --stdin')


def split_sections(lines: list[str]) -> tuple[str, list[str], list[str]]:
    header = lines[0]
    if len(lines) == 1:
        return header, [], []

    idx = 1
    if lines[idx] != '':
        return header, lines[1:], []

    idx += 1
    remainder = lines[idx:]
    first_footer_idx = None
    for i, line in enumerate(remainder):
        if FOOTER_RE.match(line):
            if i == 0 or remainder[i - 1] == '':
                first_footer_idx = i
                break

    if first_footer_idx is None:
        return header, remainder, []

    body = remainder[:first_footer_idx - 1] if first_footer_idx > 0 and remainder[first_footer_idx - 1] == '' else remainder[:first_footer_idx]
    footers = remainder[first_footer_idx:]
    return header, body, footers


def validate(message: str) -> Result:
    errors: list[str] = []
    lines = message.rstrip('\n').split('\n')
    if not lines or not lines[0].strip():
        return Result(False, ['missing commit header'])

    header, body, footers = split_sections(lines)

    m = HEADER_RE.match(header)
    if not m:
        return Result(False, ['header must match <type>[scope][!]: <description>'])

    commit_type = m.group('type')
    desc = m.group('desc')
    breaking = bool(m.group('breaking'))

    if desc != desc.lower():
        errors.append('description must be lowercase')
    if desc.endswith('.'):
        errors.append('description must not end with a period')
    if len(desc) > 72:
        errors.append('description must be 72 characters or fewer')
    if re.search(r'\b(added|fixed|updated|changed|removed)\b', desc):
        errors.append('description should use imperative mood, not past tense')
    if desc.strip() in {'wip', 'update', 'misc changes', 'fixed stuff'}:
        errors.append('description is too vague')

    if len(lines) > 1 and lines[1] != '':
        errors.append('body or footer must start after one blank line')

    if footers:
        footer_start = lines.index(footers[0])
        if footer_start > 1 and lines[footer_start - 1] != '':
            errors.append('footers must start after one blank line')
        for footer in footers:
            if not FOOTER_RE.match(footer):
                errors.append(f'invalid footer: {footer}')
            if footer.startswith('Breaking Change:'):
                errors.append('BREAKING CHANGE footer must be uppercase')

    has_breaking_footer = any(
        footer.startswith('BREAKING CHANGE:') or footer.startswith('BREAKING-CHANGE:')
        for footer in footers
    )
    semver = 'major' if breaking or has_breaking_footer else SEMVER[commit_type]

    return Result(not errors, errors, semver)


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate Conventional Commit messages.')
    parser.add_argument('--message')
    parser.add_argument('--message-file')
    parser.add_argument('--stdin', action='store_true')
    args = parser.parse_args()

    sources = [args.message is not None, args.message_file is not None, args.stdin]
    if sum(sources) != 1:
        parser.error('use exactly one of --message, --message-file, or --stdin')

    message = read_message(args)
    result = validate(message)

    if result.valid:
        print('VALID')
        print(f'SemVer impact: {result.semver}')
        return 0

    print('INVALID')
    for error in result.errors:
        print(f'- {error}')
    if result.semver:
        print(f'SemVer impact if fixed: {result.semver}')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
