#!/usr/bin/env python3
"""检查生成导师的可加载结构；不替代来源准确性或教学行为评估。"""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from mentor_state import load_state


def chapter_section(content, kind):
    """Use English/Chinese headings, or stable markers under translated headings."""
    names = {'source': {'来源', 'source', 'sources'},
             'questions': {'关键问题', 'key questions', 'practice'}}
    marker = f'<!-- mentor:{kind} -->'
    for match in re.finditer(r'^##[\t ]+([^\n]+)\n(.*?)(?=^#{1,2}[\t ]|\Z)',
                             content, re.M | re.S):
        title, body = match.groups()
        if title.strip().casefold() in names[kind] or marker in body:
            return body.replace(marker, '').strip()
    return ''


def parse_scalar(value):
    value = value.strip()
    if value.startswith('"'):
        parsed = json.loads(value)
        if not isinstance(parsed, str):
            raise ValueError('expected string scalar')
        return parsed
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'") or "'" in value[1:-1].replace("''", ''):
            raise ValueError('invalid quoted scalar')
        return value[1:-1].replace("''", "'")
    if (not value or value[0] in '[]{}&*!|>@`%,' or ': ' in value or value.endswith(':')
            or ' #' in value or value.lower() in {'null', '~', 'true', 'false'}):
        raise ValueError('use a quoted, single-line string')
    return value


def validate(root):
    root = Path(root).resolve()
    errors = []
    required = ['SKILL.md', 'sources.md', 'chapters/index.md', 'glossary.md', 'patterns.md',
                'cheatsheet.md', 'learnings.md', 'state/state.json',
                'scripts/mentor_state.py', 'references/state-schema.md']
    for name in required:
        path = root / name
        if not path.is_file():
            errors.append(f'missing file: {name}')
        elif not path.resolve().is_relative_to(root):
            errors.append(f'file escapes mentor directory: {name}')
    skill = root / 'SKILL.md'
    if skill.is_file():
        content = skill.read_text(encoding='utf-8')
        front = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', content, re.S)
        if not front:
            errors.append('SKILL.md requires YAML frontmatter')
        else:
            # 只接受本模板的两个单行标量；不把部分解析当作通用 YAML 校验。
            fields = {}
            try:
                for line in front.group(1).splitlines():
                    if not line.strip() or line.lstrip().startswith('#'):
                        continue
                    match = re.fullmatch(r'(name|description):[\t ]*(.+)', line)
                    if not match or match.group(1) in fields:
                        raise ValueError('generated frontmatter supports name/description once, as single-line strings')
                    fields[match.group(1)] = parse_scalar(match.group(2))
            except ValueError as exc:
                errors.append(f'invalid generated frontmatter: {exc}')
            name = fields.get('name', '')
            description = fields.get('description', '')
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
                errors.append('invalid or empty name')
            if not description or description in {'|', '>'}:
                errors.append('description must be a nonempty single-line scalar')
    chapters = [p for p in (root / 'chapters').glob('*.md') if p.name != 'index.md']
    if not chapters:
        errors.append('no chapter files')
    for chapter in chapters:
        content = chapter.read_text(encoding='utf-8')
        source = chapter_section(content, 'source')
        questions = chapter_section(content, 'questions')
        if not source:
            errors.append(f'{chapter.name}: missing source locator')
        if not questions or not re.search(r'^(?:\d+[.)]|[-*])\s+\S', questions, re.M):
            errors.append(f'{chapter.name}: missing question or practice item')
    for path in root.rglob('*.md'):
        if not path.resolve().is_relative_to(root):
            errors.append(f'symlink escapes mentor: {path.relative_to(root)}')
            continue
        content = path.read_text(encoding='utf-8')
        if re.search(r'\{(?:slug|Book Title|书|作者|年份|框架\d+)\}|\[TODO:|\{[^{}\n]*(?:实际材料|已知版本|实际章节|实际相对路径|生成前删除|占位链接)[^{}\n]*\}', content):
            errors.append(f'unfilled scaffold: {path.relative_to(root)}')
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^\n)]+)\)', content):
            target = target.strip().strip('<>')
            parts = urlsplit(target)
            if parts.scheme in {'https', 'http', 'mailto'} or target.startswith('#'):
                continue
            if parts.scheme:
                errors.append(f'unsupported link scheme: {target}')
                continue
            linked = (path.parent / unquote(parts.path)).resolve()
            if not linked.is_relative_to(root):
                errors.append(f'link escapes mentor: {target}')
            elif not linked.is_file():
                errors.append(f'broken link in {path.relative_to(root)}: {target}')
    if (root / 'state/state.json').is_file():
        try:
            load_state(root)
        except (ValueError, OSError) as exc:
            errors.append(f'invalid learning state: {exc}')
    return {'passed': not errors, 'chapters': len(chapters), 'errors': errors,
            'scope': 'structure and state only; source fidelity and teaching require separate evaluation'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mentor_dir', type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.mentor_dir)
    except (ValueError, OSError) as exc:
        result = {'passed': False, 'errors': [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
