#!/usr/bin/env python3
"""gen_cert.py — 为 agent-easy-http 等 HTTP 类 skill 生成自签 TLS 证书

特性：
- 支持 SAN（Subject Alternative Names）配置，可同时签多个 IP/域名
- 证书存放统一目录 ~/.http/certs/（多个 HTTP skill 共用）
- 默认有效期 825 天（macOS 信任链上限）
- 生成后打印客户端信任配置方法

用法：
    python3 gen_cert.py                                  # 交互式
    python3 gen_cert.py --san 192.168.1.10,myserver.local   # 直接指定 SAN
    python3 gen_cert.py --san auto                       # 自动嗅探本机 IP
    python3 gen_cert.py --force                          # 覆盖已有证书
"""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
from pathlib import Path

# 复用 tls_auth 的路径探测，保证三 skill 一致
sys.path.insert(0, str(Path(__file__).parent))
from tls_auth import CERT_DIR  # noqa: E402

CERT_PATH = CERT_DIR / "server.crt"
KEY_PATH = CERT_DIR / "server.key"
CSR_CONF = CERT_DIR / "openssl.cnf"

DEFAULT_DAYS = 825  # macOS Catalina+ 信任链上限
DEFAULT_CN = "openclaw-http-services"


def detect_local_ips() -> list[str]:
    """嗅探本机所有非 lo 的 IPv4。"""
    ips: list[str] = []
    try:
        # 通用方法：连接外网（不会真发包，只是让内核选源 IP）
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            primary = s.getsockname()[0]
            if primary and primary != "127.0.0.1":
                ips.append(primary)
    except Exception:
        pass

    try:
        # hostname -I 兜底，能拿到多个内网 IP
        result = subprocess.run(
            ["hostname", "-I"], capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            for ip in result.stdout.strip().split():
                if ip and ip != "127.0.0.1" and ip not in ips:
                    ips.append(ip)
    except Exception:
        pass

    return ips


def write_openssl_conf(cn: str, san_entries: list[str]) -> None:
    """生成 openssl 配置文件（含 SAN 扩展）。"""
    san_lines = []
    ip_idx = 1
    dns_idx = 1
    for entry in san_entries:
        # 简单判断 IP vs 域名
        parts = entry.split(".")
        if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            san_lines.append(f"IP.{ip_idx} = {entry}")
            ip_idx += 1
        else:
            san_lines.append(f"DNS.{dns_idx} = {entry}")
            dns_idx += 1

    # 总是把 localhost 和 127.0.0.1 加进去
    if "127.0.0.1" not in san_entries:
        san_lines.append(f"IP.{ip_idx} = 127.0.0.1")
    if "localhost" not in san_entries:
        san_lines.append(f"DNS.{dns_idx} = localhost")

    conf = f"""[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = CN
ST = Shanghai
L = Shanghai
O = OpenClaw
OU = HTTP Services
CN = {cn}

[v3_req]
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
{chr(10).join(san_lines)}
"""
    CSR_CONF.write_text(conf)


def generate_cert(cn: str, san_entries: list[str], days: int = DEFAULT_DAYS) -> None:
    """调用 openssl 生成自签证书。openssl 缺失或失败时给友好提示。"""
    write_openssl_conf(cn, san_entries)

    # 1. 生成私钥
    try:
        subprocess.run(
            ["openssl", "genrsa", "-out", str(KEY_PATH), "2048"],
            check=True, capture_output=True,
        )
    except FileNotFoundError:
        raise RuntimeError(
            "openssl 未安装。请先安装：apt-get install openssl 或 brew install openssl"
        )
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode(errors="replace") if e.stderr else ""
        raise RuntimeError(
            f"openssl genrsa 失败 (exit {e.returncode}): {stderr[:500]}"
        )
    os.chmod(KEY_PATH, 0o600)

    # 2. 生成自签证书（一步到位）
    try:
        subprocess.run(
            [
                "openssl", "req", "-x509", "-new", "-nodes",
                "-key", str(KEY_PATH),
                "-sha256",
                "-days", str(days),
                "-out", str(CERT_PATH),
                "-config", str(CSR_CONF),
                "-extensions", "v3_req",
            ],
            check=True, capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode(errors="replace") if e.stderr else ""
        raise RuntimeError(
            f"openssl req 签发证书失败 (exit {e.returncode}): {stderr[:500]}\n"
            f"  排查：openssl.conf 内容可能有问题，路径：{CSR_CONF}"
        )
    os.chmod(CERT_PATH, 0o644)


def verify_cert() -> dict:
    """读取已生成证书的关键信息。"""
    if not CERT_PATH.exists():
        return {}
    try:
        out = subprocess.check_output(
            ["openssl", "x509", "-in", str(CERT_PATH), "-noout", "-text"],
            text=True,
        )
        info = {"path": str(CERT_PATH)}
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("Not After"):
                info["expires"] = line.split(":", 1)[1].strip()
            elif line.startswith("Subject:"):
                info["subject"] = line.split(":", 1)[1].strip()
            elif "DNS:" in line or "IP Address:" in line:
                info["san"] = line.strip()
        return info
    except Exception as e:
        return {"error": str(e)}


def print_trust_instructions() -> None:
    """打印各端如何信任自签证书的指引。"""
    print()
    print("=" * 60)
    print("  📋 客户端如何信任此自签证书")
    print("=" * 60)
    print()
    print(f"证书路径：{CERT_PATH}")
    print()
    print("【curl】")
    print(f"  curl --cacert {CERT_PATH} https://your-host:port/health")
    print("  # 或临时跳过验证：curl -k https://...")
    print()
    print("【Python requests】")
    print("  requests.get('https://...', verify='" + str(CERT_PATH) + "')")
    print()
    print("【浏览器】")
    print("  macOS: 双击证书 → 钥匙串访问 → 改信任为「始终信任」")
    print("  Windows: 双击证书 → 安装到「受信任的根证书颁发机构」")
    print("  Linux: cp 到 /usr/local/share/ca-certificates/ && update-ca-certificates")
    print()
    print("【验证证书有效性】")
    print(f"  openssl s_client -connect your-host:port -CAfile {CERT_PATH}")
    print()


def main():
    parser = argparse.ArgumentParser(description="为 agent-easy-http 生成自签 TLS 证书")
    parser.add_argument("--san", default=None,
                        help="逗号分隔的 SAN 列表（IP/域名），或 'auto' 自动嗅探")
    parser.add_argument("--cn", default=DEFAULT_CN, help="证书 Common Name")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="有效期（天）")
    parser.add_argument("--force", action="store_true", help="覆盖已有证书")
    args = parser.parse_args()

    # 检查 openssl 可用
    try:
        subprocess.run(["openssl", "version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ 未找到 openssl 命令，请先安装：apt-get install openssl / brew install openssl")
        sys.exit(1)

    CERT_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(CERT_DIR.parent, 0o700)

    # 检查是否已有证书
    if CERT_PATH.exists() and not args.force:
        info = verify_cert()
        print(f"⚠️  证书已存在：{CERT_PATH}")
        if info.get("expires"):
            print(f"   到期时间：{info['expires']}")
        if info.get("san"):
            print(f"   SAN：{info['san']}")
        print()
        print("如需重新生成，加 --force")
        return

    # 收集 SAN
    san_entries: list[str] = []
    if args.san == "auto":
        san_entries = detect_local_ips()
        print(f"🔍 自动嗅探到的本机 IP：{san_entries or '(无)'}")
    elif args.san:
        san_entries = [s.strip() for s in args.san.split(",") if s.strip()]
    else:
        # 交互式
        detected = detect_local_ips()
        print(f"🔍 检测到本机 IP：{detected or '(无)'}")
        prompt = "请输入证书要绑定的 IP/域名（逗号分隔，回车=用检测到的）: "
        user_input = input(prompt).strip()
        if user_input:
            san_entries = [s.strip() for s in user_input.split(",") if s.strip()]
        else:
            san_entries = detected

    if not san_entries:
        print("⚠️  未配置任何 SAN，仅 127.0.0.1 和 localhost 可访问")

    # 生成
    print()
    print(f"📝 生成证书 CN={args.cn} SAN={san_entries + ['127.0.0.1', 'localhost']}")
    try:
        generate_cert(args.cn, san_entries, args.days)
    except subprocess.CalledProcessError as e:
        print(f"❌ openssl 失败：{e.stderr.decode() if e.stderr else e}")
        sys.exit(1)

    print(f"✅ 证书已生成")
    print(f"   证书：{CERT_PATH}")
    print(f"   私钥：{KEY_PATH}")
    info = verify_cert()
    if info.get("expires"):
        print(f"   到期：{info['expires']}")

    print_trust_instructions()


if __name__ == "__main__":
    main()
