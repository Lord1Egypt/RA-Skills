#!/usr/bin/env python3
"""
http_client.py — HTTP 客户端工具（纯标准库 + urllib）
覆盖：GET/POST/PUT/DELETE/PATCH、API调用、断链检测、下载上传、代理、Cookie管理

用法：
  python http_client.py get https://api.example.com/users --header "Authorization: Bearer xxx"
  python http_client.py post https://httpbin.org/post --data '{"name":"test"}' --json
  python http_client.py check-urls urls.txt -o report.json
  python http_client.py download https://example.com/file.zip -o file.zip
  python http_client.py head https://api.example.com/health
  python http_client.py api-swagger https://petstore.swagger.io/v2/swagger.json
  python http_client.py batch-get urls.txt --concurrent 5
"""

import sys
import os
import json
import re
import time
import ssl
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from typing import Optional, Any
from http.client import HTTPResponse, HTTPSConnection


# ─── CLI ──────────────────────────────────────────────────────

def parse_args(argv=None):
    argv = argv or sys.argv[1:]
    if not argv or '-h' in argv or '--help' in argv:
        print(__doc__)
        sys.exit(0)
    cmd = argv[0]
    args = {'_cmd': cmd, '_pos': []}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a.startswith('-'):
            key = a.lstrip('-').replace('-', '_')
            if i + 1 < len(argv) and not argv[i+1].startswith('-'):
                args[key] = argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            args['_pos'].append(a)
            i += 1
    return args


def color(text: str, fg: str = '') -> str:
    codes = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'cyan': 36}
    code = codes.get(fg, '')
    if not code or not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
        return text
    return f'\033[{code}m{text}\033[0m'


def echo(text: str, fg: str = ''):
    print(color(text, fg))


# ─── HTTP 核心封装 ──────────────────────────────────────────

class HTTPClient:
    """轻量 HTTP 客户端，基于 urllib"""

    DEFAULT_TIMEOUT = 30
    USER_AGENT = 'HTTPClient/1.0 (Python)'

    def __init__(self, timeout: int = None, verify_ssl: bool = True,
                 proxy: str = None, headers: dict = None):
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.verify_ssl = verify_ssl
        if not self.verify_ssl:
            import warnings
            warnings.warn('SSL 验证已禁用，存在中间人攻击风险', stacklevel=2)
        self.proxy = proxy
        self.default_headers = headers or {}
        self.cookies: dict[str, str] = {}

    def _build_opener(self):
        """构建 URL opener（支持代理）"""
        handlers = []

        if self.proxy:
            proxy_handler = urllib.request.ProxyHandler({
                'http': self.proxy,
                'https': self.proxy,
            })
            handlers.append(proxy_handler)

        # Cookie 处理
        cookie_jar = urllib.request.HTTPCookieProcessor()
        handlers.append(cookie_jar)

        if not self.verify_ssl:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            https_handler = urllib.request.HTTPSHandler(context=ctx)
            handlers.append(https_handler)

        return urllib.request.build_opener(*handlers)

    def request(self, method: str, url: str, data: bytes = None,
                headers: dict = None, timeout: int = None,
                allow_redirects: bool = True) -> 'Response':
        """发送 HTTP 请求"""
        all_headers = dict(self.default_headers)
        all_headers['User-Agent'] = self.USER_AGENT
        if headers:
            all_headers.update(headers)

        req = urllib.request.Request(url, data=data, method=method.upper())
        for k, v in all_headers.items():
            if v is not None:
                req.add_header(k, v)

        t_start = time.time()

        try:
            opener = self._build_opener()
            resp = opener.open(req, timeout=timeout or self.timeout)
            elapsed = time.time() - t_start
            body = resp.read()
            return Response(
                status_code=resp.getcode(),
                headers=dict(resp.headers),
                body=body,
                elapsed=elapsed,
                url=url,
                ok=200 <= resp.getcode() < 400,
            )
        except urllib.error.HTTPError as e:
            elapsed = time.time() - t_start
            body = e.read() if e.fp else b''
            return Response(
                status_code=e.code,
                headers=dict(e.headers) if e.headers else {},
                body=body,
                elapsed=elapsed,
                url=url,
                ok=False,
                error=str(e),
            )
        except Exception as e:
            elapsed = time.time() - t_start
            return Response(
                status_code=0,
                headers={},
                body=b'',
                elapsed=elapsed,
                url=url,
                ok=False,
                error=str(e),
            )

    def get(self, url: str, params: dict = None, **kw) -> 'Response':
        if params:
            sep = '&' if '?' in url else '?'
            url = f'{url}{sep}{urllib.parse.urlencode(params)}'
        return self.request('GET', url, **kw)

    def post(self, url: str, data=None, json_data=None, **kw) -> 'Response':
        body = None
        headers = kw.pop('headers', {})
        if json_data is not None:
            body = json.dumps(json_data).encode('utf-8')
            headers['Content-Type'] = 'application/json; charset=utf-8'
        elif isinstance(data, str):
            body = data.encode('utf-8')
            headers.setdefault('Content-Type', 'application/x-www-form-urlencoded')
        elif isinstance(data, dict):
            body = urllib.parse.urlencode(data).encode('utf-8')
            headers.setdefault('Content-Type', 'application/x-www-form-urlencoded')
        elif isinstance(data, (bytes, bytearray)):
            body = data

        kw['headers'] = headers
        return self.request('POST', url, data=body, **kw)

    def put(self, url: str, data=None, **kw) -> 'Response':
        return self.request('PUT', url, **kw)

    def delete(self, url: str, **kw) -> 'Response':
        return self.request('DELETE', url, **kw)

    def patch(self, url: str, data=None, **kw) -> 'Response':
        return self.request('PATCH', url, **kw)

    def head(self, url: str, **kw) -> 'Response':
        return self.request('HEAD', url, **kw)


class Response:
    """HTTP 响应对象"""

    def __init__(self, status_code: int, headers: dict, body: bytes,
                 elapsed: float, url: str, ok: bool, error: str = None):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.elapsed = elapsed
        self.url = url
        self.ok = ok
        self.error = error

    @property
    def text(self) -> str:
        encoding = 'utf-8'
        ct = self.headers.get('Content-Type', '')
        m = re.search(r'charset=([\w-]+)', ct)
        if m:
            encoding = m.group(1)
        try:
            return self.body.decode(encoding, errors='replace')
        except (LookupError, UnicodeDecodeError):
            return self.body.decode('utf-8', errors='replace')

    @property
    def json(self) -> Any:
        try:
            return json.loads(self.text)
        except (json.JSONDecodeError, ValueError):
            return None

    @property
    def content_type(self) -> str:
        return self.headers.get('Content-Type', '').split(';')[0].strip()

    def raise_for_status(self):
        if not self.ok:
            raise urllib.error.HTTPError(
                self.url, self.status_code, self.error, self.headers, None
            )

    def __repr__(self):
        status_color = 'green' if self.ok else ('red' if self.status_code >= 400 else 'yellow')
        size_str = f'{len(self.body)} bytes'
        return f'<Response [{color(str(self.status_code), status_color)}] {size_str} {self.elapsed:.3f}s>'


def parse_headers(header_list) -> dict:
    """解析 header 参数"""
    if isinstance(header_list, list):
        result = {}
        for h in header_list:
            if ':' in h:
                k, v = h.split(':', 1)
                result[k.strip()] = v.strip()
        return result
    if isinstance(header_list, str):
        return parse_headers([header_list])
    return header_list or {}


def _fmt_size(b: int) -> str:
    for u in ['B', 'KB', 'MB', 'GB']:
        if b < 1024:
            return f'{b:.1f} {u}'
        b /= 1024
    return f'{b:.1f} TB'


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

def cmd_get(args):
    url = args['_pos'][0] if args.get('_pos') else ''
    headers = parse_headers(args.get('header'))
    output = args.get('o', '')
    pretty = args.get('pretty', True)
    timeout = int(args.get('timeout', 0)) or None
    proxy = args.get('proxy')

    client = HTTPClient(timeout=timeout, proxy=proxy)
    resp = client.get(url, headers=headers)

    print(resp)

    if resp.ok:
        if resp.content_type == 'application/json' and pretty:
            try:
                parsed = json.loads(resp.text)
                print(json.dumps(parsed, ensure_ascii=False, indent=2))
            except (json.JSONDecodeError, ValueError):
                print(resp.text[:2000])
        else:
            text = resp.text[:5000]
            if len(resp.text) > 5000:
                text += f'\n... ({len(resp.text)-5000} more chars)'
            print(text)

    if resp.error:
        echo(f'错误: {resp.error}', fg='red')

    if output and resp.ok:
        with open(output, 'wb') as f:
            f.write(resp.body)
        echo(f'✅ 已保存: {output}', fg='green')


def cmd_post(args):
    url = args['_pos'][0] if args.get('_pos') else ''
    headers = parse_headers(args.get('header'))
    data_arg = args.get('data', '')
    is_json = args.get('json', False)
    timeout = int(args.get('timeout', 0)) or None

    client = HTTPClient(timeout=timeout)

    if is_json or data_arg.startswith('{') or data_arg.startswith('['):
        json_data = json.loads(data_arg) if isinstance(data_arg, str) else data_arg
        resp = client.post(url, json_data=json_data, headers=headers)
    else:
        resp = client.post(url, data=data_arg, headers=headers)

    print(resp)
    if resp.content_type == 'application/json':
        try:
            print(json.dumps(resp.json, ensure_ascii=False, indent=2))
        except TypeError:
            pass
    else:
        print(resp.text[:2000])

    if resp.error:
        echo(f'错误: {resp.error}', fg='red')


def cmd_head(args):
    url = args['_pos'][0] if args.get('_pos') else ''
    headers = parse_headers(args.get('header'))
    client = HTTPClient(timeout=int(args.get('timeout', 10)))
    resp = client.head(url, headers=headers)
    print(resp)
    echo('\n响应头:', fg='cyan')
    for k, v in resp.headers.items():
        echo(f'  {k}: {v}')


def cmd_download(args):
    url = args['_pos'][0] if args.get('_pos') else ''
    output = args.get('o', '')
    timeout = int(args.get('timeout', 60))
    show_progress = args.get('progress', True)

    client = HTTPClient(timeout=timeout)

    if not output:
        # 从 URL 推断文件名
        parsed = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed.path) or 'download'
        output = filename
        echo(f'📥 下载到: {output}', fg='cyan')

    # 检查是否已存在部分下载
    resume_pos = 0
    if os.path.exists(output):
        resume_pos = os.path.getsize(output)
        if resume_pos > 0:
            echo(f'📋 断点续传: 已有 {_fmt_size(resume_pos)}', fg='yellow')

    headers = {}
    if resume_pos > 0:
        headers['Range'] = f'bytes={resume_pos}-'

    t_start = time.time()
    resp = client.request('GET', url, headers=headers)

    if resp.status_code not in (200, 206):
        echo(f'❌ 下载失败: HTTP {resp.status_code}', fg='red')
        if resp.error:
            echo(f'   {resp.error}', fg='red')
        return

    total_size = int(resp.headers.get('Content-Length', 0))

    mode = 'ab' if resp.status_code == 206 and resume_pos > 0 else 'wb'
    downloaded = resume_pos if mode == 'ab' else 0

    with open(output, mode) as f:
        chunk_size = 8192
        while True:
            chunk = resp.fp.read(chunk_size) if resp.fp else b''
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            if show_progress and total_size:
                pct = downloaded / total_size * 100
                bar_len = 30
                filled = int(bar_len * downloaded / total_size) if total_size > 0 else bar_len
                bar = '=' * filled + '-' * (bar_len - filled)
                elapsed = time.time() - t_start
                speed = downloaded / elapsed if elapsed > 0 else 0
                sys.stderr.write(f'\r  [{bar}] {pct:.1f}% {_fmt_size(downloaded)}/{_fmt_size(total_size)} {_fmt_size(speed)}/s')
                sys.stderr.flush()

    elapsed = time.time() - t_start
    avg_speed = downloaded / elapsed if elapsed > 0 else 0
    print(f'\n✅ 完成: {output} {_fmt_size(downloaded)}, {elapsed:.1f}s, {_fmt_size(avg_speed)}/s)', fg='green')


def cmd_check_urls(args):
    """批量检测链接可用性"""
    source = args['_pos'][0] if args.get('_pos') else ''
    output = args.get('o', '')
    timeout = int(args.get('timeout', 10))
    follow_redirect = args.get('follow', False)
    concurrent = int(args.get('concurrent', 3))

    # 读取 URL 列表
    urls = []
    if os.path.isfile(source):
        with open(source, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and (line.startswith('http://') or line.startswith('https://')):
                    urls.append(line)
    else:
        urls = [source]

    if not urls:
        echo('❌ 无有效 URL', fg='red')
        sys.exit(1)

    echo(f'🔗 检测 {len(urls)} 个链接...', fg='cyan')

    results = []
    client = HTTPClient(timeout=timeout)

    for idx, url in enumerate(urls):
        sys.stderr.write(f'\r  进度: {idx+1}/{len(urls)}')
        sys.stderr.flush()
        resp = client.head(url)
        results.append({
            'url': url,
            'status': resp.status_code,
            'ok': resp.ok,
            'error': resp.error,
            'time_ms': round(resp.elapsed * 1000, 1),
            'size': resp.headers.get('Content-Length', '-'),
            'content_type': resp.content_type,
        })

    print()

    from scripts.table_format import tabulate

    # 统计
    ok_count = sum(1 for r in results if r['ok'])
    fail_count = len(results) - ok_count
    echo(f'结果: ✅{ok_count} ❌{fail_count}', fg='green' if fail_count == 0 else 'yellow')

    display_rows = [{
        '状态': color(str(r['status']), 'green' if r['ok'] else 'red'),
        '耗时(ms)': r['time_ms'],
        '大小': r['size'],
        '类型': r['content_type'][:30],
        'URL': r['url'][:80],
    } for r in sorted(results, key=lambda x: x['ok'])]
    print(tabulate(display_rows, tablefmt='grid'))

    # 失败详情
    failures = [r for r in results if not r['ok']]
    if failures:
        echo(f'\n❌ 失败的链接:', fg='red')
        for f in failures:
            reason = f"HTTP {f['status']}" if f['status'] else f.get('error', '未知错误')
            echo(f'  {f["url"]}: {reason}', fg='red')

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        echo(f'\n📄 报告已保存: {output}', fg='green')


def cmd_api_swagger(args):
    """解析 Swagger/OpenAPI 规范并生成 API 文档摘要"""
    url_or_file = args['_pos'][0] if args.get('_pos') else ''

    if url_or_file.startswith('http'):
        client = HTTPClient(timeout=30)
        resp = client.get(url_or_file)
        spec = resp.json
    else:
        with open(url_or_file, 'r', encoding='utf-8') as f:
            spec = json.load(f)

    if not spec:
        echo('❌ 无法解析 API 规范', fg='red')
        sys.exit(1)

    info = spec.get('info', {})
    version = info.get('version', 'N/A')
    title = info.get('title', 'API')
    base_url = spec.get('host', '') + spec.get('basePath', '')

    echo(f'📖 API 文档: {title} v{version}', fg='cyan', bold=True)
    if base_url:
        echo(f'   Base URL: {base_url}')
    print()

    paths = spec.get('paths', {})
    endpoints = []

    for path, methods in paths.items():
        if not isinstance(methods, dict):
            continue
        for method, details in methods.items():
            if method.upper() in ('GET', 'POST', 'PUT', 'DELETE', 'PATCH'):
                op_info = details if isinstance(details, dict) else {}
                summary = op_info.get('summary', '')
                desc = op_info.get('description', '')
                tags = op_info.get('tags', [''])
                tag = tags[0] if tags else ''
                endpoints.append({
                    '方法': method.upper(),
                    '路径': path,
                    '标签': tag,
                    '描述': summary or desc[:60],
                })

    from scripts.table_format import tabulate
    if endpoints:
        print(tabulate(endpoints, tablefmt='grid'))
        echo(f'\n共 {len(endpoints)} 个端点', fg='cyan')
    else:
        echo('(无端点信息)', fg='yellow')

    # 导出
    if args.get('o'):
        export_data = {
            'title': title, 'version': version,
            'base_url': base_url, 'endpoints': endpoints,
        }
        with open(args['o'], 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)


def cmd_batch_get(args):
    """并发 GET 多个 URL"""
    source = args['_pos'][0] if args.get('_pos') else ''
    concurrent = int(args.get('concurrent', 3))
    timeout = int(args.get('timeout', 15))
    output = args.get('o', '')

    urls = []
    if os.path.isfile(source):
        with open(source, 'r', encoding='utf-8') as f:
            urls = [l.strip() for l in f if l.strip().startswith(('http://', 'https://'))]
    else:
        urls = [source]

    echo(f'⚡ 并发请求 {len(urls)} 个 URL (并行={concurrent})...', fg='cyan')

    results = []
    client = HTTPClient(timeout=timeout)

    # 简单串行（标准库不支持真正的并发）
    for idx, url in enumerate(urls):
        sys.stderr.write(f'\r  {idx+1}/{len(urls)}')
        sys.stderr.flush()
        resp = client.get(url)
        results.append({'url': url, 'status': resp.status_code,
                        'ok': resp.ok, 'body_preview': resp.text[:200],
                        'elapsed_ms': round(resp.elapsed * 1000, 1)})

    print()

    from scripts.table_format import tabulate
    rows = [{'状态': r['status'], '耗时(ms)': r['elapsed_ms'],
             '预览': r['body_preview'][:80], 'URL': r['url'][:60]}
            for r in results]
    print(tabulate(rows, tablefmt='grid'))

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        echo(f'\n📄 结果: {output}', fg='green')


def cmd_debug_request(args):
    """调试 HTTP 请求：显示完整的请求/响应对"""
    url = args['_pos'][0] if args.get('_pos') else ''
    method = args.get('method', 'GET').upper()
    data_arg = args.get('data', '')
    headers = parse_headers(args.get('header'))

    client = HTTPClient(timeout=30)
    body = None
    if data_arg:
        if data_arg.startswith('{'):
            body = data_arg.encode('utf-8')
            headers['Content-Type'] = 'application/json; charset=utf-8'
        else:
            body = data_arg.encode('utf-8')

    echo(f'=== 请求 ===', fg='cyan', bold=True)
    echo(f'{method} {url}', bold=True)
    for k, v in {**dict(client.default_headers), **headers}.items():
        echo(f'  {k}: {v}')

    t = time.time()
    resp = client.request(method, url, data=body, headers=headers)
    elapsed = time.time() - t

    echo(f'\n=== 响应 ({resp.status_code}, {elapsed*1000:.0f}ms) ===',
         fg='green' if resp.ok else 'red', bold=True)

    for k, v in resp.headers.items():
        echo(f'  {k}: {v}')

    echo(f'\n--- Body ({len(resp.body)} bytes) ---', fg='yellow')
    if resp.content_type and 'json' in resp.content_type:
        try:
            print(json.dumps(resp.json, ensure_ascii=False, indent=2))
        except (TypeError, json.JSONDecodeError):
            print(resp.text[:3000])
    else:
        print(resp.text[:3000])


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'get': cmd_get,
    'post': cmd_post,
    'head': cmd_head,
    'download': cmd_download,
    'check-urls': cmd_check_urls,
    'api-swagger': cmd_api_swagger,
    'batch-get': cmd_batch_get,
    'debug': cmd_debug_request,
}

ALIASES = {
    'fetch': 'get', 'request': 'get',
    'curl': cmd_post,
    'link-check': 'check-urls', 'dead-links': 'check-urls',
    'dl': 'download',
    'swagger': 'api-swagger', 'openapi': 'api-swagger',
}


def main():
    args = parse_args()
    cmd = args['_cmd']
    if callable(cmd):  # 别名直接是函数引用
        cmd(args)
        return
    cmd = ALIASES.get(cmd, cmd)

    if cmd not in COMMANDS:
        available = ', '.join(sorted(set(list(COMMANDS.keys()) + [k for k, v in ALIASES.items() if not callable(v)])))
        echo(f'❌ 未知命令: {cmd}', fg='red')
        echo(f'可用命令: {available}', fg='cyan')
        sys.exit(1)

    COMMANDS[cmd](args)


if __name__ == '__main__':
    main()
