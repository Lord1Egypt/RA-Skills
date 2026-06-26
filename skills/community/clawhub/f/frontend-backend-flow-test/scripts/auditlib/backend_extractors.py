from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .common import extract_path_param_names, find_matching, find_call_segments, iter_files, line_of, normalize_path, split_top_level, uniq
from .ir import EndpointIR, RequestHints

JAVA_RECORD_RE = re.compile(r'\brecord\s+([A-Za-z0-9_]+)\s*\((.*?)\)\s*\{', re.S)
JAVA_CLASS_RE = re.compile(r'\bclass\s+([A-Za-z0-9_]+)\b[^\{]*\{', re.S)
JAVA_FIELD_RE = re.compile(r'(?:private|protected|public)\s+(?:final\s+)?[A-Za-z0-9_<>,.?\[\] ]+\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:=[^;]+)?;')
MAPPING_RE = re.compile(r'@(Get|Post|Put|Patch|Delete)Mapping(?:\s*\(([^)]*)\))?')
REQUEST_MAPPING_RE = re.compile(r'@RequestMapping\s*\(([^)]*)\)')
CLASS_RE = re.compile(r'class\s+([A-Za-z0-9_]+)')
METHOD_RE = re.compile(r'(?:public|private|protected)\s+[A-Za-z0-9_<>, ?\[\]]+\s+([A-Za-z0-9_]+)\s*\(')
RETURN_TYPE_RE = re.compile(r'(?:public|private|protected)\s+([A-Za-z0-9_$.<>?, \[\]]+)\s+([A-Za-z0-9_]+)\s*\(')

JS_VAR_ASSIGN_RE = re.compile(r'\b(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?);')
EXPRESS_ROUTER_CREATE_RE = re.compile(r'\b(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:express\.)?Router\s*\(')
EXPRESS_METHOD_CALL_RE = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\.\s*(get|post|put|patch|delete)\s*\(')
EXPRESS_ROUTE_CALL_RE = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\.\s*route\s*\(')
EXPRESS_USE_CALL_RE = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\.\s*use\s*\(')
REQ_QUERY_ACCESS_RE = re.compile(r'\breq\.query\.([A-Za-z_][A-Za-z0-9_]*)')
REQ_BODY_ACCESS_RE = re.compile(r'\breq\.body\.([A-Za-z_][A-Za-z0-9_]*)')
REQ_PARAM_ACCESS_RE = re.compile(r'\breq\.params\.([A-Za-z_][A-Za-z0-9_]*)')
REQ_HEADER_ACCESS_RE = re.compile(r'\breq\.(?:headers\[[^\]]+\]|get\([^)]+\)|header\([^)]+\))')
MULTER_CALL_RE = re.compile(r'\b(upload|multerUpload|uploader)\.(single|array|fields)\s*\(')

LARAVEL_ROUTE_DIRECT_RE = re.compile(r'Route::(get|post|put|patch|delete)\s*\(', re.I)
LARAVEL_ROUTE_MATCH_RE = re.compile(r'Route::match\s*\(', re.I)
LARAVEL_ROUTE_ANY_RE = re.compile(r'Route::any\s*\(', re.I)
LARAVEL_PREFIX_GROUP_RE = re.compile(r'Route::prefix\s*\(')
LARAVEL_RESOURCE_RE = re.compile(r'Route::(apiResource|resource)\s*\(', re.I)
LARAVEL_CONTROLLER_ACTION_RE = re.compile(r'\[\s*([A-Za-z0-9_\\]+)::class\s*,\s*[\'"]([A-Za-z0-9_]+)[\'"]\s*\]')
PHP_METHOD_DEF_RE = re.compile(r'function\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)\s*(?::\s*[A-Za-z0-9_\\|?]+)?\s*\{', re.S)
PHP_REQ_QUERY_RE = re.compile(r'\$request->(?:query|get)\(\s*[\'"]([^\'"]+)[\'"]')
PHP_REQ_INPUT_RE = re.compile(r'\$request->(?:input|post|string|integer|boolean|date|file)\(\s*[\'"]([^\'"]+)[\'"]')
PHP_REQ_VALIDATE_KEY_RE = re.compile(r'\$request->(?:validate|validated)\s*\(\s*\[([\s\S]*?)\]\s*\)', re.S)
PHP_REQ_USER_AUTH_RE = re.compile(r'\$request->user\(|auth\(\)|Auth::|->middleware\(\s*[\'"]auth')
PHP_ROUTE_NAME_TOKEN_RE = re.compile(r'[\'"]([^\'"]+)[\'"]')
PHP_CLASS_RE = re.compile(r'class\s+([A-Za-z0-9_]+)')
PHP_USE_CONTROLLER_RE = re.compile(r'use\s+([A-Za-z0-9_\\]+Controller);')


def extract_first_path(raw_args: Optional[str]) -> Optional[str]:
    if not raw_args:
        return None
    for pat in [re.compile(r'(?:value|path)\s*=\s*[\'"]([^\'"]+)[\'"]'), re.compile(r'[\'"]([^\'"]+)[\'"]')]:
        m = pat.search(raw_args)
        if m:
            return m.group(1)
    return None


def extract_request_mapping_methods(raw_args: str) -> List[str]:
    return uniq(re.findall(r'RequestMethod\.([A-Z]+)', raw_args))


def extract_java_type_name(block: str, annotation: str) -> Optional[str]:
    m = re.search(rf'@{annotation}\s+([A-Za-z0-9_$.<>?, ]+)\s+([A-Za-z_][A-Za-z0-9_]*)', block)
    if not m:
        return None
    type_expr = re.sub(r'<.*>', '', m.group(1).strip().split()[-1])
    return type_expr.split('.')[-1]


def ant_pattern_to_regex(pattern: str) -> re.Pattern:
    escaped = re.escape(normalize_path(pattern)).replace(r'\*\*', '.*').replace(r'\*', '[^/]+').replace(r'\{\}', '[^/]+')
    return re.compile(r'^' + escaped + r'$')


def build_java_dto_index(root: Path) -> Dict[str, List[str]]:
    dto_index: Dict[str, List[str]] = {}
    for path in iter_files(root):
        if path.suffix.lower() not in {'.java', '.kt'}:
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        for m in JAVA_RECORD_RE.finditer(text):
            field_names = []
            for part in split_top_level(m.group(2)):
                cleaned = re.sub(r'@[A-Za-z0-9_().," =]+', ' ', part)
                names = re.findall(r'([A-Za-z_][A-Za-z0-9_]*)\s*$', cleaned.strip())
                if names:
                    field_names.append(names[-1])
            if field_names:
                dto_index[m.group(1)] = uniq(field_names)
        for m in JAVA_CLASS_RE.finditer(text):
            brace_start = text.find('{', m.start())
            brace_end = find_matching(text, brace_start, '{', '}')
            if brace_start < 0 or brace_end < 0:
                continue
            fields = uniq(JAVA_FIELD_RE.findall(text[brace_start + 1:brace_end]))
            if fields:
                dto_index.setdefault(m.group(1), fields)
    return dto_index


def extract_security_rules(root: Path) -> List[Tuple[re.Pattern, RequestHints]]:
    rules: List[Tuple[re.Pattern, RequestHints]] = []
    for path in iter_files(root):
        if path.suffix.lower() not in {'.java', '.kt'}:
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        if 'SecurityFilterChain' not in text or 'authorizeHttpRequests' not in text:
            continue
        for m in re.finditer(r'\.requestMatchers\((.*?)\)\s*\.(permitAll|authenticated|hasRole|hasAnyRole)\s*\(', text, re.S):
            args, action = m.group(1), m.group(2)
            for raw in re.findall(r'[\'"]([^\'"]+/[^\'"]*)[\'"]', args):
                hints = RequestHints()
                if action == 'permitAll':
                    hints.auth.append('permit-all')
                if action in {'authenticated', 'hasRole', 'hasAnyRole'}:
                    hints.auth.append('authenticated-route')
                if action in {'hasRole', 'hasAnyRole'}:
                    hints.auth.append('role-guard')
                rules.append((ant_pattern_to_regex(raw), hints))
        any_req = re.search(r'\.anyRequest\(\)\.(permitAll|authenticated)\s*\(', text)
        if any_req and any_req.group(1) == 'authenticated':
            rules.append((re.compile(r'^/.*'), RequestHints(auth=['authenticated-route'])))
    return rules


def match_security_hints(path: str, rules: List[Tuple[re.Pattern, RequestHints]]) -> RequestHints:
    hints = RequestHints()
    for pattern, rule_hints in rules:
        if pattern.match(normalize_path(path)):
            hints.auth.extend(rule_hints.auth)
    hints.auth = uniq(hints.auth)
    if 'permit-all' in hints.auth:
        hints.auth = [x for x in hints.auth if x not in {'permit-all', 'authenticated-route', 'role-guard'}]
    return hints


def extract_response_type_name(nearby_block: str) -> Optional[str]:
    m = RETURN_TYPE_RE.search(nearby_block)
    if not m:
        return None
    type_expr = m.group(1).strip()
    generic_match = re.search(r'(?:ResponseEntity|ApiResponse|CommonResponse|BaseResponse)\s*<\s*([A-Za-z0-9_$.]+)', type_expr)
    if generic_match:
        return generic_match.group(1).split('.')[-1]
    type_expr = re.sub(r'<.*>', '', type_expr).strip().split()[-1]
    simple = type_expr.split('.')[-1]
    if simple in {'void', 'Void', 'ResponseEntity'}:
        return None
    return simple


def infer_backend_hints(raw_path: str, source: str, nearby_block: str, dto_index: Dict[str, List[str]], security_hints: Optional[RequestHints] = None) -> RequestHints:
    hints = RequestHints()
    path_matches = re.findall(r'@PathVariable(?:\([^)]*name\s*=\s*"([^"]+)"[^)]*\)|\(\s*"([^"]+)"\s*\))?\s+[A-Za-z0-9_<>?,. ]+\s+([A-Za-z_][A-Za-z0-9_]*)', nearby_block)
    flat = []
    for triple in path_matches:
        flat.extend([x for x in triple if x])
    hints.path_params = uniq(flat) or extract_path_param_names(raw_path)
    query_names = []
    for m in re.finditer(r'@RequestParam(?:\([^)]*name\s*=\s*"([^"]+)"[^)]*\)|\(\s*"([^"]+)"\s*\))?\s+[A-Za-z0-9_<>?,. ]+\s+([A-Za-z_][A-Za-z0-9_]*)', nearby_block):
        values = [x for x in m.groups() if x]
        query_names.append(values[0] if values else '')
    if 'Pageable' in nearby_block:
        query_names.extend(['page', 'size', 'sort'])
    hints.query_params = uniq([q for q in query_names if q])
    if '@RequestBody' in nearby_block:
        hints.body_kind = 'request-body'
        dto_type = extract_java_type_name(nearby_block, 'RequestBody')
        if dto_type:
            hints.body_keys = dto_index.get(dto_type, [])
    if '@RequestPart' in nearby_block:
        hints.body_kind = 'multipart'
        hints.consumes = 'multipart/form-data'
        hints.body_keys = uniq([p for p in re.findall(r'@RequestPart(?:\(\s*"([^"]+)"\s*\))?', nearby_block) if p])
    if re.search(r'consumes\s*=\s*MediaType\.MULTIPART_FORM_DATA_VALUE', source):
        hints.consumes = 'multipart/form-data'
    response_type = extract_response_type_name(nearby_block)
    if response_type:
        hints.response_keys = dto_index.get(response_type, [])
    if '@AuthenticationPrincipal' in nearby_block:
        hints.auth.append('authentication-principal')
    if '@RequestHeader' in nearby_block:
        hints.auth.append('request-header')
    if re.search(r'PreAuthorize|Secured|RolesAllowed', nearby_block):
        hints.auth.append('role-guard')
    if security_hints:
        hints.auth.extend(security_hints.auth)
    hints.auth = uniq(hints.auth)
    return hints


def extract_method_block(text: str, mapping_pos: int) -> str:
    pub_pos = text.find('public ', mapping_pos)
    if pub_pos < 0:
        return text[mapping_pos:mapping_pos + 800]
    brace_start = text.find('{', pub_pos)
    if brace_start < 0:
        return text[mapping_pos:pub_pos + 400]
    brace_end = find_matching(text, brace_start, '{', '}')
    if brace_end < 0:
        return text[mapping_pos:brace_start + 400]
    return text[mapping_pos:brace_end + 1]


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


def build_js_const_path_index(text: str) -> Dict[str, str]:
    consts: Dict[str, str] = {}
    changed = True
    while changed:
        changed = False
        for m in JS_VAR_ASSIGN_RE.finditer(text):
            name, expr = m.group(1), m.group(2).strip()
            path_value = extract_js_path_expr(expr, consts)
            if path_value and consts.get(name) != path_value:
                consts[name] = path_value
                changed = True
    return consts


def extract_js_path_expr(expr: str, const_paths: Optional[Dict[str, str]] = None) -> Optional[str]:
    expr = expr.strip()
    if not expr:
        return None
    literal = re.match(r'^[\'"]([^\'"]+)[\'"]$', expr, re.S)
    if literal:
        return literal.group(1)
    template = re.match(r'^`([^`]+)`$', expr, re.S)
    if template:
        return template.group(1)
    if const_paths and expr in const_paths:
        return const_paths[expr]
    parts = split_top_level(expr, '+')
    if len(parts) > 1:
        resolved: List[str] = []
        for part in parts:
            part = part.strip()
            literal = extract_js_path_expr(part, const_paths)
            if literal is None:
                return None
            resolved.append(literal)
        return ''.join(resolved)
    return None


def extract_express_router_vars(text: str) -> set[str]:
    return set(EXPRESS_ROUTER_CREATE_RE.findall(text))


def infer_express_hints(raw_path: str, block: str, middleware_args: List[str]) -> RequestHints:
    hints = RequestHints()
    hints.path_params = uniq(extract_path_param_names(raw_path) + REQ_PARAM_ACCESS_RE.findall(block))
    hints.query_params = uniq(REQ_QUERY_ACCESS_RE.findall(block))
    hints.body_keys = uniq(REQ_BODY_ACCESS_RE.findall(block))
    if hints.body_keys or 'req.body' in block:
        hints.body_kind = 'request-body'
    if 'req.files' in block or 'req.file' in block or MULTER_CALL_RE.search(' '.join(middleware_args)):
        hints.body_kind = 'multipart'
        hints.consumes = 'multipart/form-data'
    if REQ_HEADER_ACCESS_RE.search(block) or 'authorization' in block.lower() or 'bearer ' in block.lower():
        hints.auth.append('request-header')
    if re.search(r'jwt|passport|requireAuth|isAuthenticated|authenticate', block, re.I):
        hints.auth.append('authenticated-route')
    hints.auth = uniq(hints.auth)
    return hints


def extract_callback_block(text: str, handler_expr: str, call_start: int) -> str:
    arrow_pos = text.find('=>', call_start)
    if arrow_pos != -1 and arrow_pos < call_start + 800:
        brace_start = text.find('{', arrow_pos)
        if brace_start != -1:
            brace_end = find_matching(text, brace_start, '{', '}')
            if brace_end != -1:
                return text[brace_start:brace_end + 1]
    fn_start = text.find('function', call_start)
    if fn_start != -1 and fn_start < call_start + 800:
        brace_start = text.find('{', fn_start)
        if brace_start != -1:
            brace_end = find_matching(text, brace_start, '{', '}')
            if brace_end != -1:
                return text[brace_start:brace_end + 1]
    if handler_expr:
        named = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)$', handler_expr.strip())
        if named:
            name = named.group(1)
            for pat in [
                re.compile(rf'function\s+{re.escape(name)}\s*\([^)]*\)\s*\{{'),
                re.compile(rf'(?:const|let|var)\s+{re.escape(name)}\s*=\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{{'),
            ]:
                m = pat.search(text)
                if m:
                    brace_start = text.find('{', m.start())
                    brace_end = find_matching(text, brace_start, '{', '}')
                    if brace_start != -1 and brace_end != -1:
                        return text[brace_start:brace_end + 1]
    return ''


def apply_prefix(prefix: str, raw_path: str) -> str:
    if not prefix:
        return raw_path
    if not raw_path:
        return prefix
    return (prefix.rstrip('/') + '/' + raw_path.lstrip('/')).replace('//', '/')


def extract_express_endpoints(root: Path) -> List[EndpointIR]:
    endpoints: List[EndpointIR] = []
    for path in iter_files(root):
        if path.suffix.lower() not in {'.js', '.jsx', '.ts', '.tsx'}:
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        if not any(marker in text for marker in ['express.Router(', 'Router()', "from 'express'", 'require(\'express\')', 'require("express")']):
            continue
        const_paths = build_js_const_path_index(text)
        router_vars = extract_express_router_vars(text)
        mount_prefixes: Dict[str, List[str]] = {}

        for seg in find_call_segments(text, EXPRESS_USE_CALL_RE, 'express-use'):
            receiver = seg['match'].group(1)
            args = seg['args']
            if len(args) < 2:
                continue
            prefix = extract_js_path_expr(args[0], const_paths)
            if not prefix:
                continue
            for arg in args[1:]:
                name_match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)$', arg.strip())
                if name_match and name_match.group(1) in router_vars:
                    mount_prefixes.setdefault(name_match.group(1), []).append(prefix)
            if receiver in router_vars:
                mount_prefixes.setdefault(receiver, []).append(prefix)

        for seg in find_call_segments(text, EXPRESS_METHOD_CALL_RE, 'express-method'):
            receiver = seg['match'].group(1)
            method = seg['match'].group(2).upper()
            args = seg['args']
            if not args:
                continue
            raw_path = extract_js_path_expr(args[0], const_paths)
            if raw_path is None:
                continue
            middleware_args = args[1:-1] if len(args) >= 3 else []
            handler_expr = args[-1] if len(args) >= 2 else ''
            block = extract_callback_block(text, handler_expr, seg['start'])
            base_prefixes = mount_prefixes.get(receiver, ['']) if receiver in router_vars else ['']
            for prefix in base_prefixes:
                combined_raw = apply_prefix(prefix, raw_path)
                normalized = normalize_path(combined_raw)
                hints = infer_express_hints(combined_raw, block, middleware_args)
                endpoints.append(EndpointIR(
                    side='backend', method=method, path=normalized, raw_path=combined_raw,
                    file=str(path), line=seg['line'], source=seg['source'], locator=f'{receiver}.{method.lower()}',
                    framework='express', confidence='medium', hints=hints,
                ))

        for seg in find_call_segments(text, EXPRESS_ROUTE_CALL_RE, 'express-route'):
            receiver = seg['match'].group(1)
            args = seg['args']
            if not args:
                continue
            raw_path = extract_js_path_expr(args[0], const_paths)
            if raw_path is None:
                continue
            paren_start = text.find('(', seg['start'])
            paren_end = find_matching(text, paren_start, '(', ')') if paren_start != -1 else -1
            route_chain = text[paren_end + 1: min(len(text), paren_end + 1200)] if paren_end != -1 else ''
            base_prefixes = mount_prefixes.get(receiver, ['']) if receiver in router_vars else ['']
            for mm in re.finditer(r'\.\s*(get|post|put|patch|delete)\s*\(', route_chain):
                method = mm.group(1).upper()
                call_abs = (paren_end + 1 if paren_end != -1 else seg['start']) + mm.start()
                method_paren = text.find('(', call_abs)
                method_end = find_matching(text, method_paren, '(', ')') if method_paren != -1 else -1
                if method_end == -1:
                    continue
                inner_args = split_top_level(text[method_paren + 1:method_end])
                middleware_args = inner_args[:-1] if len(inner_args) >= 2 else []
                handler_expr = inner_args[-1] if inner_args else ''
                block = extract_callback_block(text, handler_expr, call_abs)
                for prefix in base_prefixes:
                    combined_raw = apply_prefix(prefix, raw_path)
                    normalized = normalize_path(combined_raw)
                    hints = infer_express_hints(combined_raw, block, middleware_args)
                    endpoints.append(EndpointIR(
                        side='backend', method=method, path=normalized, raw_path=combined_raw,
                        file=str(path), line=line_of(text, call_abs), source=text[call_abs:method_end + 1].strip(), locator=f'{receiver}.route.{method.lower()}',
                        framework='express', confidence='medium', hints=hints,
                    ))
    return endpoints


def extract_spring_endpoints(root: Path, dto_index: Optional[Dict[str, List[str]]] = None, security_rules: Optional[List[Tuple[re.Pattern, RequestHints]]] = None) -> List[EndpointIR]:
    dto_index = dto_index or build_java_dto_index(root)
    security_rules = security_rules or extract_security_rules(root)
    endpoints: List[EndpointIR] = []
    for path in iter_files(root):
        if path.suffix.lower() not in {'.java', '.kt'}:
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        class_prefix = ''
        controller = path.stem
        cm = CLASS_RE.search(text)
        if cm:
            controller = cm.group(1)
        class_request_match = REQUEST_MAPPING_RE.search(text)
        if class_request_match:
            class_prefix = normalize_path(extract_first_path(class_request_match.group(1)) or '')
            if class_prefix == '/':
                class_prefix = ''
        method_positions = [(mm.start(), mm.group(1)) for mm in METHOD_RE.finditer(text)]

        def nearest_handler(pos: int) -> str:
            for start, method_name in method_positions:
                if start >= pos:
                    return method_name
            return 'unknown'

        for m in MAPPING_RE.finditer(text):
            verb = m.group(1).upper()
            sub = extract_first_path(m.group(2)) or ''
            full_raw = (class_prefix + '/' + sub.lstrip('/')).replace('//', '/') if sub else (class_prefix or '/')
            full = normalize_path(full_raw)
            block = extract_method_block(text, m.start())
            hints = infer_backend_hints(full_raw, m.group(0).strip(), block, dto_index, match_security_hints(full_raw, security_rules))
            endpoints.append(EndpointIR(side='backend', method=verb, path=full, raw_path=full_raw, file=str(path), line=line_of(text, m.start()), source=m.group(0).strip(), locator=f'{controller}.{nearest_handler(m.start())}', framework='spring', confidence='high', hints=hints))
        for m in REQUEST_MAPPING_RE.finditer(text):
            methods = extract_request_mapping_methods(m.group(1))
            if not methods:
                continue
            sub = extract_first_path(m.group(1)) or ''
            full_raw = (class_prefix + '/' + sub.lstrip('/')).replace('//', '/') if sub else (class_prefix or '/')
            full = normalize_path(full_raw)
            block = extract_method_block(text, m.start())
            for verb in methods:
                hints = infer_backend_hints(full_raw, m.group(0).strip(), block, dto_index, match_security_hints(full_raw, security_rules))
                endpoints.append(EndpointIR(side='backend', method=verb.upper(), path=full, raw_path=full_raw, file=str(path), line=line_of(text, m.start()), source=m.group(0).strip(), locator=f'{controller}.{nearest_handler(m.start())}', framework='spring', confidence='high', hints=hints))
    return endpoints


def find_php_controller_file(root: Path, controller_fqcn: str) -> Optional[Path]:
    simple = controller_fqcn.split('\\')[-1]
    candidates = [
        root / 'app' / 'Http' / 'Controllers' / f'{simple}.php',
        root / 'src' / 'Http' / 'Controllers' / f'{simple}.php',
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    for path in iter_files(root):
        if path.suffix.lower() != '.php':
            continue
        if path.name == f'{simple}.php':
            return path
    return None


def extract_php_method_block(text: str, method_name: str) -> str:
    for m in PHP_METHOD_DEF_RE.finditer(text):
        if m.group(1) != method_name:
            continue
        brace_start = text.find('{', m.end() - 1)
        brace_end = find_matching(text, brace_start, '{', '}') if brace_start != -1 else -1
        if brace_start != -1 and brace_end != -1:
            return text[brace_start:brace_end + 1]
    return ''


def extract_php_method_signature(text: str, method_name: str) -> str:
    for m in PHP_METHOD_DEF_RE.finditer(text):
        if m.group(1) == method_name:
            return m.group(2)
    return ''


def extract_php_validate_keys(block: str) -> List[str]:
    keys: List[str] = []
    for chunk in PHP_REQ_VALIDATE_KEY_RE.findall(block):
        keys.extend(re.findall(r'[\'"]([A-Za-z_][A-Za-z0-9_.-]*)[\'"]\s*=>', chunk))
    return uniq(keys)


def infer_laravel_hints(raw_path: str, route_source: str, controller_file: Optional[Path], action: Optional[str], middleware: List[str]) -> RequestHints:
    hints = RequestHints()
    hints.path_params = extract_path_param_names(raw_path)
    block = ''
    signature = ''
    if controller_file and action:
        text = controller_file.read_text(encoding='utf-8', errors='ignore')
        block = extract_php_method_block(text, action)
        signature = extract_php_method_signature(text, action)
        hints.query_params = uniq(PHP_REQ_QUERY_RE.findall(block))
        hints.body_keys = uniq(PHP_REQ_INPUT_RE.findall(block) + extract_php_validate_keys(block))
        if hints.body_keys or '$request->all(' in block or '$request->validated(' in block:
            hints.body_kind = 'request-body'
        if 'UploadedFile' in signature or '$request->file(' in block:
            hints.body_kind = 'multipart'
            hints.consumes = 'multipart/form-data'
        if PHP_REQ_USER_AUTH_RE.search(block):
            hints.auth.append('authenticated-route')
    if any('auth' in item.lower() or 'sanctum' in item.lower() or 'verified' in item.lower() for item in middleware):
        hints.auth.append('authenticated-route')
    if 'auth:' in route_source.lower() or 'middleware(' in route_source.lower() and 'auth' in route_source.lower():
        hints.auth.append('authenticated-route')
    hints.auth = uniq(hints.auth)
    return hints


def extract_php_string_arg(args: List[str], index: int) -> Optional[str]:
    if index >= len(args):
        return None
    m = re.match(r'^[\'"]([^\'"]+)[\'"]$', args[index].strip(), re.S)
    return m.group(1) if m else None


def extract_laravel_group_blocks(text: str) -> List[Tuple[int, int, str, List[str]]]:
    blocks: List[Tuple[int, int, str, List[str]]] = []
    for seg in find_call_segments(text, LARAVEL_PREFIX_GROUP_RE, 'laravel-prefix'):
        args = seg['args']
        prefix = extract_php_string_arg(args, 0) or ''
        call_end = seg['start'] + len(seg['source'])
        group_match = re.search(r'->\s*middleware\s*\((.*?)\)', text[seg['start']: seg['start'] + 500], re.S)
        middleware = []
        if group_match:
            middleware = PHP_ROUTE_NAME_TOKEN_RE.findall(group_match.group(1))
        group_pos = text.find('->group', call_end - 10)
        if group_pos == -1 or group_pos > seg['start'] + 800:
            continue
        brace_start = text.find('{', group_pos)
        brace_end = find_matching(text, brace_start, '{', '}') if brace_start != -1 else -1
        if brace_start != -1 and brace_end != -1:
            blocks.append((brace_start, brace_end, prefix, middleware))
    return blocks


def active_laravel_prefix(pos: int, groups: List[Tuple[int, int, str, List[str]]]) -> Tuple[str, List[str]]:
    prefixes: List[str] = []
    middleware: List[str] = []
    for start, end, prefix, group_middleware in groups:
        if start <= pos <= end:
            prefixes.append(prefix)
            middleware.extend(group_middleware)
    combined = '/'.join([p.strip('/') for p in prefixes if p.strip('/')])
    return combined, uniq(middleware)


def laravel_resource_routes(name: str, api_only: bool) -> List[Tuple[str, str]]:
    base = '/' + name.strip('/')
    item = base + '/{id}'
    routes = [
        ('GET', base),
        ('POST', base),
        ('GET', item),
        ('PUT', item),
        ('PATCH', item),
        ('DELETE', item),
    ]
    if api_only:
        return routes
    return [('GET', base + '/create')] + routes[:2] + [('GET', item)] + [('GET', item + '/edit')] + routes[3:]


def extract_laravel_endpoints(root: Path) -> List[EndpointIR]:
    endpoints: List[EndpointIR] = []
    route_files = [p for p in iter_files(root) if p.suffix.lower() == '.php' and 'routes' in p.parts]
    for path in route_files:
        text = path.read_text(encoding='utf-8', errors='ignore')
        groups = extract_laravel_group_blocks(text)

        for seg in find_call_segments(text, LARAVEL_ROUTE_DIRECT_RE, 'laravel-route'):
            method = seg['match'].group(1).upper()
            args = seg['args']
            raw_path = extract_php_string_arg(args, 0)
            if raw_path is None:
                continue
            prefix, group_middleware = active_laravel_prefix(seg['start'], groups)
            action_match = LARAVEL_CONTROLLER_ACTION_RE.search(seg['source'])
            controller_file = None
            action = None
            if action_match:
                controller_file = find_php_controller_file(root, action_match.group(1))
                action = action_match.group(2)
            combined_raw = apply_prefix(prefix, raw_path)
            hints = infer_laravel_hints(combined_raw, seg['source'], controller_file, action, group_middleware)
            controller_name = action_match.group(1).split('\\')[-1] if action_match else None
            locator = f'{controller_name}.{action}' if controller_name else f'route.{method.lower()}'
            endpoints.append(EndpointIR(
                side='backend', method=method, path=normalize_path(combined_raw), raw_path=combined_raw,
                file=str(path), line=seg['line'], source=seg['source'], locator=locator,
                framework='laravel', confidence='medium', hints=hints,
            ))

        for seg in find_call_segments(text, LARAVEL_ROUTE_MATCH_RE, 'laravel-match'):
            args = seg['args']
            if len(args) < 2:
                continue
            methods = [m.upper() for m in PHP_ROUTE_NAME_TOKEN_RE.findall(args[0])]
            raw_path = extract_php_string_arg(args, 1)
            if raw_path is None:
                continue
            prefix, group_middleware = active_laravel_prefix(seg['start'], groups)
            action_match = LARAVEL_CONTROLLER_ACTION_RE.search(seg['source'])
            controller_file = find_php_controller_file(root, action_match.group(1)) if action_match else None
            action = action_match.group(2) if action_match else None
            combined_raw = apply_prefix(prefix, raw_path)
            hints = infer_laravel_hints(combined_raw, seg['source'], controller_file, action, group_middleware)
            controller_name = action_match.group(1).split('\\')[-1] if action_match else None
            locator = f'{controller_name}.{action}' if controller_name else 'route.match'
            for method in methods:
                endpoints.append(EndpointIR(
                    side='backend', method=method, path=normalize_path(combined_raw), raw_path=combined_raw,
                    file=str(path), line=seg['line'], source=seg['source'], locator=locator,
                    framework='laravel', confidence='medium', hints=hints,
                ))

        for seg in find_call_segments(text, LARAVEL_ROUTE_ANY_RE, 'laravel-any'):
            args = seg['args']
            raw_path = extract_php_string_arg(args, 0)
            if raw_path is None:
                continue
            prefix, group_middleware = active_laravel_prefix(seg['start'], groups)
            action_match = LARAVEL_CONTROLLER_ACTION_RE.search(seg['source'])
            controller_file = find_php_controller_file(root, action_match.group(1)) if action_match else None
            action = action_match.group(2) if action_match else None
            combined_raw = apply_prefix(prefix, raw_path)
            hints = infer_laravel_hints(combined_raw, seg['source'], controller_file, action, group_middleware)
            controller_name = action_match.group(1).split('\\')[-1] if action_match else None
            locator = f'{controller_name}.{action}' if controller_name else 'route.any'
            for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
                endpoints.append(EndpointIR(
                    side='backend', method=method, path=normalize_path(combined_raw), raw_path=combined_raw,
                    file=str(path), line=seg['line'], source=seg['source'], locator=locator,
                    framework='laravel', confidence='low', hints=hints,
                ))

        for seg in find_call_segments(text, LARAVEL_RESOURCE_RE, 'laravel-resource'):
            resource_kind = seg['match'].group(1).lower()
            args = seg['args']
            raw_name = extract_php_string_arg(args, 0)
            if raw_name is None:
                continue
            prefix, group_middleware = active_laravel_prefix(seg['start'], groups)
            action_match = LARAVEL_CONTROLLER_ACTION_RE.search(seg['source'])
            controller_file = find_php_controller_file(root, action_match.group(1)) if action_match else None
            for method, route_path in laravel_resource_routes(raw_name, api_only=resource_kind == 'apiresource'):
                combined_raw = apply_prefix(prefix, route_path)
                action = {
                    ('GET', '/' + raw_name.strip('/')): 'index',
                    ('POST', '/' + raw_name.strip('/')): 'store',
                    ('GET', '/' + raw_name.strip('/') + '/{id}'): 'show',
                    ('PUT', '/' + raw_name.strip('/') + '/{id}'): 'update',
                    ('PATCH', '/' + raw_name.strip('/') + '/{id}'): 'update',
                    ('DELETE', '/' + raw_name.strip('/') + '/{id}'): 'destroy',
                    ('GET', '/' + raw_name.strip('/') + '/create'): 'create',
                    ('GET', '/' + raw_name.strip('/') + '/{id}/edit'): 'edit',
                }.get((method, route_path))
                hints = infer_laravel_hints(combined_raw, seg['source'], controller_file, action, group_middleware)
                controller_name = action_match.group(1).split('\\')[-1] if action_match else None
                locator = f'{controller_name}.{action}' if controller_name and action else 'route.resource'
                endpoints.append(EndpointIR(
                    side='backend', method=method, path=normalize_path(combined_raw), raw_path=combined_raw,
                    file=str(path), line=seg['line'], source=seg['source'], locator=locator,
                    framework='laravel', confidence='medium', hints=hints,
                ))
    return endpoints


def extract_backend_endpoints(root: Path, dto_index: Optional[Dict[str, List[str]]] = None, security_rules: Optional[List[Tuple[re.Pattern, RequestHints]]] = None) -> List[EndpointIR]:
    spring_endpoints = extract_spring_endpoints(root, dto_index, security_rules)
    express_endpoints = extract_express_endpoints(root)
    laravel_endpoints = extract_laravel_endpoints(root)
    return dedupe(spring_endpoints + express_endpoints + laravel_endpoints)
