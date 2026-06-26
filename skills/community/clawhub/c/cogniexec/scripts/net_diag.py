#!/usr/bin/env python3
"""
net_diag.py — 网络诊断工具

功能：
  - ping:      Ping 检测（ICMP 回显请求，通过 TCP 模拟）
  - dns:       DNS 解析（查询 A/CNAME/MX/TXT/NS 记录）
  - port:      端口探测（TCP 连接测试）
  - traceroute: 路由追踪（TTL 递增跳数探测）
  - http-check: HTTP 服务健康检查
  - ip-info:   IP 归属查询
  - speed-test: 网速估算（下载速率）
  - resolve:   域名完整解析信息

纯标准库实现（socket/subprocess），无外部依赖。

用法:
  python net_diag.py ping example.com -c 4
  python net_diag.py dns example.com --type A,MX
  python net_diag.py port example.com 80,443,8080
  python net_diag.py traceroute example.com --max-hops 20
  python net_diag.py http-check https://api.example.com/health
  python net_diag.py ip-info 8.8.8.8
"""

import argparse
import sys
import socket
import struct
import time
import select
import json
import platform
import subprocess
from datetime import datetime, timezone


def _calc_checksum(data):
    """计算 ICMP 校验和"""
    if len(data) % 2:
        data += b'\x00'
    s = 0
    for i in range(0, len(data), 2):
        w = (data[i] << 8) + data[i + 1]
        s += w
    s = (s >> 16) + (s & 0xffff)
    s += (s >> 16)
    return ~s & 0xffff


def cmd_ping(args):
    """Ping 检测"""
    host = args.host
    count = args.count or 4
    timeout = args.timeout or 2

    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[!] DNS 解析失败: {host}")
        return

    print(f"\nPING {host} ({ip}) - {count} 次\n")

    stats = {'sent': 0, 'recv': 0, 'times': [], 'min': None, 'max': None}

    for i in range(1, count + 1):
        stats['sent'] += 1

        # Try raw socket first (may need admin)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            use_raw = True
        except (PermissionError, OSError):
            # Fallback: TCP-based ping
            use_raw = False
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        start = time.time()

        if use_raw:
            try:
                # Build ICMP echo request
                packet_id = os.getpid() & 0xFFFF if hasattr(os, 'getpid') else i
                header = struct.pack('!BBHHH', 8, 0, 0, packet_id, i)
                data = b'cogniexec-ping' * 4
                chksum = _calc_checksum(header + data)
                header = struct.pack('!BBHHH', 8, 0, chksum, packet_id, i)

                sock.sendto(header + data, (ip, 0))
                sock.settimeout(timeout)

                while True:
                    ready = select.select([sock], [], [], timeout)
                    if not ready[0]:
                        break
                    recv_data, addr = sock.recvfrom(1024)
                    recv_time = (time.time() - start) * 1000
                    if recv_data[20] == 0:  # Echo reply
                        stats['recv'] += 1
                        stats['times'].append(recv_time)
                        print(f"  来自 {addr[0]}: 时间={recv_time:.1f}ms  序号={i}")
                        break
            except socket.timeout:
                print(f"  请求超时")
            finally:
                sock.close()
        else:
            # TCP fallback: connect to common ports
            try:
                port = 80  # Try HTTP port
                sock.settimeout(timeout)
                result = sock.connect_ex((ip, port))
                elapsed = (time.time() - start) * 1000
                if result == 0:
                    stats['recv'] += 1
                    stats['times'].append(elapsed)
                    print(f"  TCP:{port} 开放 (延迟 ≈{elapsed:.1f}ms)")
                else:
                    print(f"  端口 {port} 关闭 ({elapsed:.1f}ms)")
            except socket.timeout:
                print(f"  连接超时")
            finally:
                sock.close()

        if i < count:
            time.sleep(0.5)

    # Summary
    lost = stats['sent'] - stats['recv']
    loss_pct = (lost / stats['sent'] * 100) if stats['sent'] > 0 else 0

    print(f"\n--- {host} ping 统计 ---")
    print(f"  发送: {stats['sent']}  接收: {stats['recv']}  丢失: {lost} ({loss_pct:.0f}%)")

    if stats['times']:
        print(f"  最小/最大/平均: {min(stats['times']):.1f}/{max(stats['times']):.1f}/{sum(stats['times'])/len(stats['times']):.1f} ms")


# Need os for getpid
import os


def cmd_dns(args):
    """DNS 解析"""
    domain = args.type or 'A'
    host = args.host

    query_types = [t.strip().upper() for t in domain.split(',')]

    print(f"\n=== DNS 解析: {host} ===\n")

    for qtype in query_types:
        print(f"[{qtype}] ", end='')

        try:
            if qtype == 'A':
                results = socket.getaddrinfo(host, None, socket.AF_INET)
                ips = sorted(set(info[4][0] for info in results))
                print(', '.join(ips[:8]))

            elif qtype == 'AAAA':
                results = socket.getaddrinfo(host, None, socket.AF_INET6)
                ips = sorted(set(info[4][0] for info in results))
                print(', '.join(ips[:5]) if ips else '(无 AAAA 记录)')

            elif qtype == 'CNAME':
                try:
                    _, _, aliaslist, _ = socket.gethostbyaddr(host)
                    print(aliaslist[0] if aliaslist else '(无 CNAME)')
                except socket.herror:
                    print('(无 CNAME)')

            elif qtype == 'MX':
                # Use nslookup/dig as fallback
                rc, out, _ = _run_cmd(['nslookup', '-type=MX', host])
                if out and 'mail exchanger' in out.lower():
                    for line in out.split('\n'):
                        if 'exchanger' in line.lower() or 'mail' in line.lower():
                            print(line.strip())
                    continue
                print('(无法获取 MX，需安装 dns.resolver 或使用 dig/nslookup)')

            elif qtype == 'TXT':
                rc, out, _ = _run_cmd(['nslookup', '-type=TXT', host])
                if out:
                    for line in out.split('\n'):
                        if 'text' in line.lower() or '=' in line:
                            print(f"  {line.strip()}")
                            continue
                    print('(无 TXT 或格式不支持)')
                else:
                    print('(无 TXT 记录)')

            elif qtype == 'NS':
                _, _, _, addrs = socket.gethostbyaddr(host)
                print(', '.join(addrs[:6]))

            elif qtype == 'ALL' or qtype == 'ANY':
                # Full info dump
                try:
                    fqdn, aliases, ips = socket.gethostbyaddr(
                        socket.gethostbyname(host)
                    )
                    print(f"FQDN: {fqdn}")
                    print(f"Aliases: {aliases}")
                    print(f"A: {ips}")
                except Exception as e:
                    print(f"错误: {e}")

            else:
                print(f"(不支持的类型: {qtype})")

        except socket.gaierror as e:
            print(f"(解析失败: {e})")


def _run_cmd(cmd_list):
    """执行系统命令"""
    try:
        r = subprocess.run(cmd_list, capture_output=True, text=True, timeout=10)
        return r.returncode, r.stdout, r.stderr
    except FileNotFoundError:
        return -1, '', ''
    except subprocess.TimeoutExpired:
        return -1, '', 'timeout'


def cmd_port(args):
    """端口探测"""
    host = args.host
    ports_str = args.ports
    timeout = args.timeout or 2

    # Parse ports
    ports = []
    for p in ports_str.split(','):
        p = p.strip()
        if '-' in p:
            start, end = p.split('-', 1)
            ports.extend(range(int(start), int(end) + 1))
        elif p:
            ports.append(int(p))

    if not ports:
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995,
                 3306, 3389, 5432, 6379, 8080, 8443, 8888, 27017]

    print(f"\n=== 端口扫描: {host} ({len(ports)} 个端口) ===\n")

    open_ports = []
    filtered = []

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        start = time.time()

        result = sock.connect_ex((host, port))
        elapsed = (time.time() - start) * 1000

        if result == 0:
            open_ports.append((port, elapsed))
            status = f"🟢 开放  {elapsed:.0f}ms"
        elif result == 111 or result == 10035:
            filtered.append(port)
            status = "🔴 过滤"
        else:
            status = "⚫ 关闭"

        service = _guess_service(port)
        print(f"  {port:>6d}/{service:<12s}  {status}")

        sock.close()

    print(f"\n结果: {len(open_ports)} 个开放, "
          f"{len(filtered)} 个过滤, "
          f"{len(ports) - len(open_ports) - len(filtered)} 个关闭")

    if open_ports:
        print(f"\n开放端口:")
        for p, t in open_ports:
            svc = _guess_service(p)
            print(f"  :{p}  {svc}  ({t:.0f}ms)")


def _guess_service(port):
    services = {
        21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
        53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
        443: 'HTTPS', 465: 'SMTPS', 587: 'SMTP',
        993: 'IMAPS', 995: 'POP3S',
        3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
        6379: 'Redis', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt',
        27017: 'MongoDB',
    }
    return services.get(port, '')


def cmd_traceroute(args):
    """路由追踪"""
    host = args.host
    max_hops = args.max_hops or 20
    timeout = args.timeout or 2

    try:
        dest_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[!] DNS 解析失败: {host}")
        return

    print(f"\ntraceroute 到 {host} ({dest_ip}), 最大 {max_hops} 跳:\n")

    system = platform.system().lower()

    if system == 'windows':
        # Use Windows tracert
        rc, out, err = _run_cmd(['tracert', '-d', '-h', str(max_hops), '-w', str(int(timeout*1000)), host])
        if out:
            print(out)
        else:
            print(f"tracert 失败: {err}")
        return

    elif system in ('linux', 'darwin'):
        # Use system traceroute
        rc, out, err = _run_cmd(['traceroute', '-n', '-m', str(max_hops), '-w', str(timeout), host])
        if out:
            print(out)
        else:
            # Fallback: manual TTL probing
            _manual_traceroute(dest_ip, max_hops, timeout)
        return

    # Pure Python fallback
    _manual_traceroute(dest_ip, max_hops, timeout)


def _manual_traceroute(dest_ip, max_hops, timeout):
    """纯 Python 路由追踪（TTL 探测）"""
    for ttl in range(1, max_hops + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(timeout)

        # Send with TTL via raw socket trick (or use UDP approach)
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        try:
            recv_sock.sendto(b'\x00' * 8, (dest_ip, 33434))
            start = time.time()
            try:
                _, addr = sock.recvfrom(512)
                elapsed = (time.time() - start) * 1000
                hop_ip = addr[0]
                print(f"  {ttl:2d}.  {hop_ip:<18s}  {elapsed:.1f}ms")
                if hop_ip == dest_ip:
                    print(f"\n  已到达目标!")
                    break
            except socket.timeout:
                print(f"  {ttl:2d}.  *                          超时")
        except Exception:
            print(f"  {ttl:2d}.  *                          请求失败")
        finally:
            sock.close()
            recv_sock.close()


def cmd_http_check(args):
    """HTTP 服务健康检查"""
    url = args.url
    method = getattr(args, 'method', 'GET')
    expected_status = args.expected or 200
    timeout = args.timeout or 10

    # Parse URL
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError

    print(f"\n=== HTTP 健康检查: {url} ===\n")
    print(f"  方法: {method}  期望状态: {expected_status}\n")

    start = time.time()
    try:
        req = Request(url, method=method)

        # Add common headers
        req.add_header('User-Agent', 'cogniexec-net-diag/1.0')
        if args.headers:
            for h in args.headers:
                if ':' in h:
                    k, v = h.split(':', 1)
                    req.add_header(k.strip(), v.strip())

        response = urlopen(req, timeout=timeout)
        elapsed = (time.time() - start) * 1000
        status = response.status
        headers = dict(response.headers)

        print(f"  状态码:     {status}")
        print(f"  响应时间:   {elapsed:.0f}ms")
        print(f"  内容长度:   {headers.get('Content-Length', '?')}")
        print(f"  Content-Type: {headers.get('Content-Type', '?')}")
        print(f"  Server:     {headers.get('Server', '?')}")

        if status == expected_status:
            print(f"\n  ✅ 健康 (状态匹配)")
        else:
            print(f"\n  ⚠️  异常 (期望 {expected_status}, 实际 {status})")

    except HTTPError as e:
        elapsed = (time.time() - start) * 1000
        print(f"  状态码:     {e.code}")
        print(f"  响应时间:   {elapsed:.0f}ms")
        print(f"\n  ❌ HTTP 错误: {e.code} {e.reason}")

    except URLError as e:
        elapsed = (time.time() - start) * 1000
        print(f"  响应时间:   {elapsed:.0f}ms")
        print(f"\n  ❌ 连接失败: {e.reason}")

    except Exception as e:
        print(f"\n  ❌ 错误: {e}")


def cmd_ip_info(args):
    """IP 归属查询"""
    ip_or_host = args.ip

    try:
        ip = socket.gethostbyname(ip_or_host)
    except socket.gaierror:
        ip = ip_or_host

    print(f"\n=== IP 信息: {ip} ===\n")

    # Local info
    hostname = ''
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        pass

    print(f"  IP 地址:   {ip}")
    print(f"  主机名:    {hostname or '(未知)'}")

    # Check private/range
    import ipaddress
    try:
        addr = ipaddress.ip_address(ip)
        if addr.is_private:
            print(f"  类型:      🏠 内网/私有地址")
            if addr.is_loopback:
                print(f"  特殊:      回环地址 (localhost)")
        elif addr.is_reserved:
            print(f"  类型:      🔒 保留地址")
        else:
            print(f"  类型:      🌐 公网地址")

        # IPv4 range info
        if isinstance(addr, ipaddress.IPv4Address):
            first = int(addr)
            ranges = [
                ('APNIC (亚太)', 167772160, 184549375),
                ('ARIN (北美)', 1392508928, 1499463679),
                ('RIPE (欧洲)', 1996488704, 2147483647),
                ('LACNIC (拉美)', 2147483648, 2281701375),
                ('AFRINIC (非洲)', 2281701376, 2415919103),
            ]
            for name, start, end in ranges:
                if start <= first <= end:
                    print(f"  分配区域:  {name}")
                    break
    except ValueError:
        pass

    # Try online lookup (optional, non-blocking)
    print(f"\n  在线查询 (可选):")
    print(f"    https://ip-api.com/json/{ip}")
    print(f"    https://ipinfo.io/{ip}/json")


def cmd_speed_test(args):
    """简单网速估算"""
    servers = args.servers or ['https://www.google.com/generate_204',
                                'https://cloudflare.com/',
                                'https://github.com']

    print(f"\n=== 网速测试 (下载估算) ===\n")

    from urllib.request import urlopen
    results = []

    for url in servers:
        print(f"  测试: {url[:50]}...", end='', flush=True)

        try:
            start = time.time()
            req = Request(url, headers={'User-Agent': 'cogniexec/1.0'})
            resp = urlopen(req, timeout=10)
            data = resp.read(1024 * 64)  # Read 64KB sample
            elapsed = time.time() - start

            size_kb = len(data) / 1024
            speed_kbps = size_kb / elapsed if elapsed > 0 else 0
            speed_mbps = speed_kbps / 125

            results.append(speed_mbps)
            print(f" {speed_mbps:.1f} Mbps ({elapsed:.2f}s)")

        except Exception as e:
            print(f" 失败 ({type(e).__name__})")

    if results:
        avg = sum(results) / len(results)
        best = max(results)
        print(f"\n  平均: {avg:.1f} Mbps | 最佳: {best:.1f} Mbps")


def cmd_resolve(args):
    """域名完整解析信息"""
    host = args.host

    print(f"\n{'='*55}")
    print(f" 完整解析: {host}")
    print(f"{'='*55}\n")

    try:
        # Basic resolution
        fqdn = None
        aliases = []
        all_ips = []

        try:
            fqdn, aliases, ips = socket.gethostbyaddr(socket.gethostbyname(host))
            all_ips = ips
        except socket.herror:
            # Just get IPs
            results = socket.getaddrinfo(host, None, socket.AF_INET)
            all_ips = sorted(set(r[4][0] for r in results))

        if fqdn:
            print(f"  FQDN:         {fqdn}")
        if aliases:
            print(f"  CNAME/Alias:  {', '.join(aliases)}")
        print(f"  A 记录:       {', '.join(all_ips)}")

        # AAAA
        try:
            results_v6 = socket.getaddrinfo(host, None, socket.AF_INET6)
            v6_ips = sorted(set(r[4][0] for r in results_v6))
            if v6_ips:
                print(f"  AAAA 记录:    {', '.join(v6_ips)}")
        except Exception:
            pass

        # Reverse DNS
        print(f"\n  反向解析:")
        seen_reverse = set()
        for ip in all_ips[:5]:
            try:
                rev_name = socket.gethostbyaddr(ip)[0]
                if rev_name not in seen_reverse:
                    seen_reverse.add(rev_name)
                    print(f"    {ip} → {rev_name}")
            except socket.herror:
                print(f"    {ip} → (无 PTR)")

        # System resolver check
        print(f"\n  系统 DNS 解析器:")
        resolv_conf = '/etc/resolv.conf' if os.path.exists('/etc/resolv.conf') else None
        if system := platform.system().lower():
            if system == 'windows':
                rc, out, _ = _run_cmd(['ipconfig', '/all'])
                for line in out.split('\n'):
                    if 'dns' in line.lower() and '.' in line:
                        print(f"    {line.strip()}")

    except socket.gaierror as e:
        print(f"[!] 解析完全失败: {e}")


# ─── 命令注册 ──────────────────────────────────────────────
COMMANDS = {
    'ping':        cmd_ping,
    'dns':         cmd_dns,
    'port':        cmd_port,
    'traceroute':  cmd_traceroute,
    'http-check':  cmd_http_check,
    'ip-info':     cmd_ip_info,
    'speed-test':  cmd_speed_test,
    'resolve':     cmd_resolve,
}

ALIASES = {
    'p':           'ping',
    'nslookup':    'dns',
    'lookup':      'dns',
    'scan':        'port',
    'trace':       'traceroute',
    'tr':          'traceroute',
    'health':      'http-check',
    'check':       'http-check',
    'ip':          'ip-info',
    'whois':       'ip-info',
    'speed':       'speed-test',
    'res':         'resolve',
    'full':        'resolve',
}


def main():
    parser = argparse.ArgumentParser(
        prog='net_diag',
        description='网络诊断工具集',
        epilog='示例:\n'
              '  %(prog)s ping example.com -c 4\n'
              '  %(prog)s dns example.com --type A,MX,TXT\n'
              '  %(prog)s port example.com 80,443,8080\n'
              '  %(prog)s traceroute example.com\n'
              '  %(prog)s http-check https://example.com\n'
              '  %(prog)s ip-info 114.114.114.114\n'
              '  %(prog)s speed-test\n'
              '  %(prog)s resolve github.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('command', nargs='?', help='子命令: ' + ', '.join(COMMANDS))
    parser.add_argument('rest', nargs=argparse.REMAINDER, help='命令参数')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print("\n可用子命令:", ', '.join(COMMANDS))
        print(f"共 {len(COMMANDS)} 个命令 | 别名数: {len(ALIASES)}")
        sys.exit(0)

    cmd_name = ALIASES.get(args.command, args.command)

    if cmd_name not in COMMANDS:
        print(f"[!] 未知命令: {args.command}")
        print(f"    可用: {', '.join(COMMANDS)}")
        sys.exit(1)

    sub_parser = argparse.ArgumentParser(prog=f'{parser.prog} {cmd_name}', add_help=False)

    if cmd_name == 'ping':
        sub_parser.add_argument('host', help='目标主机')
        sub_parser.add_argument('-c', '--count', type=int, default=4, help='次数 (默认: 4)')
        sub_parser.add_argument('-t', '--timeout', type=float, default=2, help='超时秒数 (默认: 2)')

    elif cmd_name == 'dns':
        sub_parser.add_argument('host', help='目标域名')
        sub_parser.add_argument('--type', default='A', help='查询类型: A,AAAA,CNAME,MX,TXT,NS,ALL (默认: A)')

    elif cmd_name == 'port':
        sub_parser.add_argument('host', help='目标主机')
        sub_parser.add_argument('ports', nargs='?', default='',
                                help='端口列表 (逗号分隔或范围如 1-1024, 默认常用端口)')
        sub_parser.add_argument('-t', '--timeout', type=float, default=2, help='超时秒数')

    elif cmd_name == 'traceroute':
        sub_parser.add_argument('host', help='目标主机')
        sub_parser.add_argument('-m', '--max-hops', type=int, default=20, help='最大跳数 (默认: 20)')
        sub_parser.add_argument('-t', '--timeout', type=float, default=2, help='每跳超时秒数')

    elif cmd_name == 'http-check':
        sub_parser.add_argument('url', help='目标 URL')
        sub_parser.add_argument('-X', '--method', default='GET', help='HTTP 方法 (默认: GET)')
        sub_parser.add_argument('-e', '--expected', type=int, default=200, help='期望状态码 (默认: 200)')
        sub_parser.add_argument('-t', '--timeout', type=float, default=10, help='超时秒数')
        sub_parser.add_argument('-H', '--header', action='append', dest='headers', default=[],
                                help='额外请求头 (可多次)')

    elif cmd_name == 'ip-info':
        sub_parser.add_argument('ip', help='IP 地址或域名')

    elif cmd_name == 'speed-test':
        sub_parser.add_argument('--servers', nargs='*', default=[], help='自定义测试服务器 URL 列表')

    elif cmd_name == 'resolve':
        sub_parser.add_argument('host', help='目标域名/IP')

    sub_args = sub_parser.parse_args(args.rest)

    try:
        COMMANDS[cmd_name](sub_args)
    except KeyboardInterrupt:
        print("\n[!] 操作已取消")
        sys.exit(130)
    except Exception as e:
        print(f"[!] 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
