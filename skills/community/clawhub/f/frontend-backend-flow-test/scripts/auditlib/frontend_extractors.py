from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .common import extract_literal_path, extract_path_from_expr, extract_path_param_names, find_call_segments, find_matching, iter_files, normalize_path, split_top_level, uniq
from .ir import EndpointIR, RequestHints

AXIOS_CREATE_ALIAS_RE = re.compile(r'''\b(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*axios\.create\s*\(''', re.I)
AXIOS_ASSIGN_ALIAS_RE = re.compile(r'''\b(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*axios\s*;''', re.I)
DIO_ALIAS_RE = re.compile(r'''\b(?:final|var|const)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*Dio\s*\(''', re.I)
DIO_SERVICE_RE = re.compile(r'''\.\s*(getRequest|postRequest|putRequest|deleteRequest|postFormRequest|putFormRequest|multipartRequest)\s*\(''', re.I)
CONST_STRING_RE = re.compile(r'''\b(?:const|let|var|final)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([\s\S]*?);''')
AXIOS_BASEURL_RE = re.compile(r'''\b(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*axios\.create\s*\(\s*\{(?:(?!\}\s*\)).)*?baseURL\s*:\s*([^,}\n]+)''', re.I | re.S)
AXIOS_DEFAULT_HEADER_RE = re.compile(r'''\b([A-Za-z_][A-Za-z0-9_]*)\.defaults\.headers(?:\.common)?\s*\[\s*['"]Authorization['"]\s*\]''', re.I)
TS_DECL_RE = re.compile(r'\b(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?::\s*([^=;]+))?=\s*', re.S)
TS_PROP_RE = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)\s*\??\s*:')
TS_METHOD_RE = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*\)\s*:')
TS_INDEX_SIG_RE = re.compile(r'\[[^\]]+\]\s*:')


def build_client_call_re(alias: str) -> re.Pattern:
    return re.compile(rf'''\b{re.escape(alias)}\.(get|post|put|patch|delete)\s*(?:<[\s\S]*?>+)?\s*\(''', re.I)


def build_client_config_re(alias: str) -> re.Pattern:
    return re.compile(rf'''\b{re.escape(alias)}\s*\(\s*\{{(?:(?!\}}\s*\)).)*?method\s*:\s*['"](get|post|put|patch|delete)['"](?:(?!\}}\s*\)).)*?url\s*:\s*(?:"([^"]+)"|'([^']+)'|`([^`]+)`)''', re.I | re.S)


def build_client_request_re(alias: str) -> re.Pattern:
    return re.compile(rf'''\b{re.escape(alias)}\.request\s*(?:<[\s\S]*?>+)?\s*\(\s*\{{(?:(?!\}}\s*\)).)*?method\s*:\s*['"](get|post|put|patch|delete)['"](?:(?!\}}\s*\)).)*?url\s*:\s*(?:"([^"]+)"|'([^']+)'|`([^`]+)`)''', re.I | re.S)


def parse_path_groups(match: re.Match, start_group: int = 2) -> Tuple[str, str, bool]:
    values = [match.group(start_group), match.group(start_group + 1), match.group(start_group + 2)]
    raw = next((v for v in values if v is not None), '')
    ambiguous = '${' in raw or '+' in raw
    return raw, normalize_path(raw), ambiguous


def extract_const_paths(text: str) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for m in CONST_STRING_RE.finditer(text):
        literal = extract_literal_path(m.group(2))
        if literal:
            values[m.group(1)] = literal
    for m in re.finditer(r'for\s*\(\s*final\s+([A-Za-z_][A-Za-z0-9_]*)\s+in\s+\[([^\]]+)\]', text, re.S):
        var_name = m.group(1)
        entries = re.findall(r'''["']([^"']+/[^"']*)["']''', m.group(2))
        if len(entries) == 1:
            values[var_name] = normalize_path(entries[0])
    return values


def extract_axios_alias_base_urls(text: str, const_paths: Dict[str, str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for m in AXIOS_BASEURL_RE.finditer(text):
        literal = extract_literal_path(m.group(2).strip()) or const_paths.get(m.group(2).strip())
        if literal:
            out[m.group(1)] = literal
    return out


def extract_alias_auth_defaults(text: str) -> Dict[str, List[str]]:
    auth_map: Dict[str, List[str]] = {}
    for m in AXIOS_DEFAULT_HEADER_RE.finditer(text):
        auth_map.setdefault(m.group(1), []).append('authorization-default-header')
    return {k: uniq(v) for k, v in auth_map.items()}


def combine_base_url(base_url: Optional[str], raw_path: str) -> str:
    if base_url and raw_path.startswith('/'):
        return normalize_path(f"{base_url.rstrip('/')}/{raw_path.lstrip('/')}")
    return normalize_path(raw_path)


def collect_inline_object_keys(text: str) -> List[str]:
    colon_keys = re.findall(r'([A-Za-z_][A-Za-z0-9_]*)\s*\??\s*:', text)
    shorthand_keys = []
    for part in split_top_level(text):
        candidate = part.strip()
        if not candidate or ':' in candidate or candidate.startswith('...'):
            continue
        candidate = re.sub(r'=.+$', '', candidate).strip()
        candidate = re.sub(r'\?.+$', '', candidate).strip()
        candidate = re.sub(r'\|\|.+$', '', candidate).strip()
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)$', candidate)
        if m:
            shorthand_keys.append(m.group(1))
    return uniq([k for k in colon_keys + shorthand_keys if k not in {'headers', 'params', 'data', 'method', 'url'}])


def find_enclosing_function_bounds(text: str, pos: int) -> Tuple[int, int]:
    for i in range(pos, -1, -1):
        if text[i] != '{':
            continue
        window = text[max(0, i - 220):i]
        if re.search(r'(?:function\s+[A-Za-z_][A-Za-z0-9_]*\s*\([^)]*\)|(?:const|let|var)\s+[A-Za-z_][A-Za-z0-9_]*\s*=\s*(?:async\s*)?\([^)]*\)\s*=>|(?:async\s*)?[A-Za-z_][A-Za-z0-9_]*\s*\([^)]*\)\s*\{?)', window, re.S):
            end = find_matching(text, i, '{', '}')
            if end >= pos:
                return i, end
    return 0, len(text)


def parse_ts_object_type_block(body: str) -> List[str]:
    cleaned = TS_INDEX_SIG_RE.sub('', body)
    props = TS_PROP_RE.findall(cleaned)
    methods = TS_METHOD_RE.findall(cleaned)
    return uniq([k for k in props if k not in methods])


def extract_ts_type_shape(type_name: str, text: str, seen: Optional[set] = None) -> List[str]:
    type_name = re.sub(r'<.*>', '', type_name).strip().split('.')[-1]
    if not type_name:
        return []
    if seen is None:
        seen = set()
    if type_name in seen:
        return []
    seen.add(type_name)
    inline = re.match(r'^\{([\s\S]*)\}$', type_name)
    if inline:
        return parse_ts_object_type_block(inline.group(1))
    iface_pat = re.compile(rf'interface\s+{re.escape(type_name)}(?:\s+extends\s+([^{{]+))?\s*\{{', re.S)
    type_pat = re.compile(rf'type\s+{re.escape(type_name)}\s*=\s*([\s\S]+?);')
    iface = iface_pat.search(text)
    if iface:
        brace_start = text.find('{', iface.start())
        brace_end = find_matching(text, brace_start, '{', '}')
        if brace_start >= 0 and brace_end >= 0:
            keys = parse_ts_object_type_block(text[brace_start + 1:brace_end])
            bases = [b.strip() for b in iface.group(1).split(',')] if iface.group(1) else []
            for base in bases:
                keys.extend(extract_ts_type_shape(base, text, seen))
            return uniq(keys)
    tm = type_pat.search(text)
    if not tm:
        return []
    expr = tm.group(1).strip()
    obj = re.match(r'^\{([\s\S]*)\}$', expr)
    if obj:
        return parse_ts_object_type_block(obj.group(1))
    pick = re.match(r'^(?:Pick|Omit|Partial|Required|Readonly)\s*<\s*([A-Za-z0-9_$.]+)', expr)
    if pick:
        return extract_ts_type_shape(pick.group(1), text, seen)
    alias = re.match(r'^([A-Za-z_][A-Za-z0-9_$.<>]*)$', expr)
    if alias:
        return extract_ts_type_shape(alias.group(1), text, seen)
    return []


def find_nearest_variable_declaration(name: str, text: str, pos: int, scope_start: int, scope_end: int):
    search_area = text[scope_start:pos]
    last = None
    for m in TS_DECL_RE.finditer(search_area):
        if m.group(1) != name:
            continue
        abs_start = scope_start + m.end() - 1
        while abs_start < len(text) and text[abs_start].isspace():
            abs_start += 1
        if abs_start >= len(text):
            continue
        expr = ''
        if text[abs_start] == '{':
            end = find_matching(text, abs_start, '{', '}')
            if end > abs_start:
                expr = text[abs_start:end + 1]
        else:
            semi = text.find(';', abs_start, scope_end)
            newline = text.find('\n', abs_start, scope_end)
            candidates = [x for x in [semi, newline] if x != -1]
            end = min(candidates) if candidates else min(scope_end, abs_start + 300)
            expr = text[abs_start:end].strip()
        last = (expr.strip(), (m.group(2) or '').strip() or None)
    return last


def extract_function_param_type(name: str, text: str, pos: int) -> Optional[str]:
    scope_start, _ = find_enclosing_function_bounds(text, pos)
    header = text[max(0, scope_start - 320):scope_start]
    m = re.search(r'\(([^()]*)\)\s*(?::\s*[^=]+)?\s*(?:=>)?\s*$', header, re.S)
    if not m:
        return None
    for part in split_top_level(m.group(1)):
        pm = re.match(rf'\s*{re.escape(name)}\s*\??\s*:\s*([\s\S]+?)\s*$', part)
        if pm:
            return pm.group(1).strip()
    return None


def extract_named_object_shape(name: str, text: str, pos: Optional[int] = None) -> List[str]:
    pos = len(text) if pos is None else pos
    scope_start, scope_end = find_enclosing_function_bounds(text, pos)
    decl = find_nearest_variable_declaration(name, text, pos, scope_start, scope_end)
    keys: List[str] = []
    if decl:
        expr, declared_type = decl
        if expr.startswith('{'):
            keys.extend(collect_inline_object_keys(expr[1:-1]))
        else:
            keys.extend(re.findall(rf'\b{re.escape(name)}\.([A-Za-z_][A-Za-z0-9_]*)\s*=', text[scope_start:scope_end]))
            if declared_type:
                keys.extend(extract_ts_type_shape(declared_type, text))
    if not keys:
        param_type = extract_function_param_type(name, text, pos)
        if param_type:
            keys.extend(extract_ts_type_shape(param_type, text))
    return uniq(keys)


def extract_local_string_assignments(text: str, pos: int, scope_window: int = 500) -> Dict[str, str]:
    start = max(0, pos - scope_window)
    snippet = text[start:pos]
    values: Dict[str, str] = {}
    for m in CONST_STRING_RE.finditer(snippet):
        literal = extract_literal_path(m.group(2))
        if literal:
            values[m.group(1)] = literal
    return values


def infer_body_keys_from_expr(expr: str, text: str, pos: Optional[int] = None) -> List[str]:
    expr = expr.strip()
    if not expr:
        return []
    if expr.startswith('{'):
        return collect_inline_object_keys(expr[1:-1])
    cast_m = re.match(r'\(?\s*([A-Za-z_][A-Za-z0-9_]*)\s+as\s+([A-Za-z0-9_$.<>|&\[\] ]+)\s*\)?$', expr)
    if cast_m:
        return extract_named_object_shape(cast_m.group(1), text, pos) or extract_ts_type_shape(cast_m.group(2).strip(), text)
    m = re.match(r'([A-Za-z_][A-Za-z0-9_]*)\s*$', expr)
    if m:
        return extract_named_object_shape(m.group(1), text, pos)
    return []


def infer_auth_from_expr(expr: str) -> List[str]:
    auth = []
    if re.search(r'Authorization\s*:', expr, re.I) or re.search(r'authorizationHeader', expr, re.I):
        auth.append('authorization-header')
    if re.search(r'withAuth\s*\(', expr):
        auth.append('authorization-helper')
    if re.search(r'Bearer\s|accessToken|token', expr, re.I):
        auth.append('token-ref')
    if re.search(r'withCredentials\s*:\s*true', expr):
        auth.append('cookie-session')
    return uniq(auth)


def infer_response_keys(source: str, file_text: str, call_pos: Optional[int] = None) -> List[str]:
    window_start = call_pos or 0
    window = file_text[window_start:min(len(file_text), window_start + 900)]
    keys: List[str] = []
    patterns = [
        r'\.data\.([A-Za-z_][A-Za-z0-9_]*)',
        r'\.data\?\.([A-Za-z_][A-Za-z0-9_]*)',
        r'\.json\(\)\s*\.([A-Za-z_][A-Za-z0-9_]*)',
        r"\[['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\]",
    ]
    for pat in patterns:
        keys.extend(re.findall(pat, window))
    assign_match = re.search(r'(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*await\s+' + re.escape(source[: min(len(source), 80)]), file_text[max(0, window_start - 200):window_start + 200], re.S)
    if assign_match:
        var_name = assign_match.group(1)
        later = file_text[window_start:min(len(file_text), window_start + 1200)]
        keys.extend(re.findall(rf'\b{re.escape(var_name)}\.data\.([A-Za-z_][A-Za-z0-9_]*)', later))
        keys.extend(re.findall(rf'\b{re.escape(var_name)}\.([A-Za-z_][A-Za-z0-9_]*)', later))
    return uniq([k for k in keys if k not in {'then', 'catch', 'length', 'map', 'filter', 'status', 'data'}])


def infer_frontend_hints(method: str, raw_path: str, source: str, file_text: str, args: List[str], alias_auth: Optional[List[str]] = None, call_pos: Optional[int] = None) -> RequestHints:
    hints = RequestHints(path_params=extract_path_param_names(raw_path))
    method = method.upper()
    config_expr = ''
    body_expr = ''
    if method in {'POST', 'PUT', 'PATCH'}:
        if len(args) >= 2:
            body_expr = args[1]
        if len(args) >= 3:
            config_expr = args[2]
    elif method == 'DELETE':
        if len(args) >= 2:
            config_expr = args[1]
            data_match = re.search(r'data\s*:\s*(\{[\s\S]*\}|[A-Za-z_][A-Za-z0-9_]*)', config_expr, re.S)
            if data_match:
                body_expr = data_match.group(1)
    else:
        if len(args) >= 2:
            config_expr = args[1]
    params_match = re.search(r'params\s*:\s*\{([\s\S]*?)\}', config_expr, re.S)
    if params_match:
        hints.query_params = collect_inline_object_keys(params_match.group(1))
    else:
        params_var = re.search(r'params\s*:\s*([A-Za-z_][A-Za-z0-9_]*)', config_expr)
        if params_var:
            hints.query_params = extract_named_object_shape(params_var.group(1), file_text, call_pos) or [params_var.group(1)]
    if method in {'POST', 'PUT', 'PATCH', 'DELETE'} and body_expr:
        if 'FormData' in body_expr or 'formData' in body_expr:
            hints.body_kind = 'form-data'
            hints.consumes = 'multipart/form-data'
        else:
            body_keys = infer_body_keys_from_expr(body_expr, file_text, call_pos)
            hints.body_kind = 'json-object' if body_keys else 'body-variable'
            hints.body_keys = body_keys
    if re.search(r'multipart/form-data', source, re.I) or re.search(r'FormData|formData', body_expr):
        hints.consumes = 'multipart/form-data'
    hints.response_keys = infer_response_keys(source, file_text, call_pos)
    hints.auth.extend(infer_auth_from_expr(source))
    hints.auth.extend(infer_auth_from_expr(config_expr))
    if alias_auth:
        hints.auth.extend(alias_auth)
    hints.auth = uniq(hints.auth)
    return hints


def extract_frontend_default_base_path(root: Path) -> Optional[str]:
    candidates = [root / 'assets' / 'config', root / 'config', root]
    seen = set()
    for base in candidates:
        if not base.exists() or not base.is_dir():
            continue
        for env_path in base.glob('.env*'):
            raw = env_path.read_text(encoding='utf-8', errors='ignore')
            for line in raw.splitlines():
                if not line.startswith('HTTP_URL='):
                    continue
                m = re.match(r'https?://[^/]+(/[^?#]+)', line.split('=', 1)[1].strip())
                if m:
                    path = normalize_path(m.group(1))
                    if path not in {'/', ''}:
                        seen.add(path)
    return sorted(seen, key=len)[0] if seen else None


def dedupe(items: List[EndpointIR]) -> List[EndpointIR]:
    seen = set()
    out = []
    for item in items:
        key = (item.side, item.method, item.path, item.file, item.line, item.framework)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def extract_frontend_endpoints(root: Path) -> List[EndpointIR]:
    endpoints: List[EndpointIR] = []
    default_base_path = extract_frontend_default_base_path(root)
    for path in iter_files(root):
        try:
            text = path.read_text(encoding='utf-8')
        except Exception:
            text = path.read_text(encoding='utf-8', errors='ignore')
        axios_aliases = {'axios'}
        dio_aliases = set()
        const_paths = extract_const_paths(text)
        axios_alias_base_urls = extract_axios_alias_base_urls(text, const_paths)
        alias_auth_defaults = extract_alias_auth_defaults(text)
        for m in AXIOS_CREATE_ALIAS_RE.finditer(text):
            axios_aliases.add(m.group(1))
        for m in AXIOS_ASSIGN_ALIAS_RE.finditer(text):
            axios_aliases.add(m.group(1))
        if path.suffix.lower() == '.dart':
            for m in DIO_ALIAS_RE.finditer(text):
                dio_aliases.add(m.group(1))
        def append_endpoint(method: str, raw_path: str, line: int, source: str, framework: str, ambiguous: bool, hints: RequestHints, effective_base: Optional[str]):
            if not raw_path:
                return
            confidence = 'medium' if ambiguous else 'high'
            endpoints.append(EndpointIR(side='frontend', method=method.upper(), path=combine_base_url(effective_base, normalize_path(raw_path)), raw_path=raw_path, file=str(path), line=line, source=source.strip(), locator=framework, framework=framework, ambiguous=ambiguous, confidence=confidence, hints=hints))
        for alias in sorted(axios_aliases):
            for seg in find_call_segments(text, build_client_call_re(alias), f'axios-alias:{alias}'):
                args = seg['args']
                if not args:
                    continue
                method = seg['match'].group(1).upper()
                raw = extract_path_from_expr(args[0], const_paths) or ''
                ambiguous = '${' in raw or '+' in raw
                hints = infer_frontend_hints(method, raw, seg['source'], text, args, alias_auth_defaults.get(alias, []), int(seg['start']))
                append_endpoint(method, raw, seg['line'], seg['source'], seg['kind'], ambiguous, hints, axios_alias_base_urls.get(alias) or default_base_path)
        for alias in sorted(axios_aliases):
            for seg in find_call_segments(text, build_client_request_re(alias), f'axios-request:{alias}'):
                method = seg['match'].group(1).upper()
                raw = parse_path_groups(seg['match'], 2)[0]
                ambiguous = '${' in raw or '+' in raw
                hints = infer_frontend_hints(method, raw, seg['source'], text, seg['args'], alias_auth_defaults.get(alias, []), int(seg['start']))
                append_endpoint(method, raw, seg['line'], seg['source'], seg['kind'], ambiguous, hints, axios_alias_base_urls.get(alias) or default_base_path)
        for alias in sorted(axios_aliases):
            for seg in find_call_segments(text, build_client_config_re(alias), f'axios-config:{alias}'):
                method = seg['match'].group(1).upper()
                raw = parse_path_groups(seg['match'], 2)[0]
                ambiguous = '${' in raw or '+' in raw
                hints = infer_frontend_hints(method, raw, seg['source'], text, seg['args'], alias_auth_defaults.get(alias, []), int(seg['start']))
                append_endpoint(method, raw, seg['line'], seg['source'], seg['kind'], ambiguous, hints, axios_alias_base_urls.get(alias) or default_base_path)
        for seg in find_call_segments(text, re.compile(r'\bfetch\s*\('), 'fetch'):
            args = seg['args']
            if not args:
                continue
            local_paths = extract_local_string_assignments(text, int(seg['start']))
            raw = extract_path_from_expr(args[0], {**const_paths, **local_paths}) or ''
            method = 'GET'
            if len(args) >= 2:
                mm = re.search(r'method\s*:\s*["\'](GET|POST|PUT|PATCH|DELETE)["\']', args[1], re.I)
                if mm:
                    method = mm.group(1).upper()
            ambiguous = '${' in raw or '+' in raw
            hints = infer_frontend_hints(method, raw, seg['source'], text, args, None, int(seg['start']))
            append_endpoint(method, raw, seg['line'], seg['source'], 'fetch', ambiguous, hints, default_base_path)
        if path.suffix.lower() == '.dart':
            for alias in sorted(dio_aliases):
                for seg in find_call_segments(text, build_client_call_re(alias), f'dio-alias:{alias}'):
                    args = seg['args']
                    if not args:
                        continue
                    method = seg['match'].group(1).upper()
                    local_paths = extract_local_string_assignments(text, int(seg['start']))
                    raw = extract_path_from_expr(args[0], {**const_paths, **local_paths}) or ''
                    if not raw.startswith('/'):
                        continue
                    ambiguous = '${' in raw or '+' in raw
                    hints = infer_frontend_hints(method, raw, seg['source'], text, args, None, int(seg['start']))
                    append_endpoint(method, raw, seg['line'], seg['source'], seg['kind'], ambiguous, hints, default_base_path)
            wrapper_method_map = {'getrequest': 'GET', 'postrequest': 'POST', 'putrequest': 'PUT', 'deleterequest': 'DELETE', 'postformrequest': 'POST', 'putformrequest': 'PUT', 'multipartrequest': 'POST'}
            for seg in find_call_segments(text, DIO_SERVICE_RE, 'dio-service-wrapper'):
                wrapper_name = seg['match'].group(1)
                method = wrapper_method_map.get(wrapper_name.lower())
                args = seg['args']
                if not method or not args:
                    continue
                local_paths = extract_local_string_assignments(text, int(seg['start']))
                raw = extract_path_from_expr(args[0], {**const_paths, **local_paths}) or ''
                if not raw.startswith('/'):
                    continue
                ambiguous = '${' in raw or '+' in raw
                hints = infer_frontend_hints(method, raw, seg['source'], text, args, None, int(seg['start']))
                if wrapper_name.lower() in {'postformrequest', 'putformrequest', 'multipartrequest'}:
                    hints.consumes = 'multipart/form-data'
                    hints.body_kind = hints.body_kind or 'form-data'
                append_endpoint(method, raw, seg['line'], seg['source'], seg['kind'], ambiguous, hints, default_base_path)
    return dedupe(endpoints)
