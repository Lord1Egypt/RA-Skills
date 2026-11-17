#!/usr/bin/env python3
"""Dependency-free Mealie API client for OpenClaw. Credentials come only from env."""
import argparse
import json
import mimetypes
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

METHODS = {'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'}


class ClientError(Exception):
    pass


class TextResponse(str):
    """Unstructured text, distinct from a JSON string response."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def pairs(values):
    result = []
    for value in values or []:
        key, sep, val = value.partition('=')
        if not sep or not key:
            raise ClientError('Expected KEY=VALUE')
        result.append((key, val))
    return result


def read_text(path):
    return sys.stdin.read() if path == '-' else Path(path).read_text(encoding='utf-8')


class Client:
    def __init__(self):
        self.base = os.environ.get('MEALIE_URL', '').rstrip('/')
        self.token = os.environ.get('MEALIE_API_TOKEN', '')
        parsed = urllib.parse.urlsplit(self.base)
        if (parsed.scheme not in ('http', 'https') or not parsed.netloc
                or parsed.username or parsed.password or parsed.query or parsed.fragment):
            raise ClientError('Set MEALIE_URL to an http(s) installation URL without credentials, query, or fragment')
        if not self.token:
            raise ClientError('Set MEALIE_API_TOKEN to a Mealie API token')
        self.opener = urllib.request.build_opener(NoRedirect())
        self._schema = None

    def request(self, method, path, query=(), headers=(), body=None, content_type=None, output=None):
        # Never accept another origin or path traversal, even when percent encoded.
        parsed = urllib.parse.urlsplit(path)
        decoded = path
        for _ in range(4):
            unquoted = urllib.parse.unquote(decoded)
            if unquoted == decoded:
                break
            decoded = unquoted
        clean = urllib.parse.urlsplit(decoded)
        if (parsed.scheme or parsed.netloc or parsed.query or parsed.fragment
                or clean.query or clean.fragment or '\\' in decoded
                or not (decoded.startswith('/api/') or decoded in ('/api', '/openapi.json'))
                or any(part in ('.', '..') for part in clean.path.split('/'))
                or any(ord(c) < 32 for c in decoded)):
            raise ClientError('Use an installation-relative /api/... path (or /openapi.json); use --query for query parameters')
        url = self.base + path
        if query:
            url += '?' + urllib.parse.urlencode(query)
        hdrs = {'Authorization': 'Bearer ' + self.token, 'Accept': 'application/json'}
        for key, value in headers:
            if key.lower() in ('authorization', 'host', 'cookie', 'proxy-authorization'):
                raise ClientError('Authentication and routing headers cannot be overridden')
            hdrs[key] = value
        if content_type:
            hdrs['Content-Type'] = content_type
        req = urllib.request.Request(url, data=body, headers=hdrs, method=method.upper())
        try:
            with self.opener.open(req, timeout=120) as response:
                data = response.read()
                media = response.headers.get_content_type()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='replace')
            raise ClientError(f'HTTP {exc.code} {method.upper()} {path}: {detail}') from None
        except urllib.error.URLError as exc:
            raise ClientError(f'Connection failed: {exc.reason}') from None
        if output:
            Path(output).write_bytes(data)
            return {'output': str(output), 'bytes': len(data)}
        if not data:
            return None
        if media == 'application/json' or media.endswith('+json'):
            return json.loads(data)
        if media.startswith('text/') or media in ('application/xml', 'application/x-ndjson'):
            return TextResponse(data.decode('utf-8'))
        raise ClientError('Non-text response; use --output FILE to save it')

    def schema(self):
        if self._schema is None:
            self._schema = self.request('GET', '/openapi.json')
        return self._schema


def multipart(fields, files):
    boundary = 'mealie-' + uuid.uuid4().hex
    chunks = []
    def quoted(value):
        if '\r' in value or '\n' in value:
            raise ClientError('Multipart names cannot contain newlines')
        return value.replace('\\', '\\\\').replace('"', '\\"')
    for key, value in fields:
        chunks.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{quoted(key)}"\r\n\r\n'.encode() + value.encode() + b'\r\n')
    for key, filename in files:
        file = Path(filename)
        mime = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
        chunks.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{quoted(key)}"; filename="{quoted(file.name)}"\r\nContent-Type: {mime}\r\n\r\n'.encode() + file.read_bytes() + b'\r\n')
    chunks.append(f'--{boundary}--\r\n'.encode())
    return b''.join(chunks), 'multipart/form-data; boundary=' + boundary


def payload(args):
    fields, files = pairs(args.field), pairs(args.file)
    if sum((args.json is not None, args.body is not None, bool(fields or files))) > 1:
        raise ClientError('Choose one of --json, --body, or --field/--file')
    if args.json is not None:
        value = read_text(args.json[1:]) if args.json.startswith('@') else args.json
        return json.dumps(json.loads(value)).encode(), 'application/json'
    if args.body is not None:
        return (sys.stdin.buffer.read() if args.body == '-' else Path(args.body).read_bytes()), args.content_type or 'application/octet-stream'
    if files or (fields and args.content_type != 'application/x-www-form-urlencoded'):
        return multipart(fields, files)
    if fields:
        return urllib.parse.urlencode(fields).encode(), 'application/x-www-form-urlencoded'
    return None, args.content_type


def describe(document, method, path):
    item = document.get('paths', {}).get(path, {})
    op = item.get(method.lower())
    if op is None:
        raise ClientError('Operation not found; use endpoints to discover exact methods and paths')
    refs = {}
    def visit(node):
        if isinstance(node, dict):
            ref = node.get('$ref', '')
            if ref.startswith('#/') and ref not in refs:
                target = document
                for part in ref[2:].split('/'):
                    target = target[part.replace('~1', '/').replace('~0', '~')]
                refs[ref] = target
                visit(target)
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)
    result = {'method': method.upper(), 'path': path, 'operation': op,
              'pathParameters': item.get('parameters', [])}
    visit(result)
    result['references'] = refs
    return result


def imported(client, slug):
    if not isinstance(slug, str) or not slug:
        raise ClientError('Import returned no slug; inspect recipes before trying again')
    # If this GET fails, the recipe may already exist. Never repeat the POST automatically.
    try:
        recipe = client.request('GET', '/api/recipes/' + urllib.parse.quote(slug, safe=''))
    except ClientError as exc:
        raise ClientError(f'Import created slug {slug!r}, but verification failed: {exc}. Do not re-import; fetch this slug.') from None
    return {'slug': slug, 'recipe': recipe}


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    ep = sub.add_parser('endpoints', help='List all operations advertised by this instance')
    ep.add_argument('--search', default='')
    d = sub.add_parser('describe', help='Show operation and recursively referenced schemas')
    d.add_argument('method'); d.add_argument('path')
    s = sub.add_parser('schema', help='Show full live OpenAPI or a named component schema')
    s.add_argument('name', nargs='?')
    for command in ('request', 'call'):
        r = sub.add_parser(command)
        if command == 'request':
            r.add_argument('method', choices=[m.upper() for m in sorted(METHODS)])
            r.add_argument('route')
        else:
            r.add_argument('operation_id')
            r.add_argument('--path', action='append', default=[])
        for name in ('query', 'header', 'field', 'file'):
            r.add_argument('--' + name, action='append', default=[])
        r.add_argument('--json'); r.add_argument('--body')
        r.add_argument('--content-type'); r.add_argument('--output')
    for command in ('import-url', 'import-recipe'):
        r = sub.add_parser(command)
        r.add_argument('source')
        r.add_argument('--include-tags', action='store_true')
        r.add_argument('--include-categories', action='store_true')
        if command == 'import-recipe':
            r.add_argument('--source-url')
    a = sub.add_parser('import-ai', help='Use optional server AI; may send data to its configured provider')
    a.add_argument('--content'); a.add_argument('--url')
    a.add_argument('--image', action='append', default=[])
    a.add_argument('--language')
    e = sub.add_parser('extract-pdf', help='Extract text locally using optional pdftotext; scanned PDFs need vision/OCR')
    e.add_argument('file')
    return p


def run(args):
    if args.command == 'extract-pdf':
        result = subprocess.run(['pdftotext', '-layout', str(Path(args.file).resolve()), '-'], capture_output=True)
        if result.returncode:
            raise ClientError(result.stderr.decode(errors='replace'))
        text = result.stdout.decode('utf-8')
        if not text.strip():
            raise ClientError('PDF has no extractable text; render pages and use OpenClaw vision/OCR')
        return TextResponse(text)
    client = Client()
    if args.command == 'schema':
        doc = client.schema()
        if args.name:
            if args.name not in doc.get('components', {}).get('schemas', {}):
                raise ClientError('Unknown schema name')
            return doc['components']['schemas'][args.name]
        return doc
    if args.command == 'endpoints':
        result = []
        for path, item in client.schema()['paths'].items():
            for method, op in item.items():
                if method in METHODS:
                    row = {'method': method.upper(), 'path': path, 'operationId': op.get('operationId'),
                           'summary': op.get('summary'), 'tags': op.get('tags', [])}
                    if args.search.lower() in json.dumps(row).lower():
                        result.append(row)
        return result
    if args.command == 'describe':
        return describe(client.schema(), args.method, args.path)
    if args.command in ('request', 'call'):
        if args.command == 'request':
            method, path = args.method, args.route
        else:
            matches = [(m, p) for p, item in client.schema()['paths'].items()
                       for m, op in item.items() if m in METHODS and op.get('operationId') == args.operation_id]
            if len(matches) != 1:
                raise ClientError('Operation ID must match exactly one live endpoint')
            method, path = matches[0]
            supplied = dict(pairs(args.path))
            needed = set(re.findall(r'\{([^}]+)\}', path))
            if needed != set(supplied):
                raise ClientError('Supply exactly these --path keys: ' + ', '.join(sorted(needed)))
            path = re.sub(r'\{([^}]+)\}', lambda m: urllib.parse.quote(supplied[m[1]], safe=''), path)
        body, content_type = payload(args)
        return client.request(method, path, pairs(args.query), pairs(args.header), body, content_type, args.output)
    if args.command in ('import-url', 'import-recipe'):
        body = {'includeTags': args.include_tags, 'includeCategories': args.include_categories}
        if args.command == 'import-url':
            body['url'] = args.source
            path = '/api/recipes/create/url'
        else:
            body['data'] = read_text(args.source)
            if args.source_url:
                body['url'] = args.source_url
            path = '/api/recipes/create/html-or-json'
        slug = client.request('POST', path, body=json.dumps(body).encode(), content_type='application/json')
        return imported(client, slug)
    if args.command == 'import-ai':
        if not (args.content or args.url or args.image):
            raise ClientError('Supply --content, --url, or --image')
        fields = []
        if args.content:
            fields.append(('content', read_text(args.content)))
        if args.url:
            fields.append(('url', args.url))
        if args.language:
            fields.append(('translateLanguage', args.language))
        body, content_type = multipart(fields, [('images', f) for f in args.image])
        return imported(client, client.request('POST', '/api/recipes/create/ai', body=body, content_type=content_type))


def main():
    args = parser().parse_args()
    try:
        value = run(args)
        if isinstance(value, TextResponse):
            print(value)
        else:
            print(json.dumps(value, ensure_ascii=False, indent=2))
        return 0
    except (ClientError, OSError, ValueError, KeyError) as exc:
        # Redact even if the remote error response echoes the Authorization value.
        message = str(exc)
        token = os.environ.get('MEALIE_API_TOKEN')
        if token:
            message = message.replace(token, '[REDACTED]')
        print(json.dumps({'error': message}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
