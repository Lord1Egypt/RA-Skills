from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

TEXT_EXTENSIONS = {'.js', '.jsx', '.ts', '.tsx', '.dart', '.java', '.kt', '.php'}
DEFAULT_EXCLUDED_PARTS = {'node_modules', 'build', 'dist', '.git', '.gradle', 'target'}


def load_excluded_parts() -> set[str]:
    raw = os.environ.get('AUDIT_EXCLUDE_PARTS', '')
    extra = {part.strip() for part in raw.split(',') if part.strip()}
    return DEFAULT_EXCLUDED_PARTS | extra


def iter_files(root: Path):
    excluded_parts = load_excluded_parts()
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if any(part in excluded_parts for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def uniq(seq: List[str]) -> List[str]:
    seen = set()
    out = []
    for item in seq:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def normalize_path(path: str) -> str:
    path = path.strip()
    if not path:
        return '/'
    if '?' in path:
        path = path.split('?', 1)[0]
    if '#' in path:
        path = path.split('#', 1)[0]
    if not path.startswith('/'):
        path = '/' + path
    path = re.sub(r'\$\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}', r'{\1}', path)
    path = re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)', r'{\1}', path)
    path = re.sub(r'\{[^/]+\}', '{}', path)
    path = re.sub(r':([A-Za-z_][A-Za-z0-9_]*)', '{}', path)
    path = re.sub(r'//+', '/', path)
    if len(path) > 1 and path.endswith('/'):
        path = path[:-1]
    return path


def extract_path_param_names(raw_path: str) -> List[str]:
    names = re.findall(r'\$\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}', raw_path)
    names += re.findall(r'\$([A-Za-z_][A-Za-z0-9_]*)', raw_path)
    names += re.findall(r'\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}', raw_path)
    names += re.findall(r':([A-Za-z_][A-Za-z0-9_]*)', raw_path)
    return uniq(names)


def path_similarity(a: str, b: str) -> bool:
    return normalize_path(a) == normalize_path(b)


def line_of(text: str, pos: int) -> int:
    return text[:pos].count('\n') + 1


def find_matching(text: str, start: int, open_char: str, close_char: str) -> int:
    depth = 0
    quote = None
    escaped = False
    i = start
    while i < len(text):
        ch = text[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == quote:
                quote = None
            i += 1
            continue
        if ch in {'"', "'", '`'}:
            quote = ch
        elif ch == open_char:
            depth += 1
        elif ch == close_char:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def split_top_level(expr: str, delimiter: str = ',') -> List[str]:
    parts: List[str] = []
    start = 0
    stack: List[str] = []
    quote = None
    escaped = False
    i = 0
    while i < len(expr):
        ch = expr[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == quote:
                quote = None
            i += 1
            continue
        if ch in {'"', "'", '`'}:
            quote = ch
        elif ch in '([{<':
            stack.append(ch)
        elif ch in ')]}>':
            if stack:
                stack.pop()
        elif ch == delimiter and not stack:
            parts.append(expr[start:i].strip())
            start = i + 1
        i += 1
    tail = expr[start:].strip()
    if tail:
        parts.append(tail)
    return parts


def find_call_segments(text: str, pattern: re.Pattern, kind: str) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for m in pattern.finditer(text):
        paren_start = text.find('(', m.start())
        if paren_start < 0:
            continue
        paren_end = find_matching(text, paren_start, '(', ')')
        if paren_end < 0:
            continue
        full_call = text[m.start():paren_end + 1]
        args_src = text[paren_start + 1:paren_end]
        args = split_top_level(args_src)
        out.append({'start': m.start(), 'line': line_of(text, m.start()), 'source': full_call.strip(), 'args': args, 'kind': kind, 'match': m})
    return out


def extract_literal_path(expr: str) -> Optional[str]:
    for m in re.finditer(r'''["']([^"']+)["']''', expr):
        value = m.group(1)
        if '/' in value:
            if value.startswith('http://') or value.startswith('https://'):
                value = '/' + value.split('/', 3)[-1].split('?', 1)[0]
            return normalize_path(value)
    return None


def extract_path_from_expr(expr: str, const_paths: Optional[Dict[str, str]] = None) -> Optional[str]:
    expr = expr.strip()
    for pat in [r'^"([^"]+)"$', r"^'([^']+)'$", r'^`([^`]+)`$']:
        m = re.match(pat, expr, re.S)
        if m:
            return m.group(1)
    if const_paths and expr in const_paths:
        return const_paths[expr]
    return extract_literal_path(expr)


def compare_hint_lists(fe_items: List[str], be_items: List[str], normalize=None) -> Dict[str, List[str]]:
    if normalize:
        fe_set = set(normalize(fe_items))
        be_set = set(normalize(be_items))
    else:
        fe_set = set(fe_items)
        be_set = set(be_items)
    return {'frontend_only': sorted(fe_set - be_set), 'backend_only': sorted(be_set - fe_set), 'shared': sorted(fe_set & be_set)}
