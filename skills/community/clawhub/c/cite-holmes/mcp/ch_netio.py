"""cite-holmes v6.0.0 模块层：ch_netio（由手术脚本从单文件引擎分层，
判定语义与 API 见壳 verify_refs.py 与 ADR-0010）。一切跨层符号与被
测试 patch 的函数一律经 _ROOT（由壳注入主壳命名空间）——patch 语义
与 trunk/mcp 双壳隔离（目录前缀加载）共同由该机制保证。"""

import argparse
import csv
import difflib
import hashlib
import ipaddress
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import escape as html_escape
from urllib.parse import urlparse, urlunparse, quote

_ROOT = None  # 由 verify_refs 壳注入


def _bind(root):
    global _ROOT
    _ROOT = root


_OPTS = {"openalex_key": "", "s2_key": "", "mailto": "", "ncbi_key": ""}


def _ncbi_qs(extra: str = "") -> str:
    """E-utilities 查询串:可选 NCBI API key(环境 NCBI_API_KEY/--ncbi-key,
    3rps→10rps 提速并行批验证)。key 不落日志只进请求参数。"""
    qs = extra
    k = _OPTS.get("ncbi_key") or ""
    if k:
        qs += f"&api_key={quote(k, safe='')}"
    return qs


# ---------------- 主机断路器（v1.6，国内适配主攻）+ 全局网络降级（v1.10） ----------------
# 同一主机连续 _CB_THRESHOLD 次传输层失败（超时/连接重置/DNS 解析失败）→ 本批次内
# 跳过该主机的后续外呼并诚实备注，避免断网环境整批卡死（弱网痛点：等待网络响应的时间不可控）。
# HTTP 层失败（404/403/429 等站点有响应的情况）不触发熔断。main() 每次运行重置。
# v1.10 并行验证引入 _CB_LOCK：_cb_record 的「累计→熔断」是读改写序列，多 worker
# 并发下必须串行化（CPython dict 单操作原子不覆盖 check-then-act）。
# v1.10 全局网络降级：批内 ≥_NET_DEGRADE_THRESHOLD 个「不同主机」传输层失败 →
# 判定出海受限，未确认过成功的主机全部快速跳过（诚实备注+建议），不再逐主机烧超时
# ——受限网络下「等很久」的机制层缓解：一次快速诚实的通过胜过几分钟干等。
_CB_THRESHOLD = 2
_CB = {}
_CB_LOCK = threading.Lock()
_NET_DEGRADE_THRESHOLD = 3
_NET_STATE = {"fail_hosts": set(), "ok_hosts": set(), "degraded": False}


def _net_reset() -> None:
    with _CB_LOCK:
        _CB.clear()
        _NET_STATE["fail_hosts"] = set()
        _NET_STATE["ok_hosts"] = set()
        _NET_STATE["degraded"] = False


def _cb_host(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{(p.hostname or '').lower()}" if p.hostname else ""


def _cb_open(url: str) -> bool:
    """该主机是否应跳过外呼：单主机熔断，或（v1.10）全局降级下从未成功过的主机。"""
    h = _cb_host(url)
    with _CB_LOCK:
        st = _CB.get(h)
        if st and st["open"]:
            return True
        return _NET_STATE["degraded"] and h not in _NET_STATE["ok_hosts"]


def _cb_skip_note(url: str) -> str:
    h = _cb_host(url)
    with _CB_LOCK:
        degraded = _NET_STATE["degraded"] and h not in _NET_STATE["ok_hosts"]
    if degraded:
        return (
            "全局网络降级：本批次已有多个外部主机连续传输失败（出海受限特征），"
            "跳过本次外呼（建议配置代理/更换网络后重跑），本条仅按结构/其他信息判定"
        )
    return (
        f"网络断路器：{h} 本批次已连续 {_CB_THRESHOLD} 次传输失败，"
        "跳过本次外呼（避免整批卡死），本条仅按结构/其他信息判定"
    )


def _cb_record(url: str, transport_fail: bool, degrade: bool = None) -> None:
    """transport_fail=True 记一次传输层失败（累计到阈值即熔断）；
    False（拿到任意 HTTP 响应或成功）清零。v1.10：同时维护全局降级状态。
    degrade 显式传 False 表示「计入单主机熔断但不计入全局降级」——用于站点有
    HTTP 响应却被个别函数按传输失败记账的路径（如 OpenAlex 403/429、Crossref
    限流）：出海链路本身是通的，不能因为站点级反爬/限流就判定全局网络受限。"""
    h = _cb_host(url)
    if not h:
        return
    if degrade is None:
        degrade = transport_fail
    with _CB_LOCK:
        st = _CB.setdefault(h, {"fails": 0, "open": False})
        if transport_fail:
            st["fails"] += 1
            if st["fails"] >= _CB_THRESHOLD:
                st["open"] = True
            if degrade and not _NET_STATE["degraded"] and h not in _NET_STATE["ok_hosts"]:
                _NET_STATE["fail_hosts"].add(h)
                if len(_NET_STATE["fail_hosts"]) >= _NET_DEGRADE_THRESHOLD:
                    _NET_STATE["degraded"] = True
        else:
            st["fails"] = 0
            _NET_STATE["ok_hosts"].add(h)
            _NET_STATE["fail_hosts"].discard(h)


# ---------------- 公共安全/转义帮手（v1.4 评审加固） ----------------


def ssrf_blocked(url: str) -> bool:
    """SSRF 字面量防护：URL 主机部分写明回环/内网/链路本地/保留 IP 或 localhost
    时拒绝请求。**刻意不做 DNS 解析判定**——污染网络环境下解析结果不可信，
    会把正常域名误判成内网地址（实测 pubmed/doi.org 均被解析污染误伤）。
    域名类 URL 的 DNS 层防护不在本工具承诺内。"""
    host = (urlparse(url).hostname or "").lower().rstrip(".")
    if not host:
        return False
    if (
        host == "localhost"
        or host.endswith(".localhost")
        or host.endswith(".local")
        or host.endswith(".internal")
    ):
        return True
    try:
        addr = ipaddress.ip_address(host)  # 仅当主机部分本身就是 IP 字面量
    except ValueError:
        return False
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
        or addr.is_multicast
    )


# v6.6.0 F62：SSRF 拒绝话术单一来源（raise 与调用方识别共用同一常量，
# 消跨文件措辞耦合——审计 P2：此前靠子串匹配两处手工同步）
_SSRF_REFUSAL_NOTE = "重定向目标命中内网/保留地址，已拒绝（SSRF 防护）"


class GuardedRedirectHandler(urllib.request.HTTPRedirectHandler):
    """v6.6.0 F62：重定向逐跳 SSRF 复核。此前 check_url 的自动跟随路径对
    302 目标不做防护——公网 URL 经重定向跳内网/保留地址的绕过面封死
    （_fetch_landing_html 手动逐跳路径 v4.8.0 起已有每跳双门，本类补齐
    自动跟随路径）。命中即抛 URLError，由调用方按 SSRF 拒绝如实透出。"""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if ssrf_blocked(str(newurl)):
            raise urllib.error.URLError(_SSRF_REFUSAL_NOTE)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_NCBI_LAST = [0.0]
_NCBI_LOCK = threading.Lock()


def _ncbi_rate_wait():
    """E-utilities 免钥上限 3 req/秒（超限封 IP）。v1.10 并行验证下必须全局
    串行化：锁内等足 0.4 秒间隔（2.5 req/s，留安全余量），与 arXiv/S2 同模式。"""
    with _NCBI_LOCK:
        wait = 0.4 - (time.time() - _NCBI_LAST[0])
        if wait > 0:
            time.sleep(wait)
        _NCBI_LAST[0] = time.time()


_TLS_STALL_MARKERS = (
    "timed out",
    "timeout",
    "handshake",
    "ssl",
    "tls",
    "connection reset",
    "eof occurred",
)
_TLS12_CTX = [None]


def _tls12_context():
    """v6.4.0 M1：TLS1.2 降级上下文（懒构建，全局复用）。测试线实测（两度
    复现）：OpenSSL 3.0.13 与 Cloudflare TLS1.3 指纹交互对 anthropic.com/
    claude.com 必握手超时，TLS1.2 秒通——EB/OL 引用指向此类 CDN 站会被
    误判 unreachable。仅在 _urlopen_retry 的 TLS 特征异常后降级一试。"""
    if _TLS12_CTX[0] is None:
        import ssl

        ctx = ssl.create_default_context()
        try:
            ctx.options |= ssl.OP_NO_TLSv1_3
        except AttributeError:
            pass  # 老版本 OpenSSL 无该旗标=无 TLS1.3 可禁
        _TLS12_CTX[0] = ctx
    return _TLS12_CTX[0]


def _urlopen_retry(req, timeout: float, attempts: int = 3, backoff: float = 1.5):
    """v4.1.0 传输层重试（与 pmid_doi_crosscheck v3.3.0 同标准，收拢为公共助手）。

    只重试传输类异常（URLError/超时/SSL 握手失败——代理抖动/TUN 环境实测高频）；
    HTTPError 是服务器已应答（429/404/403），绝不重试，由调用方走各自可观测路径。
    全部 attempts 耗尽后抛出最后一次异常——调用方负责把「传输失败」与「查无」
    区分开（2026-10-16 实测事故：传输失败曾被当成查无 → 12+ 条真文献被报 unverified）。

    v6.3.1 代理自愈：环境带代理变量且传输失败时，先用无代理 opener 直连试一次
    再进入常规退避（2026-11-13 实测：代理栈故障期 18/18 全 unreachable、CiteScore
    假 0/D 两连发，而同环境直连健康——代理在场≠代理可用，自愈优于把 unreachable
    全量甩给人工复核）。

    v6.4.0 M1 TLS 降级（测试线 P0）：传输异常含 TLS 指纹特征词（超时/握手/
    ssl）且 https 目标时，用 OP_NO_TLSv1_3 上下文重试一次——OpenSSL 3.0.13
    与 Cloudflare TLS1.3 指纹交互对部分 CDN 站必超时（TLS1.2 秒通），不降级
    会把可达站误判 unreachable。判定语义零改动（失败仍按传输失败上抛）。
    """
    last_exc = None
    use_direct = False
    tls12_tried = False  # M1：TLS1.2 降级重试只试一次（防降级路径循环）
    tries = 0
    max_tries = attempts + (1 if urllib.request.getproxies() else 0)
    while tries < max_tries:
        tries += 1
        try:
            if use_direct:
                import os

                # 陷阱（2026-11-13 单变量实验实证）：代理路径首轮会把代理地址
                # 烘焙进 Request.host（如 127.0.0.1:7890）——复用被污染对象时
                # 即使换了无代理 opener 仍连死代理。直连必须重建请求对象。
                direct_req = urllib.request.Request(
                    req.full_url,
                    data=req.data,
                    headers=dict(req.header_items()),
                    method=req.get_method(),
                )
                # 走 urlopen（而非自建 opener.open）保持与调用方/测试同一入口：
                # ①测试对 urllib.request.urlopen 的统一 mock 在直连分支同样生效
                #   （自建 opener.open 会绕过 mock 打真网——9 用例回归实证）；
                # ②清代理 env + 装无代理默认 opener 实现"urlopen 但直连"。
                # install_opener 全局副作用=本进程此后默认直连：代理栈已证实
                # 故障的会话里这是期望行为（会话级自愈）。
                _saved = {
                    k: os.environ.pop(k)
                    for k in (
                        "http_proxy",
                        "https_proxy",
                        "HTTP_PROXY",
                        "HTTPS_PROXY",
                        "all_proxy",
                        "ALL_PROXY",
                    )
                    if k in os.environ
                }
                try:
                    urllib.request.install_opener(
                        urllib.request.build_opener(urllib.request.ProxyHandler({}))
                    )
                    return urllib.request.urlopen(direct_req, timeout=timeout)
                finally:
                    os.environ.update(_saved)
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.HTTPError:
            raise
        except Exception as e:
            last_exc = e
            if not use_direct and urllib.request.getproxies():
                use_direct = True  # 代理在场且传输失败 → 立即无代理直连一试
                continue
            # v6.4.0 M1（测试线 P0）：TLS 指纹性超时 → TLS1.2 上下文重试一次。
            # 实测（测试线 2026-11-13，两度复现）：OpenSSL 3.0.13 与 Cloudflare
            # TLS1.3 指纹交互对 anthropic.com/claude.com 必握手超时（TLS1.2 秒通、
            # node undici 不受影响）——EB/OL 引用指向此类 CDN 站会被误判
            # unreachable。特征词命中即降级一试；mock 签名不含 context 时
            # TypeError 回退常规重试（密封兼容）。
            if (
                not tls12_tried
                and str(getattr(req, "full_url", "")).startswith("https")
                and any(m in str(e).lower() for m in _TLS_STALL_MARKERS)
            ):
                tls12_tried = True
                try:
                    # 对抗审计观察（v6.4.0）：代理路径可能把代理地址烘焙进
                    # req.host（v6.3.1 注释已立档的陷阱）——降级轮与直连自愈
                    # 分支同刀：重建请求对象，防降级轮连死代理。
                    tls_req = urllib.request.Request(
                        req.full_url,
                        data=req.data,
                        headers=dict(req.header_items()),
                        method=req.get_method(),
                    )
                    return urllib.request.urlopen(
                        tls_req, timeout=timeout, context=_tls12_context()
                    )
                except TypeError:
                    pass  # 密封 mock 严格签名——回退常规退避路径
                except Exception as e2:
                    last_exc = e2  # 降级一试仍败：原样进入退避（不掩盖真实失败）
            if tries < max_tries:
                time.sleep(backoff * tries)
    raise last_exc


def _host_of(url: str) -> str:
    m = re.match(r"https?://([^/:?#]+)", str(url or ""), re.I)
    return m.group(1).lower() if m else ""


_ARXIV_LAST = [0.0]
_ARXIV_LOCK = threading.Lock()


def _arxiv_rate_wait():
    """export.arxiv.org 官方礼貌上限：同一客户端 ≥3 秒/请求（仅 arXiv 查询互相控频）。
    v1.10：加锁——并行 worker 下也保持全局限速（先到者持锁等待，计时刻整体串行）。"""
    with _ARXIV_LOCK:
        wait = 3.0 - (time.time() - _ARXIV_LAST[0])
        if wait > 0:
            time.sleep(wait)
        _ARXIV_LAST[0] = time.time()


_RETRACTION_CACHE = [None]  # 惰性加载:--retraction-cache 指向 JSON 索引
# {doi_lower: {"date","type","reason"}}(Crossref GitLab 官方 dump 构建,63k+ 条)


_S2_LAST = [0.0]
_S2_LOCK = threading.Lock()


def _s2_rate_wait():
    """免钥走 S2 共享限速池（约 100 请求/5 分钟），客户端串行化 ≥1.5 秒/请求。
    v1.10：加锁——并行 worker 下保持全局串行（否则并发线程同时读到旧时刻，
    一起通过等待，实际请求间隔被压缩）。"""
    with _S2_LOCK:
        wait = 1.5 - (time.time() - _S2_LAST[0])
        if wait > 0:
            time.sleep(wait)
        _S2_LAST[0] = time.time()


def _cache_key(ref: dict) -> tuple:
    """v1.10 批内缓存键：doi → url → pmid → arxiv 取首个可用标识；全无则 ()（不缓存）。
    仅作缓存命中优化，不参与判定；判定顺序与 mark_duplicates 去重一致（url/doi/pmid）。"""
    doi = str(ref.get("doi") or "").strip()
    if doi:
        return ("doi", doi.lower())
    u = str(ref.get("url") or "").strip()
    if u:
        return ("url", _ROOT.normalize_url(u))
    pmid = str(ref.get("pmid") or "").strip()
    if pmid:
        return ("pmid", pmid)
    ax = _ROOT.extract_arxiv_id(ref)
    if ax:
        return ("arxiv", ax)
    return ()


# ---------------- 持久磁盘缓存（v1.12：复跑不出国，判定口径一致） ----------------
# ~/.cache/cite-holmes/cache.sqlite3（标准库 sqlite3）。键=影响判定的全部输入字段
# （同 DOI 不同声称标题/年份必须分开——标题相似度判定依赖声称值）+ 验证器版本 + 预设。
# 只缓存稳定判定 verified/partial/invalid；unreachable（瞬态）与 offline 结果不缓存。
# --strict 强制绕过读（CI 诚实）；--refresh-cache 绕过读但仍写；写失败静默（缓存绝不影响验证）。
_DC_CACHEABLE = {"verified", "partial", "invalid"}


def _dc_key(ref: dict, profile: str) -> str:
    basis = {
        k: ref.get(k)
        for k in ("doi", "url", "pmid", "arxiv", "title", "year", "source", "authors", "tier")
    }
    basis["_v"] = _ROOT.VERSION
    basis["_p"] = profile
    raw = json.dumps(basis, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


# ---------------- L4 证据升级级联（v3.0.0,DeepSciVerify 两级联开源化） ----------------


def _dc_path(args) -> str:
    return os.path.abspath(os.path.expanduser(args.cache_path))


def _dc_get(path: str, key: str, ttl_h: float):
    """命中且未过期 → (result_dict, age_hours)；未命中/坏库/坏行 → None（静默）。"""
    if not key:
        return None
    try:
        import sqlite3

        os.makedirs(os.path.dirname(path), exist_ok=True)
        conn = sqlite3.connect(path)
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS dc(" "k TEXT PRIMARY KEY, ts REAL, payload TEXT)"
            )
            row = conn.execute("SELECT ts, payload FROM dc WHERE k=?", (key,)).fetchone()
        finally:
            conn.close()
    except Exception:
        return None
    if not row:
        return None
    ts, payload = row
    age_h = (time.time() - ts) / 3600.0
    if age_h > max(0.0, ttl_h):
        return None
    try:
        r = json.loads(payload)
    except Exception:
        return None
    if not isinstance(r, dict) or not r.get("verdict"):
        return None
    return r, age_h


def _dc_put(path: str, key: str, result: dict) -> None:
    if not key:
        return
    try:
        import sqlite3

        os.makedirs(os.path.dirname(path), exist_ok=True)
        slim = {k: v for k, v in result.items() if k != "index"}
        conn = sqlite3.connect(path)
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS dc(" "k TEXT PRIMARY KEY, ts REAL, payload TEXT)"
            )
            conn.execute(
                "INSERT OR REPLACE INTO dc(k, ts, payload) VALUES (?,?,?)",
                (key, time.time(), json.dumps(slim, ensure_ascii=False)),
            )
            conn.commit()
        finally:
            conn.close()
    except Exception:
        pass  # 缓存写失败绝不影响验证本身
