"""Bounded HTTP transport: explicit destinations, no proxies or redirects.

DNS is resolved once, every answer is checked, and sockets connect to those IPs
directly. HTTPS still uses the original hostname for SNI and certificate checks.
"""
import http.client
import ipaddress
import json
import math
import queue
import socket
import ssl
import threading
import time
from urllib.parse import urlsplit


MAX_RESPONSE = 4 * 1024 * 1024
_PRIVATE = tuple(ipaddress.ip_network(x) for x in ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', 'fc00::/7'))
_NAT64 = ipaddress.ip_network('64:ff9b::/96')
_METADATA = {ipaddress.ip_address(x) for x in ('169.254.169.254', '100.100.100.200', '168.63.129.16', 'fd00:ec2::254')}
_METADATA_HOSTS = {'metadata.google.internal', 'metadata.google', 'instance-data.ec2.internal', 'instance-data'}


def _check_ip(value, allow_remote):
    ip = ipaddress.ip_address(value)
    effective = ip.ipv4_mapped if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped else ip
    candidates = [effective]
    if isinstance(ip, ipaddress.IPv6Address):
        if ip in _NAT64: candidates.append(ipaddress.IPv4Address(int(ip) & 0xffffffff))
        if ip.sixtofour: candidates.append(ip.sixtofour)
        if ip.teredo: candidates.extend(ip.teredo)
    if any(candidate in _METADATA or candidate.is_link_local or candidate.is_unspecified or candidate.is_multicast
           for candidate in candidates):
        raise ValueError('拒绝元数据、链路本地、未指定或多播地址')
    private = any(effective.version == net.version and effective in net for net in _PRIVATE)
    if effective.is_loopback or private:
        return ip
    if not effective.is_global:
        raise ValueError('拒绝保留或不可路由地址')
    if not allow_remote:
        raise ValueError('公网地址需要显式 --allow-remote')
    return ip


def validate_url(url, allow_remote=False):
    """No-network URL policy check; returns normalized URL components."""
    if not isinstance(url, str) or not url or any(ord(c) <= 32 or ord(c) == 127 for c in url) or '\\' in url:
        raise ValueError('URL 不能为空或含空白、控制字符、反斜杠')
    try:
        parts = urlsplit(url)
        host, port = parts.hostname, parts.port
    except ValueError as exc:
        raise ValueError('无法解析 HTTP(S) 端点') from exc
    if parts.scheme not in {'http', 'https'} or not host:
        raise ValueError('端点仅支持带主机名的 http:// 或 https:// URL')
    if parts.username is not None or parts.password is not None:
        raise ValueError('URL 不允许携带用户名或密码')
    if parts.fragment or '%' in host:
        raise ValueError('端点不支持 URL 片段、转义主机或 IPv6 scope ID')
    if port is not None and not 1 <= port <= 65535:
        raise ValueError('端口必须为 1–65535')
    try:
        host = host.encode('idna').decode('ascii').lower()
    except UnicodeError as exc:
        raise ValueError('主机名无法解析为 IDNA') from exc
    if host.rstrip('.') in _METADATA_HOSTS:
        raise ValueError('拒绝云元数据主机')
    try:
        literal = ipaddress.ip_address(host)
    except ValueError:
        literal = None
    if literal is not None:
        _check_ip(literal, allow_remote)
    elif host != 'localhost' and not allow_remote:
        raise ValueError('默认仅允许精确 localhost、回环和私有 IP；其他域名需要显式 --allow-remote')
    return parts.scheme, host, port or (443 if parts.scheme == 'https' else 80), parts.path or '/', parts.query


def _remaining(deadline):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError('HTTP 请求超过 timeout')
    return remaining


def _addresses(host, port, allow_remote, deadline):
    if host == 'localhost':
        values = ['127.0.0.1']  # Do not trust a hosts-file/DNS override for localhost.
    else:
        try:
            values = [str(ipaddress.ip_address(host))]
        except ValueError:
            # A daemon resolver bounds waiting without an executor that blocks shutdown.
            replies = queue.Queue(maxsize=1)
            def resolve():
                try:
                    replies.put((socket.getaddrinfo(host, port, type=socket.SOCK_STREAM), None))
                except Exception as exc:
                    replies.put((None, exc))
            threading.Thread(target=resolve, daemon=True).start()
            try:
                infos, error = replies.get(timeout=_remaining(deadline))
            except queue.Empty as exc:
                raise TimeoutError('DNS 解析超过 timeout') from exc
            if error:
                raise error
            values = [info[4][0] for info in infos if info[0] in {socket.AF_INET, socket.AF_INET6}]
    if not values:
        raise ValueError('主机没有可用的 IPv4/IPv6 地址')
    checked = []
    for value in dict.fromkeys(values):
        ip = _check_ip(value, allow_remote)  # Reject mixed safe/unsafe DNS answers as a whole.
        checked.append((socket.AF_INET6, (str(ip), port, 0, 0)) if ip.version == 6 else (socket.AF_INET, (str(ip), port)))
    _remaining(deadline)
    return checked


def _connect(addresses, deadline):
    last_error = None
    for family, sockaddr in addresses:
        sock = socket.socket(family, socket.SOCK_STREAM)
        try:
            sock.settimeout(_remaining(deadline))
            sock.connect(sockaddr)  # Numeric address tuple: no second hostname lookup.
            _remaining(deadline)
            return sock
        except OSError as exc:
            sock.close(); last_error = exc
    raise last_error or OSError('没有可连接的已校验地址')


class _PinnedHTTP(http.client.HTTPConnection):
    def connect(self):
        self.sock = _connect(self.addresses, self.deadline)
        self._active_socket = self.sock


class _PinnedHTTPS(http.client.HTTPSConnection):
    def connect(self):
        self.sock = _connect(self.addresses, self.deadline)
        self._active_socket = self.sock
        # wrap_socket detaches the raw socket. Publish the SSL socket before its
        # blocking handshake so the overall deadline can interrupt the real fd.
        self.sock = self._context.wrap_socket(self.sock, server_hostname=self.host,
                                              do_handshake_on_connect=False)
        self._active_socket = self.sock
        self.sock.settimeout(_remaining(self.deadline))
        self.sock.do_handshake()
        _remaining(self.deadline)


def _request(url, payload, timeout, allow_remote):
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('timeout 必须是正的有限秒数')
    scheme, host, port, path, query = validate_url(url, allow_remote)
    deadline = time.monotonic() + timeout
    addresses = _addresses(host, port, allow_remote, deadline)
    if scheme == 'https':
        conn = _PinnedHTTPS(host, port, timeout=_remaining(deadline), context=ssl.create_default_context())
    else:
        conn = _PinnedHTTP(host, port, timeout=_remaining(deadline))
    conn.addresses, conn.deadline = addresses, deadline
    timed_out = threading.Event()
    def abort():
        timed_out.set()
        # HTTPConnection transfers/clears .sock for HTTP/1.0 or Connection: close.
        # The response file still owns that socket while a body is being read.
        sock = getattr(conn, '_active_socket', None) or conn.sock
        if sock is not None:
            try: sock.shutdown(socket.SHUT_RDWR)
            except OSError: pass
            try: sock.close()
            except OSError: pass
    timer = threading.Timer(_remaining(deadline), abort)
    timer.daemon = True
    timer.start()
    response = None
    try:
        data = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode('utf-8') if payload is not None else None
        target = path + ('?' + query if query else '')
        conn.request('POST' if data is not None else 'GET', target, body=data,
                     headers={'Content-Type': 'application/json', 'Accept-Encoding': 'identity'})
        response = conn.getresponse()
        if 300 <= response.status < 400:
            raise ValueError('拒绝 HTTP 重定向；请明确配置最终端点后重试')
        length = response.getheader('Content-Length')
        if length is not None:
            try: declared = int(length)
            except ValueError as exc: raise ValueError('响应 Content-Length 无效') from exc
            if declared < 0 or declared > MAX_RESPONSE:
                raise ValueError('HTTP 响应超过 4 MB 限制或长度无效')
        data = response.read(MAX_RESPONSE + 1)
        if len(data) > MAX_RESPONSE:
            raise ValueError('HTTP 响应超过 4 MB 限制')
        if timed_out.is_set():
            raise TimeoutError('HTTP 请求超过 timeout')
        _remaining(deadline)
        return response.status, data
    except Exception as exc:
        if timed_out.is_set():
            raise TimeoutError('HTTP 请求超过 timeout') from exc
        raise
    finally:
        timer.cancel()
        if response is not None:
            response.close()
        conn.close()
        active = getattr(conn, '_active_socket', None)
        if active is not None:
            active.close()


def safe_json(url, payload=None, timeout=30, allow_remote=False):
    """GET/POST JSON, raising on policy/transport/HTTP/JSON errors."""
    status, body = _request(url, payload, timeout, allow_remote)
    if not 200 <= status < 300:
        raise ValueError(f'HTTP 请求失败，状态码 {status}')
    def invalid_constant(value):
        raise ValueError('响应 JSON 含非有限数值')
    try:
        return json.loads(body, parse_constant=invalid_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError('HTTP 响应不是有效 JSON') from exc


def safe_health(url, timeout=3, allow_remote=False):
    """True for 2xx, False for other non-redirect statuses; policy/I/O errors raise."""
    status, _ = _request(url, None, timeout, allow_remote)
    return 200 <= status < 300


def response_error(value, allow_refusal=False, require_result=False, allow_sql=False):
    """Validate service completion; callers opt in to result/plan evidence checks.

    Absent status retains the legacy protocol. Explicit status must be one of the
    documented successes (or an allowed refusal). NULL needs completion evidence;
    an explicit empty rows list is a result, not a missing response.
    """
    if not isinstance(value, dict):
        return '接口响应必须是 JSON 对象'
    if value.get('error') not in (None, False, ''):
        return '接口错误：' + str(value['error'])
    if value.get('success') is False:
        return '接口明确返回 success=false'
    status = str(value.get('status', '')).lower()
    success = status in {'ok', 'success', 'completed', 'done'}
    refusal = bool(value.get('rejected') or value.get('refused') or status in {'rejected', 'refused'})
    if 'status' in value and not success and not (allow_refusal and status in {'rejected', 'refused'}):
        return '接口没有明确成功完成（未知/未完成状态）：' + status
    if not allow_refusal and refusal:
        return '接口拒答或追问，不能作为数值核对成功'
    if require_result and not (allow_refusal and refusal):
        sql = isinstance(value.get('sql'), str) and bool(value['sql'].strip())
        if value.get('rows') is not None and not isinstance(value['rows'], list):
            return 'rows 必须是完整数组，不能用其他 JSON 类型冒充结果'
        rows = isinstance(value.get('rows'), list)
        scalar = 'value' in value and (value['value'] is not None or success or sql)
        if not (rows or scalar or (allow_sql and sql)):
            return '没有已完成的结果或查询计划证据；缺少返回值不等于 NULL'
    return None
