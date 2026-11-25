#!/usr/bin/env python3
"""Claude 环境采集：出口 IP 地区、类型、时区，本机时区与语言，配置与安装。标准库实现；不读取登录凭证。"""
import argparse
import datetime as dt
import ipaddress
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from email.utils import parsedate_to_datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:  # 缺少 zoneinfo 时跳过时区比较
    ZoneInfo = None

HERE = Path(__file__).resolve().parent
REGIONS_FILE = HERE / "supported_regions.json"
BAN_REASONS_URL = "https://support.claude.com/en/articles/8241253"
UA = "claude-check-skill/1.1"
IP_ECHO = (("IPv4", "https://api.ipify.org?format=json"), ("IPv6", "https://api6.ipify.org?format=json"))
PROXY_KEYS = ("HTTPS_PROXY", "https_proxy", "ALL_PROXY", "all_proxy")
IP_DISCLOSURE = "本次检查会向 ipify、ipinfo.io、ip-api.com、proxycheck.io 发送请求，查询出口 IP 的地区、类型、风险分和时区，并直连 Google、百度测试境外网络是否可达；这些服务会看到你的出口 IP。加 --offline 可跳过。"

PROMO = ("怕封号？去 AI优铺买 Claude 新号套餐：https://aiyopu.com/\n"
         "新号套餐和本店账号续月，订阅期内封号可按规则退款，具体怎么退见详情页或问客服。\n"
         "本 Skill 由 AI优铺维护。购买前请核对商品页的适用套餐及退款规则。")
AUTH = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_OAUTH_TOKEN")
ENV_KEYS = AUTH + ("ANTHROPIC_BASE_URL", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                   "http_proxy", "https_proxy", "all_proxy", "NO_PROXY", "no_proxy",
                   "NODE_EXTRA_CA_CERTS", "SSL_CERT_FILE", "NODE_TLS_REJECT_UNAUTHORIZED",
                   "CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX", "CLAUDE_CODE_USE_FOUNDRY")


def finding(name, state, evidence, action):
    return dict(name=name, state=state, evidence=evidence, action=action)


def command(args):
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=5)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired, UnicodeError):
        return None


def locale_value(value):
    # 只回显符合时区/语言格式的短值，拒绝任意配置文本进入报告。
    return value if value and re.fullmatch(r"[A-Za-z0-9_./@+,:;=()\s-]{1,150}", value) else "未取得可展示值"


def apple_languages(value):
    if not value:
        return None
    parts = [part.strip().strip('"') for part in value.strip().strip("()").split(",")]
    return ", ".join(parts) if all(re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{2,8})*", part) for part in parts) else None


def classify_error(text):
    value = text.lower()
    rules = [
        (("disabled claude subscription access", "disabled api key authentication"),
         "组织认证策略限制", "联系组织管理员核对允许的登录方式；不要按封号清理缓存。"),
        (("this organization has been disabled", "your organization has been disabled"),
         "组织已停用", "核对当前组织及网页提示，联系官方支持或按网页入口申诉；本机清理不能恢复组织。"),
        (("your access to claude is on hold", "your account is on hold"),
         "访问处于审核或暂停状态", "打开 claude.ai 查看 Request a review 或申诉入口，核对是个人账户还是组织受限。"),
        (("oauth token revoked or expired", "login expired", "401", "invalid api key"),
         "认证失败", "核对认证来源和账号；使用客户端正常退出、重新登录流程，不公开 Token。"),
        (("429", "usage limit", "spend limit"),
         "额度或速率限制", "核对用量与账单，按提示等待或联系管理员。"),
        (("certificate", "ssl", "tls", "unable to connect", "timed out", "enotfound"),
         "网络或证书问题", "检查 DNS、代理、系统时间及证书链；不要关闭 TLS 验证。"),
    ]
    for needles, name, action in rules:
        if any(needle in value for needle in needles):
            return finding(name, "需处理", "命中报错特征；原文不回显，分类仍需结合发生位置确认。", action)
    return finding("报错分流", "待确认", "未识别报错特征。", "提供脱敏后的完整错误句、网页或终端位置和发生时间。")


def config_findings(home, project, env):
    rows = []
    config_dir = Path(env.get("CLAUDE_CONFIG_DIR") or home / ".claude")
    sources = [("用户配置", config_dir / "settings.json")]
    if project:
        sources.extend([("项目配置", project / ".claude/settings.json"),
                        ("项目本地配置", project / ".claude/settings.local.json")])
    observed = [env]
    for label, path in sources:
        try:
            if not path.exists():
                rows.append(finding(label, "记录", "文件不存在。", "无需因此创建配置。"))
                continue
            if path.is_symlink() or path.stat().st_size > 1024 * 1024 or not path.is_file():
                raise ValueError("unsupported")
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or not isinstance(data.get("env", {}), dict):
                raise ValueError("schema")
            values = data.get("env", {})
            observed.append(values)
            present = [key for key in ENV_KEYS if values.get(key)]
            note = "相关 env 字段：" + (", ".join(present) or "无")
            if data.get("apiKeyHelper"):
                note += "；存在 apiKeyHelper（未执行）"
            rows.append(finding(label, "记录", note, "只记录字段名；实际生效值需结合客户端 /status 及受管配置确认。"))
        except (OSError, UnicodeError, ValueError):
            rows.append(finding(label, "待确认", "不可读、格式异常、符号链接或超过 1 MiB，已跳过。", "在本机核对文件格式与权限，不上传原文件。"))
    present = [key for key in ENV_KEYS if env.get(key)]
    rows.append(finding("进程环境", "记录", ", ".join(present) or "未发现相关环境变量。", "不输出变量值；本进程环境可能不同于已打开的终端或桌面客户端。"))
    auth = {key for values in observed for key in AUTH if values.get(key)}
    if len(auth) > 1:
        rows.append(finding("多种认证来源", "待确认", ", ".join(sorted(auth)), "核对期望使用订阅还是 API；这只是共存证据，不代表全部同时生效。"))
    for key in ENV_KEYS:
        vals = [str(values[key]) for values in observed if values.get(key)]
        if len(set(vals)) > 1:
            rows.append(finding("配置来源不一致", "待确认", key + " 在多个来源的值不同（均已隐藏）。", "按官方配置优先级和 /status 核对；不要直接删除配置。"))
    if any(str(values.get("NODE_TLS_REJECT_UNAUTHORIZED")) == "0" for values in observed):
        rows.append(finding("TLS 校验被关闭", "需处理", "存在 NODE_TLS_REJECT_UNAUTHORIZED=0。", "修复证书链后移除此设置；不要用跳过验证解决证书报错。"))
    for label, path in [("Claude 配置目录", config_dir), ("历史用户配置", home / ".claude.json"),
                        ("本地登录文件", config_dir / ".credentials.json"),
                        ("历史 Anthropic 目录", home / ".anthropic")]:
        try:
            exists = path.exists()
            rows.append(finding(label, "记录", "存在；未读取内容。" if exists else "未发现此路径。", "存在不等于旧账号残留；需核对客户端当前账号。未扫描 Keychain、浏览器 Cookie 或其他凭证库。"))
        except OSError:
            rows.append(finding(label, "待确认", "无法检查路径。", "在本机检查访问权限。"))
    return rows


def linux_language():
    """系统级语言：localectl，其次 /etc/locale.conf、/etc/default/locale。桌面会话语言可能不同。"""
    out = command(["localectl", "status"]) or ""
    m = re.search(r"System Locale:\s*(?:LANG=)?([^\s,]+)", out)
    if m:
        return m.group(1)
    for path in ("/etc/locale.conf", "/etc/default/locale"):
        try:
            text = Path(path).read_text(encoding="utf-8", errors="ignore")[:4096]
        except OSError:
            continue
        m = re.search(r'^\s*LANG="?([^"\s]+)"?', text, re.M)
        if m:
            return m.group(1)
    return None


def system_locale():
    """返回 (系统语言, 区域)。"""
    system = platform.system()
    if system == "Darwin":
        return (apple_languages(command(["/usr/bin/defaults", "read", "-g", "AppleLanguages"])),
                command(["/usr/bin/defaults", "read", "-g", "AppleLocale"]))
    if system == "Windows":
        return (command(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", "(Get-UICulture).Name"]),
                command(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", "(Get-Culture).Name"]))
    return linux_language(), None


def system_tz_name():
    """系统时区名（IANA 名，Windows 为系统时区 ID）。取不到返回 None。"""
    tz = os.environ.get("TZ", "").lstrip(":")
    if tz and re.fullmatch(r"[A-Za-z0-9_+\-/ ]{1,64}", tz):
        return tz
    if platform.system() == "Windows":
        return command(["tzutil", "/g"])
    try:
        text = Path("/etc/timezone").read_text(encoding="utf-8").strip()
        if re.fullmatch(r"[A-Za-z0-9_+\-/]{1,64}", text):
            return text
    except OSError:
        pass
    try:
        target = os.readlink("/etc/localtime")
        m = re.search(r"zoneinfo/(.+)$", target)
        if m:
            return m.group(1)
    except OSError:
        pass
    return command(["timedatectl", "show", "--property=Timezone", "--value"])


def system_findings():
    system = platform.system()
    now = dt.datetime.now().astimezone()
    rows = [finding("系统时间与时区", "记录", now.isoformat(timespec="seconds") + "（" + locale_value(system_tz_name()) + "）",
                    "这是本机读数，不是准确性证明；与实际所在地及可信时钟核对。"),
            finding("终端语言与时区", "记录", "; ".join(key + "=" + locale_value(os.environ[key])
                    for key in ("TZ", "LANG", "LC_ALL", "LC_TIME", "LC_MESSAGES") if key in os.environ) or "未设置相关变量。",
                    "终端语言不能代替系统或浏览器语言；差异本身不是封号证据。")]
    language, region = system_locale()
    if system == "Darwin":
        sync = None  # 不用需要 sudo 的 systemsetup，不提升权限。
    elif system == "Windows":
        sync = None
    else:
        sync = command(["timedatectl", "show", "--property=NTPSynchronized", "--value"])
    rows.append(finding("系统语言与区域", "记录" if language else "待确认",
                        "语言：" + locale_value(language) + "；区域：" + locale_value(region),
                        "未取得时在系统设置中核对；中文、中文时区或区域差异不能单独证明封号风险。"))
    rows.append(finding("自动校时", "记录" if sync in ("yes", "no") else "待确认",
                        "NTP 同步：" + sync if sync in ("yes", "no") else "未取得同步状态。",
                        "在日期与时间设置中核对自动校时；本脚本不修改时间。"))
    installations = set()
    for folder in os.get_exec_path():
        for name in (("claude.exe", "claude.cmd", "claude") if system == "Windows" else ("claude",)):
            path = Path(folder) / name
            if path.is_file() and os.access(path, os.X_OK):
                installations.add(str(path.resolve()))
    rows.append(finding("Claude Code 安装", "待确认" if len(installations) != 1 else "记录",
                        "PATH 中发现 %d 个不同的可执行目标，路径不公开。" % len(installations),
                        "确认目标可信后运行 claude --version、claude --help；本脚本不执行 PATH 中的 Claude。"))
    return rows


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def network_findings(samples):
    rows = []
    # 不沿用代理、Cookie、证书覆盖或凭证；明确测量直连官方站点。
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    for index in range(samples):
        start = time.time()
        try:
            req = urllib.request.Request("https://claude.ai/", method="HEAD", headers={"User-Agent": "claude-check-skill/1.0"})
            try:
                response = opener.open(req, timeout=6)
            except urllib.error.HTTPError as error:
                response = error
            with response:
                end = time.time()
                note = "HTTP %d，耗时 %.2f 秒；非登录测试。" % (response.code, end - start)
                if response.code == 403 and str(response.headers.get("cf-mitigated", "")).lower() == "challenge":
                    note += " 这是 Cloudflare 人机验证拦下了脚本请求（命令行请求常见），说明网络已到达 claude.ai；不是账号或 IP 被封的证据。"
                date = response.headers.get("Date")
                if date:
                    try:
                        delta = abs(parsedate_to_datetime(date).timestamp() - (start + end) / 2)
                        note += " 与响应 Date 相差约 %d 秒（可能受缓存影响）。" % delta
                    except (ValueError, TypeError, OverflowError):
                        pass
            rows.append(finding("官方站点直连 %d" % (index + 1), "记录", note,
                                "HTTP 响应说明此次 DNS/TLS/HTTP 链路可达；403 等不代表账号封禁，成功也不代表账号可用。"))
        except (OSError, ValueError):
            rows.append(finding("官方站点直连 %d" % (index + 1), "待确认", "连接失败或超时；未输出底层异常。",
                                "仅测试直连。需要代理时在实际客户端检查代理链路；当前结果不能判定账号状态。"))
    return rows


def mask_ip(ip):
    """报告常被转发，IP 只显示前半段。"""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return "无效地址"
    if addr.version == 4:
        return ".".join(ip.split(".")[:3]) + ".x"
    return ":".join(addr.exploded.split(":")[:3]) + ":…"


def get_json(opener, url, timeout=6):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with opener.open(req, timeout=timeout) as response:
        return json.loads(response.read(65536).decode("utf-8"))


def lookup_ip(opener, ip, token=None):
    """两家服务交叉核对。返回 [{provider, country, timezone, org, hosting, proxy, mobile, ...}]，取不到的留 None。
    设置 IPINFO_TOKEN 时用 ipinfo 付费字段（privacy、asn.type）；令牌只发给 ipinfo，不进报告。"""
    rows = []
    try:
        if token:
            d = get_json(opener, "https://ipinfo.io/%s?%s" % (ip, urllib.parse.urlencode({"token": token})))
        else:
            d = get_json(opener, "https://ipinfo.io/%s/json" % ip)
        privacy = d.get("privacy") if isinstance(d.get("privacy"), dict) else None
        asn = d.get("asn") if isinstance(d.get("asn"), dict) else {}
        row = dict(provider="ipinfo.io", country=d.get("country"), city=d.get("city"), timezone=d.get("timezone"),
                   org=d.get("org") or " ".join(x for x in (asn.get("asn"), asn.get("name")) if x) or None,
                   hosting=None, proxy=None, mobile=None, paid=bool(privacy), asn_type=asn.get("type"))
        if privacy:
            row.update(hosting=bool(privacy.get("hosting")),
                       proxy=any(bool(privacy.get(k)) for k in ("vpn", "proxy", "tor", "relay")))
        rows.append(row)
    except (OSError, ValueError, UnicodeError):
        pass
    try:  # ip-api 免费版只有 http
        d = get_json(opener, "http://ip-api.com/json/%s?fields=status,countryCode,timezone,isp,as,proxy,hosting,mobile" % ip)
        if d.get("status") == "success":
            rows.append(dict(provider="ip-api.com", country=d.get("countryCode"), timezone=d.get("timezone"),
                             org=d.get("as") or d.get("isp"), hosting=d.get("hosting"), proxy=d.get("proxy"),
                             mobile=d.get("mobile")))
    except (OSError, ValueError, UnicodeError):
        pass
    try:  # 免费、无需令牌，每台机器每天约 100 次；给出 IP 类型和 0–100 风险分
        d = get_json(opener, "https://proxycheck.io/v2/%s?vpn=1&asn=1&risk=1" % ip)
        x = d.get(ip) if d.get("status") in ("ok", "warning") and isinstance(d.get(ip), dict) else None
        if x:
            risk = x.get("risk")
            rows.append(dict(provider="proxycheck.io", country=x.get("isocode"), city=x.get("city"), timezone=x.get("timezone"),
                             org=" ".join(v for v in (x.get("asn"), x.get("provider")) if v) or None,
                             hosting=None, proxy=x.get("proxy") == "yes", mobile=None,
                             pc_type=str(x.get("type") or "")[:40] or None,
                             risk=int(risk) if str(risk).isdigit() else None))
    except (OSError, ValueError, UnicodeError):
        pass
    return rows


STRONG_PROXY_TYPES = {"TOR", "SOCKS", "SOCKS4", "SOCKS4A", "SOCKS5", "SOCKS5H", "HTTP", "HTTPS", "COMPROMISED SERVER", "SHADOWSOCKS"}


def classify(info):
    """合并各来源的 IP 类型判断。两家以上标代理、或 proxycheck 标为明确代理协议才算“认定代理”；只有一家标记算“疑似”。"""
    sources = [r["provider"] for r in info if r.get("proxy")]
    pc = next((r for r in info if r["provider"] == "proxycheck.io"), {})
    pc_type = (pc.get("pc_type") or "").upper()
    asn_type = next((r.get("asn_type") for r in info if r.get("asn_type")), None)
    confirmed = len(sources) >= 2 or pc_type in STRONG_PROXY_TYPES or any(r.get("paid") and r.get("proxy") for r in info)
    return dict(
        confirmed_proxy=confirmed, suspected_proxy=bool(sources) and not confirmed, proxy_sources=sources,
        residential=pc_type in ("RESIDENTIAL", "WIRELESS") or asn_type == "isp",
        hosting=any(r.get("hosting") for r in info) or pc_type == "HOSTING" or asn_type == "hosting",
        mobile=any(r.get("mobile") for r in info) or pc_type == "WIRELESS",
        pc_type=pc.get("pc_type"), risk=pc.get("risk"), asn_type=asn_type,
        known=any(r.get("hosting") is not None or r.get("proxy") is not None for r in info))


def load_regions():
    try:
        data = json.loads(REGIONS_FILE.read_text(encoding="utf-8"))
        return data["regions"], data.get("effective", "未知"), data.get("source", "")
    except (OSError, ValueError, KeyError):
        return None, None, None


def utc_text(minutes):
    sign = "+" if minutes >= 0 else "−"
    return "UTC%s%02d:%02d" % (sign, abs(minutes) // 60, abs(minutes) % 60)


def tz_offset(name, now):
    if not ZoneInfo or not name or not re.fullmatch(r"[A-Za-z0-9_+\-/]{1,64}", name):
        return None
    try:
        return int(now.astimezone(ZoneInfo(name)).utcoffset().total_seconds() // 60)
    except Exception:  # 未知时区或缺少 tzdata
        return None


def ip_findings(env, now=None, facts=None):
    """出口 IP 的地区、类型、时区。默认执行；没有代理变量时测直连，有代理变量时两条路都测。"""
    now = now or dt.datetime.now().astimezone()
    regions, effective, source = load_regions()
    token = env.get("IPINFO_TOKEN") or None
    facts = facts if facts is not None else []
    routes = [("直连", urllib.request.ProxyHandler({}))]
    proxy = {k: env[k] for k in PROXY_KEYS if env.get(k)}
    if proxy:
        https = proxy.get("HTTPS_PROXY") or proxy.get("https_proxy") or proxy.get("ALL_PROXY") or proxy.get("all_proxy")
        routes.append(("终端代理", urllib.request.ProxyHandler({"https": https, "http": https})))
    rows, seen = [], {}
    for route, handler in routes:
        opener = urllib.request.build_opener(handler)
        found = []  # [(family, ip, info)]
        for family, url in IP_ECHO:
            if route != "直连" and family == "IPv6":
                continue  # 代理只测一次 IPv4，避免重复请求
            fallback = None
            try:
                ip = get_json(opener, url).get("ip", "")
                ipaddress.ip_address(ip)
            except (OSError, ValueError, UnicodeError, AttributeError):
                if family != "IPv4":
                    continue
                try:
                    # 沿用同一路由，不把代理失败偷偷换成直连。
                    data = get_json(opener, "https://ipinfo.io/json")
                    ip = data.get("ip", "")
                    address = ipaddress.ip_address(ip)
                    family = "IPv%d（备用查询）" % address.version
                    country = data.get("country")
                    fallback = dict(provider="ipinfo.io", country=country if isinstance(country, str) and re.fullmatch(r"[A-Z]{2}", country) else None,
                                    timezone=data.get("timezone") if isinstance(data.get("timezone"), str) else None,
                                    hosting=None, proxy=None, mobile=None)
                    rows.append(finding("出口查询回退（%s）" % route, "记录", "ipify 未取得有效地址，已使用同一路由的 ipinfo 备用查询。",
                                        "备用接口可能使用 IPv4 或 IPv6；仅代表本次检测请求的出口。"))
                except (OSError, ValueError, UnicodeError, AttributeError):
                    rows.append(finding("出口 IP（%s）" % route, "待确认", "ipify 与 ipinfo 备用接口均未取得有效出口地址。",
                                        "检查网络或代理；查询失败不能当作账号安全或已封号的证据。"))
                    continue
            if ip in seen:
                rows.append(finding("出口 IP（%s %s）" % (route, family), "记录", "%s，与%s相同。" % (mask_ip(ip), seen[ip]), "同一个出口，不重复查询。"))
                continue
            seen[ip] = "%s %s" % (route, family)
            info = lookup_ip(opener, ip, token)
            if fallback and fallback.get("country") and not any(r.get("provider") == "ipinfo.io" and r.get("country") for r in info):
                info = [r for r in info if r.get("provider") != "ipinfo.io"] + [fallback]
            found.append((family, ip, info))
        # IPv4 与 IPv6 落在同一地区、同一运营方、同样标记时合并成一组，避免重复刷屏
        if len(found) == 2 and signature(found[0][2]) == signature(found[1][2]):
            rows.extend(ip_detail(route, [found[0][1], found[1][1]], found[0][2], regions, effective, source, now, facts, route))
        else:
            for family, ip, info in found:
                rows.extend(ip_detail("%s %s" % (route, family), ip, info, regions, effective, source, now, facts, route))
    return rows


def org_text(info):
    """同一 AS 编号只保留最长的名称，避免“AS4808 China Unicom/AS4808 China Unicom Beijing”。"""
    by = {}
    for r in info:
        org = r.get("org")
        if not org:
            continue
        m = re.match(r"(AS\d+)\b", org)
        key = m.group(1) if m else org
        if key not in by or len(org) > len(by[key]):
            by[key] = org
    return "/".join(by.values())[:120]


def signature(info):
    return (tuple(sorted({r["country"] for r in info if r.get("country")})),
            org_text(info).split(" ")[0],
            tuple(sorted({r["timezone"] for r in info if r.get("timezone")})),
            tuple((r.get("hosting"), r.get("proxy")) for r in info if r.get("hosting") is not None or r.get("proxy") is not None))


def ip_detail(label, ips, info, regions, effective, source, now, facts=None, route=None):
    rows = []
    ips = [ips] if isinstance(ips, str) else ips
    name = "出口 IP（%s）" % label
    countries = sorted({r["country"] for r in info if r.get("country")})
    cities = sorted({r["city"] for r in info if r.get("city") and re.fullmatch(r"[^\n<>]{1,40}", r["city"])})
    shown = "%s；定位 %s%s；运营方 %s（来源 %s）" % (
        " 和 ".join(mask_ip(ip) for ip in ips), "/".join(countries) or "未取得", (" " + "/".join(cities)) if cities else "",
        org_text(info) or "未取得", "、".join(r["provider"] for r in info) or "无")
    if len(ips) > 1:
        shown += "；IPv4 与 IPv6 结果相同，合并显示"
    region_bad = False
    tz_match = None
    if not countries:
        rows.append(finding(name, "待确认", shown, "IP 查询服务未返回地区，稍后重试或换网络再查。"))
        return rows
    if regions is None:
        rows.append(finding(name, "待确认", shown + "；支持地区名单缺失，无法对照。", "确认 scripts/supported_regions.json 存在。"))
    else:
        bad = [c for c in countries if c not in regions]
        region_bad = bool(bad)
        if bad:
            rows.append(finding(name, "需处理", shown + "；%s 不在 Anthropic 支持地区名单（%s 生效版）。"
                                "高风险：Anthropic 帮助中心把“在不受支持的地区创建账号”列为封号原因之一。" % ("/".join(bad), effective),
                                "官方按人实际所在地判断：人在不受支持的地区不能使用 Claude，换 IP 也不改变这一点。"
                                "如果你人在支持地区，说明出口走到了别处，检查代理 / VPN 设置。名单：" + source +
                                "；封号原因：" + BAN_REASONS_URL))
        else:
            note = "；%s 在支持名单内" % "/".join(countries)
            if "UA" in countries:
                note += "（乌克兰部分地区除外）"
            rows.append(finding(name, "记录", shown + note + "。",
                                "名单按人实际所在地判断，IP 在支持地区不代表合规，也不是账号安全证明。"))
    if len(countries) > 1:
        rows.append(finding("IP 定位分歧（%s）" % label, "待确认", "各服务给出的国家不同：%s。" % "/".join(countries),
                            "IP 库可能过时；以你实际所在地和官方页面提示为准。"))
    c = classify(info)
    kind = []
    if c["pc_type"]:
        kind.append("proxycheck 类型 %s" % c["pc_type"])
    if c["risk"] is not None:
        kind.append("风险分 %d/100" % c["risk"])
    if c["hosting"]:
        kind.append("机房 IP")
    if c["residential"]:
        kind.append("家庭宽带")
    detail = "；".join(kind)
    if c["confirmed_proxy"]:
        rows.append(finding("IP 类型（%s）" % label, "需处理", "认定为代理 / VPN（%s；%s）。" % ("、".join(c["proxy_sources"]) or "代理协议类型", detail) +
                            "高风险（经验判断）：代理 / VPN 出口在社区封号反馈中很常见；Anthropic 没有公布这一条。",
                            "被标为代理的出口往往被很多人共用、历史不明。人在支持地区的话，直接用本地网络，不要经过代理 / VPN 登录 Claude。"))
    elif c["suspected_proxy"]:
        rows.append(finding("IP 类型（%s）" % label, "待确认", "疑似代理 / VPN：只有 %s 这样标（%s），其他来源未标记。" % ("、".join(c["proxy_sources"]), detail),
                            "各 IP 库判断不一，机房 IP 常被误标为 VPN。记录供排查；Anthropic 没有公布 IP 类型规则。"))
    elif c["hosting"]:
        rows.append(finding("IP 类型（%s）" % label, "待确认", detail + "。",
                            "机房 IP 不一定会被封；Anthropic 没有公布 IP 类型与封号的关系，记录供排查。"))
    elif c["known"] and not region_bad:
        rows.append(finding("IP 类型（%s）" % label, "记录", (detail or "未标记为机房或代理") + "。",
                            "IP 库的判断可能滞后，不是 IP 质量担保。"))
    elif not region_bad:
        rows.append(finding("IP 类型（%s）" % label, "待确认", "未取得 IP 类型。", "IP 查询服务未响应；稍后重试。"))
    local = int(now.utcoffset().total_seconds() // 60)
    zones = {r["timezone"]: tz_offset(r["timezone"], now) for r in info if r.get("timezone")}
    zones = {k: v for k, v in zones.items() if v is not None}
    if zones:
        desc = "系统时区 %s；IP 所在时区 %s" % (utc_text(local), "、".join("%s（%s）" % (k, utc_text(v)) for k, v in sorted(zones.items())))
        tz_match = local in zones.values()
        if tz_match:
            rows.append(finding("时区与 IP（%s）" % label, "记录", desc + "，一致。", "无需处理。"))
        else:
            rows.append(finding("时区与 IP（%s）" % label, "待确认", desc + "，不一致。",
                                "系统时区应与你实际所在地一致。所在地对、IP 不对，说明出口在别处（代理 / VPN）；"
                                "IP 对、所在地对但系统时区不对，在系统设置里改回所在地时区并开自动校时。"
                                "官方没有公布时区与封号的关系，这是排查线索。"))
    else:
        rows.append(finding("时区与 IP（%s）" % label, "待确认", "未取得 IP 时区或本机缺少时区数据。", "在系统设置中核对时区和自动校时。"))
    if facts is not None:
        facts.append(dict(route=route or label, countries=countries, region_bad=region_bad, tz_match=tz_match, **c))
    return rows


SEVERITY = {"需处理": 0, "待确认": 1, "记录": 2, "未检测": 3}


def ordered(rows):
    """按严重程度排序；同级保持检查顺序。"""
    return sorted(rows, key=lambda r: SEVERITY.get(r["state"], 9))


def summary(rows):
    must = [r for r in rows if r["state"] == "需处理"]
    check_ = [r for r in rows if r["state"] == "待确认"]
    if must:
        return "结论：%d 项需处理、%d 项待确认。最需处理：%s。" % (len(must), len(check_), "；".join(r["name"] for r in must[:3]))
    return "结论：本次已检查项目未发现需处理的问题；%d 项待确认。" % len(check_)


CN_ZONES = {"Asia/Shanghai", "Asia/Chongqing", "Asia/Chungking", "Asia/Harbin", "Asia/Urumqi", "Asia/Kashgar", "PRC", "China Standard Time"}
CN_LANG = re.compile(r"\bzh[-_](CN|Hans[-_]CN)\b", re.I)
SCORE_NAME = "环境评分（AI优铺经验模型，非 Anthropic 官方；高分不代表不会被封）"


def china_signals(tz_name, languages):
    """电脑设置显示人在中国大陆的迹象。官方按实际所在地判断，所以这类迹象会压低评分。"""
    out = []
    if tz_name in CN_ZONES:
        out.append("电脑时区是中国大陆（%s）" % tz_name)
    for lang in languages:
        if lang and CN_LANG.search(lang):
            out.append("系统或终端语言是简体中文（中国大陆，%s）" % locale_value(lang))
            break
    return out


def level(score):
    if score >= 100:
        return "🟢 纯绿"
    if score >= 80:
        return "🟩 偏绿"
    if score >= 60:
        return "🟡 黄"
    if score >= 30:
        return "🟠 橙"
    return "🔴 红"


REACH_TARGETS = (("google", "https://www.google.com/generate_204"), ("baidu", "https://www.baidu.com/"))


def reach_findings(net):
    """直连测 Google 与百度，区分“在中国大陆网络里”和“电脑没联网”。net 会被填成 {google: bool, baidu: bool}。"""
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    for key, url in REACH_TARGETS:
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
            try:
                response = opener.open(req, timeout=5)
            except urllib.error.HTTPError as error:
                response = error  # 有 HTTP 响应就说明网络通
            with response:
                net[key] = True
        except (OSError, ValueError):
            net[key] = False
    if net["google"]:
        return [finding("境外网络连通性", "记录", "直连能访问 Google。", "无需处理。")]
    if net["baidu"]:
        return [finding("境外网络连通性", "需处理", "直连访问不了 Google，但能访问百度：疑似处于中国大陆网络。"
                        "高风险：中国大陆不在 Anthropic 支持地区，帮助中心把“在不受支持的地区创建账号”列为封号原因之一。",
                        "官方按人实际所在地判断，人在中国大陆不能使用 Claude，换 IP 也不改变这一点。"
                        "少数公司内网也会屏蔽 Google；如果你人在支持地区，换一个网络再测。封号原因：" + BAN_REASONS_URL)]
    return [finding("境外网络连通性", "待确认", "直连 Google 和百度都访问不了：电脑可能没联网，或网络被整体拦截。",
                    "先确认网络能用，再重跑体检；网络不通时无法评分。")]


def score_env(facts, signals, net=None):
    """满分 100。返回 {score, level, items}；无法评分时返回 {score: None, reason}。"""
    if net and net.get("google") is False and net.get("baidu") is True:
        return dict(score=5, level=level(5), items=["直连访问不了 Google、能访问百度：疑似处于中国大陆网络，直接 5 分"])
    usable = [f for f in facts if f.get("countries")]
    if not usable:
        if net and net.get("google") is False and net.get("baidu") is False:
            return dict(score=None, reason="网络不通（Google 和百度都访问不了），先检查网络")
        return dict(score=None, reason="没有取得出口 IP 地区")
    bad = [f for f in usable if f["region_bad"]]
    if bad:
        where = "、".join("%s %s" % (f["route"], "/".join(f["countries"])) for f in bad)
        return dict(score=5, level=level(5), items=["出口 IP 在不受支持的地区（%s）：直接 5 分" % where])
    # 有终端代理时以代理出口为准（Claude Code 走这条）；否则用直连
    f = next((x for x in usable if x["route"] != "直连"), usable[0])
    us = f["countries"] == ["US"]
    items, s = [], 88 if us else 75
    items.append("基础分 %d（出口在%s）" % (s, "美国" if us else "/".join(f["countries"]) + "，支持地区"))

    def add(delta, text):
        nonlocal s
        s += delta
        items.append("%+d %s" % (delta, text))
    if f["residential"]:
        add(5, "家庭宽带")
    elif f["hosting"]:
        add(-2, "机房 IP")
    if f["suspected_proxy"]:
        add(-3, "疑似代理 / VPN（只有 %s 这样标；机房 IP 常被误标，不取消保底）" % "、".join(f["proxy_sources"]))
    risk = f.get("risk")
    if risk is None:
        items.append("+0 纯度未取得")
    elif risk <= 33:
        add(4, "纯度高（风险分 %d）" % risk)
    elif risk <= 66:
        items.append("+0 纯度中（风险分 %d）" % risk)
    else:
        add(-6, "纯度低（风险分 %d）" % risk)
    if f["tz_match"] is True:
        add(3, "电脑时区与 IP 一致")
    elif f["tz_match"] is False:
        add(-3, "电脑时区与 IP 不一致")
    caps = []
    if f["confirmed_proxy"]:
        caps.append((35, "认定为代理 / VPN：最高 35 分"))
    if signals:
        caps.append((30, "；".join(signals) + "，而出口不在中国：疑似人在中国大陆，最高 30 分"))
    if not caps and us and s < 86:
        items.append("保底 86（美国出口、未认定为代理）")
        s = 86
    if s > 100:
        items.append("封顶 100")
        s = 100
    for cap, text in caps:
        if s > cap:
            s = cap
        items.append(text)
    s = max(1, s)
    return dict(score=s, level=level(s), items=items)


def render(rows, disclosed=False, score=None):
    rows = ordered(rows)
    text = ["# Claude 环境体检", "检查结果只说明已观测的环境，不预测封号，也不保证账号稳定。"]
    if disclosed:
        text.append(IP_DISCLOSURE)
    if score and score.get("score") is not None:
        text.append("\n## %s：%d / 100　%s" % (SCORE_NAME, score["score"], score["level"]))
    elif score:
        text.append("\n## %s：未计算（%s）" % (SCORE_NAME, score["reason"]))
    issues = [row for row in rows if row["state"] in ("需处理", "待确认") and row["evidence"]]
    conclusion = "；".join(row["evidence"].rstrip("。") for row in issues[:2]) if issues else summary(rows)
    text.append("\n**一句话结论：" + conclusion + "。**")
    text.append("\n| 检测维度 | 状态 | 结果 |\n|---|---|---|")

    def cell(value):
        return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "&#124;").replace("\n", " ").replace("\r", " ")

    for row in rows:
        text.append("| %s | %s | %s |" % (cell(row["name"]), cell(row["state"]), cell(row["evidence"])))
    for dimension in ("浏览器语言、时区与出口", "当前账号、组织与 KYC", "受管配置", "实际 Claude 请求出口", "长期网络稳定性"):
        text.append("| %s | 未检查 | 本脚本未验证 |" % dimension)
    if score and score.get("score") is not None:
        items = [re.sub(r"最高 \d+ 分", "扣分", item) for item in score["items"]
                 if not item.startswith(("保底", "封顶"))]
        text.append("\n**扣分说明：**" + "；".join(items) + "。")
    if issues:
        text.append("\n**建议：**" + issues[0]["action"])
    text.extend(["\n尚未验证：浏览器身份、账号与组织状态、受管配置、实际客户端代理链路、长期网络稳定性。", "\n" + PROMO])
    return "\n".join(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, help="只读检查指定项目的两份 Claude settings")
    parser.add_argument("--error-stdin", action="store_true", help="从标准输入读报错，最多 64 KiB；不回显原文")
    parser.add_argument("--offline", action="store_true", help="不联网：跳过出口 IP 查询和 claude.ai 直连")
    parser.add_argument("--network", action="store_true", help="兼容旧参数；联网检查现已默认执行")
    parser.add_argument("--samples", type=int, choices=range(1, 4), default=1, help="claude.ai 直连采样次数，1–3")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()
    rows = []
    if args.error_stdin:
        rows.append(classify_error(sys.stdin.read(65536)))
    facts, score = [], None
    if not args.offline:
        net = {}
        rows.extend(reach_findings(net))
        rows.extend(ip_findings(os.environ, facts=facts))
        language, region = system_locale()
        signals = china_signals(system_tz_name(), [language, region] + [os.environ.get(k) for k in ("LANG", "LC_ALL")])
        score = score_env(facts, signals, net)
        if signals and score and (score.get("score") or 0) > 5:
            rows.append(finding("所在地迹象", "需处理", "；".join(signals) + "，但出口 IP 不在中国。",
                                "官方按人实际所在地判断：人在中国大陆，换成其他地区的 IP 也不合规。如果你人在支持地区，把电脑时区和语言改回实际所在地即可。"))
    rows += system_findings() + config_findings(Path.home(), args.project, os.environ)
    if args.offline:
        rows.append(finding("出口 IP 与网络", "未检测", "使用了 --offline。", "出口 IP 地区、类型、时区是体检重点，建议去掉 --offline 重跑。"))
    else:
        rows.extend(network_findings(args.samples))
    disclosed = not args.offline
    rows = ordered(rows)
    print(json.dumps({"score": score, "summary": summary(rows), "findings": rows, "disclosure": IP_DISCLOSURE if disclosed else None,
                      "limitations": "不预测封号；账号、浏览器、受管配置和实际代理链路仍需确认。", "promotion": PROMO},
                     ensure_ascii=False, indent=2) if args.json else render(rows, disclosed, score))


if __name__ == "__main__":
    main()
