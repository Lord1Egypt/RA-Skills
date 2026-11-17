"""底层工具：日期解析、网络 IO、区域/代理探测。

所有函数无业务依赖，供其它子模块引用。
外部使用请直接 `from aiweekly.utils import ...`；`aiweekly/__init__.py` 亦做了导出。
"""
import html
import json
import os
import random
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

# 使用常规浏览器 UA：部分站点对自报爬虫身份的 UA 会返回 429，改用常规 UA 以正常获取公开 RSS。
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# 出站代理：适用于「所有出站流量必须经统一代理」的网络架构（如企业内网）。
# 来源优先级为 --proxy 参数 / HTTPS_PROXY 等环境变量 / 系统代理设置；默认直连。
_PROXY_OVERRIDE = None  # 由 configure_proxy() 写入

_SOCKS_ACTIVE = False  # 由 _configure_proxy() 在启用 SOCKS 时置位


def resolve_proxy() -> str:
    """探测可用的出站代理，优先级：CLI --proxy > 环境变量 > 系统代理。

    - CLI --proxy：由 ``configure_proxy()`` 写入 ``_PROXY_OVERRIDE``；
    - 环境变量：``HTTPS_PROXY`` / ``https_proxy`` / ``HTTP_PROXY`` / ``http_proxy``；
    - 系统代理：Windows 注册表 Internet Settings、macOS ``scutil --proxy``、
      Linux ``gsettings``（无需用户手动 ``export`` 环境变量即可自动沿用系统设置）；
    全无则返回 ``""``（直连）。任何探测异常均静默降级为直连，绝不阻断抓取。

    示例：
        >>> resolve_proxy()                                   # doctest: +SKIP
        ''
    """
    p = _PROXY_OVERRIDE or os.environ.get("HTTPS_PROXY") \
        or os.environ.get("https_proxy") or os.environ.get("HTTP_PROXY") \
        or os.environ.get("http_proxy")
    if p:
        return p
    return _detect_system_proxy()


def _resolved_proxy() -> str:
    """向后兼容别名：复用 ``resolve_proxy()`` 的完整探测链（generate_site.py 仍引用）。"""
    return resolve_proxy()


# 系统代理探测结果缓存：避免每次 ``_build_opener()`` / ``_probe()`` 重复读注册表/调子进程。
_SYSTEM_PROXY_CACHE = None


def _detect_system_proxy() -> str:
    """探测操作系统级代理设置（env/CLI 均未指定时的最后兜底）。

    支持 Windows 注册表、macOS ``scutil --proxy``、Linux ``gsettings``。
    任何异常均静默返回 ``""``（回退直连），探测失败不阻断上层抓取。
    """
    global _SYSTEM_PROXY_CACHE
    if _SYSTEM_PROXY_CACHE is not None:
        return _SYSTEM_PROXY_CACHE
    _SYSTEM_PROXY_CACHE = ""
    try:
        if os.name == "nt":
            _SYSTEM_PROXY_CACHE = _win_proxy_from_registry()
        elif sys.platform == "darwin":
            _SYSTEM_PROXY_CACHE = _mac_proxy_from_scutil()
        elif os.name == "posix":
            _SYSTEM_PROXY_CACHE = _linux_proxy_from_gsettings()
    except Exception:  # noqa: BLE001 系统代理探测失败应静默降级为直连
        _SYSTEM_PROXY_CACHE = ""
    return _SYSTEM_PROXY_CACHE


def _norm_proxy_endpoint(endpoint: str) -> str:
    """给缺 scheme 的代理端点补 ``http://``，确保 urllib ProxyHandler 可用。"""
    endpoint = (endpoint or "").strip()
    if not endpoint:
        return ""
    if "://" in endpoint:
        return endpoint
    return "http://" + endpoint


def _norm_proxy_server(server: str) -> str:
    """把系统代理串（可能含 per-scheme 或多条目）规整为单个代理 URL。

    Windows 注册表 ``ProxyServer`` 常为 ``http=host:port;https=host:port``
    或裸 ``host:port``。优先取 https，其次 http，最后裸串。
    """
    server = (server or "").strip()
    if not server:
        return ""
    parts = [p.strip() for p in server.split(";") if p.strip()]
    if len(parts) > 1:
        for p in parts:
            low = p.lower()
            if low.startswith("https="):
                return _norm_proxy_endpoint(p.split("=", 1)[1])
            if low.startswith("http="):
                return _norm_proxy_endpoint(p.split("=", 1)[1])
    return _norm_proxy_endpoint(server)


def _win_proxy_from_registry() -> str:
    """从 Windows 注册表读取 IE/系统代理（Internet Settings）。

    ``ProxyEnable=1`` 且 ``ProxyServer`` 非空时返回规整后的代理 URL；
    否则返回 ``""``（直连）。``AutoConfigURL``(PAC) 不解析（需取 .pac 内容，
    复杂度高、价值低，受限网络下 PAC 多已不可用，故忽略）。
    """
    try:
        import winreg
    except ImportError:
        return ""
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        ) as key:
            try:
                enabled, _ = winreg.QueryValueEx(key, "ProxyEnable")
            except OSError:
                return ""
            if not enabled:
                return ""
            try:
                server, _ = winreg.QueryValueEx(key, "ProxyServer")
            except OSError:
                return ""
            return _norm_proxy_server(server)
    except OSError:
        return ""


def _mac_proxy_from_scutil() -> str:
    """macOS：解析 ``scutil --proxy`` 输出的系统代理配置。

    优先 ``HTTPSProxy:HTTPSPort``，其次 ``HTTPProxy:HTTPPort``；
    ``*Enable=0`` 或无值返回 ``""``。
    """
    try:
        out = subprocess.run(
            ["scutil", "--proxy"], capture_output=True, text=True, timeout=10
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return ""
    cfg: dict = {}
    for line in out.splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if k in ("HTTPEnable", "HTTPSEnable", "HTTPProxy", "HTTPSProxy",
                 "HTTPPort", "HTTPSPort"):
            cfg[k] = v
    https_on = cfg.get("HTTPSEnable") == "1"
    http_on = cfg.get("HTTPEnable") == "1"
    if https_on and cfg.get("HTTPSProxy"):
        return _norm_proxy_endpoint(
            f"{cfg['HTTPSProxy']}:{cfg.get('HTTPSPort', '443')}")
    if http_on and cfg.get("HTTPProxy"):
        return _norm_proxy_endpoint(
            f"{cfg['HTTPProxy']}:{cfg.get('HTTPPort', '80')}")
    return ""


def _linux_proxy_from_gsettings() -> str:
    """Linux(GNOME)：读取 gsettings 系统代理（mode=manual 时有效）。

    优先 https，其次 http；非 manual 模式或无 gsettings 返回 ``""``。
    """
    try:
        mode = subprocess.run(
            ["gsettings", "get", "org.gnome.system.proxy", "mode"],
            capture_output=True, text=True, timeout=10,
        ).stdout.strip().strip("'\"")
    except (OSError, subprocess.SubprocessError):
        return ""
    if mode != "manual":
        return ""
    for grp in ("org.gnome.system.proxy.https", "org.gnome.system.proxy.http"):
        try:
            host = subprocess.run(
                ["gsettings", "get", grp, "host"],
                capture_output=True, text=True, timeout=10,
            ).stdout.strip().strip("'\"")
            port = subprocess.run(
                ["gsettings", "get", grp, "port"],
                capture_output=True, text=True, timeout=10,
            ).stdout.strip().strip("'\"")
        except (OSError, subprocess.SubprocessError):
            continue
        if host:
            return _norm_proxy_endpoint(f"{host}:{port or '8080'}")
    return ""


def _configure_proxy():
    """根据 _resolved_proxy() 配置代理（在抓取前调用一次）。

    - http/https 代理：由各 _build_opener() 按请求挂载，无需全局状态；
    - socks5/socks4 代理：需要 PySocks，通过 socks.wrapmodule(urllib.request)
      全局生效，并置 _SOCKS_ACTIVE 以免重复挂载 http ProxyHandler。
    """
    global _SOCKS_ACTIVE
    _SOCKS_ACTIVE = False
    proxy = _resolved_proxy()
    if not proxy:
        return
    if proxy.startswith("socks"):
        try:
            import socks  # PySocks
            scheme, _, rest = proxy.partition("://")
            auth_hostport = rest
            username = password = None
            if "@" in rest:
                auth, auth_hostport = rest.rsplit("@", 1)
                if ":" in auth:
                    username, password = auth.split(":", 1)
            host, _, port = auth_hostport.rpartition(":")
            stype = socks.SOCKS5 if scheme in ("socks5", "socks5h") else socks.SOCKS4
            socks.set_default_proxy(stype, host, int(port), rdns=(scheme == "socks5h"),
                                    username=username, password=password)
            socks.wrapmodule(urllib.request)
            _SOCKS_ACTIVE = True
            print(f"  🔌 已启用 SOCKS 代理：{host}:{port}（PySocks）")
        except ImportError:
            print("  ⚠️ 检测到 SOCKS 代理但未安装 PySocks，无法使用。"
                  " 请运行：pip install PySocks（在 aiweekly venv 中），或改用 HTTP 代理。")
        except Exception as e:
            print(f"  ⚠️ SOCKS 代理配置失败：{e}")


def configure_proxy(proxy: str | None = None) -> str:
    """设置本次运行的出站代理并立即生效（CLI ``--proxy`` 的唯一入口）。

    输入：proxy — 代理 URL（``http://host:port`` / ``socks5://…``）；
          为 ``None`` 时只沿用现有来源（环境变量 / 系统代理）重配一次。
    输出：本次实际生效的代理串（``""`` 表示直连）。
    异常：不抛——SOCKS 缺 PySocks 等情况由 ``_configure_proxy`` 内部告警降级。

    为什么要有这个函数：此前 CLI 直接赋值 ``utils._PROXY_OVERRIDE``，
    属于「跨模块改写别人的私有全局」，且代理生效与否取决于调用顺序。
    统一走本入口后，设置与生效是一步，调用方无需知道内部全局叫什么。
    """
    global _PROXY_OVERRIDE
    if proxy is not None:
        _PROXY_OVERRIDE = proxy
    _configure_proxy()
    return resolve_proxy()


def _build_opener():
    """构造带代理的 opener，**校验证书链与主机名**。

    历史实现曾显式关闭证书校验（既不校验主机名、也不校验证书链），
    其效果是：任何持有任意自签证书的中间人都能冒充上游站点，而抓取到的 RSS 正文会
    原样进入本期报告。已改为 ``ssl.create_default_context()`` 的默认行为（强制校验证书链与主机名）。

    若出站流量须经企业代理做 TLS 拦截，正确做法是把代理根证书装入系统信任库
    （或指向 ``SSL_CERT_FILE``），而不是退回关闭校验。
    """
    handlers = []
    proxy = _resolved_proxy()
    if proxy and not _SOCKS_ACTIVE:
        handlers.append(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    handlers.append(
        urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    return urllib.request.build_opener(*handlers)


def _http_get(url: str, timeout: int = 45, opener=None) -> str:
    """抓取 URL 文本内容。

    输入：
        url     — 目标地址；
        timeout — 单次请求超时（秒，默认 45）；
        opener  — **依赖注入点（P1#6）**：任意实现 `.open(req, timeout=)` 的对象。
                  为 None 时用 `_build_opener()` 真实网络；单测传 mock 即可脱网。
    输出：解码后的响应正文（utf-8，非法字节 replace）。
    异常：向上抛 `urllib.error.URLError` / `TimeoutError` 等，由调用方的
          `_retry_fetch` 或 best-effort 容错块处理。
    示例：
        >>> _http_get("https://example.com", timeout=5)          # doctest: +SKIP
        >>> _http_get("x", opener=FakeOpener("<html/>"))         # doctest: +SKIP
    """
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    opener = opener or _build_opener()
    with opener.open(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def _probe(url: str, timeout: int = 8, opener=None) -> bool:
    """轻量连通性探测：能拿到响应即视为可达（不解析内容）。

    输入：url / timeout（秒）/ opener（依赖注入点，同 `_http_get`）。
    输出：bool，可达为 True。
    异常：不抛——任何异常都被视为「不可达」返回 False（探测语义要求永不中断上层）。
    示例：
        >>> _probe("https://www.baidu.com", 6)                   # doctest: +SKIP
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        with (opener or _build_opener()).open(req, timeout=timeout) as r:
            r.read(256)
        return True
    except Exception:  # noqa: BLE001 探测语义：任何失败都只意味着「不可达」
        return False


def _detect_region(probe=None) -> str:
    """探测当前运行环境是 cn / global / unknown。

    输入：probe — 依赖注入点（P1#6），签名同 `_probe(url, timeout)`；None 用真实探测。
    输出：`"cn"` / `"global"` / `"unknown"`。双通时返回 global（榜源更丰富）。
    异常：不抛（内部全部走 `_probe` 的静默语义）。
    示例：
        >>> _detect_region(probe=lambda u, t=6: "baidu" in u)
        'cn'

    国内哨兵：baidu（必通）+ OpenCompass（学术榜）
    国外哨兵：lmarena + huggingface
    """
    _p = probe or _probe
    cn_ok = _p("https://www.baidu.com", 6) or _p("https://rank.opencompass.org.cn/leaderboard-llm", 6)
    foreign_ok = _p("https://lmarena.ai/leaderboard", 8) or _p("https://huggingface.co", 6)
    if cn_ok and not foreign_ok:
        return "cn"
    if foreign_ok and not cn_ok:
        return "global"
    if cn_ok and foreign_ok:
        return "global"  # 双通时按国外优先级（榜源更丰富）
    return "unknown"


def _retry_fetch(fn, attempts: int = 3, base: float = 1.0, cap: float = 30.0, sleeper=None):
    """指数退避 + 随机抖动重试（P0#10）：best-effort，不向上层抛异常。

    输入：
        fn       — 无参可调用；返回任意值即视为成功；
        attempts — 最大尝试次数（默认 3）；
        base/cap — 退避基数与上限（秒）；
        sleeper  — **依赖注入点（P1#6）**，签名 `f(seconds)`；单测传 `lambda s: None`
                   可让重试路径瞬时跑完，不再真 sleep。
    输出：`fn()` 的返回值；全部失败返回 None，由调用方兜底（缓存快照 / 标注「暂无实时数据」）。
    异常：不抛——通用重试包装必须吞掉所有异常（已加 noqa 说明）。
    示例：
        >>> _retry_fetch(lambda: 1)
        1
        >>> _retry_fetch(lambda: (_ for _ in ()).throw(OSError), attempts=2,
        ...              sleeper=lambda s: None) is None            # doctest: +SKIP
        True

    - 第 i 次失败后等待 `min(cap, base * 2**i) + 随机抖动` 秒，避免与上游限流同步重试。
    """
    _sleep = sleeper or time.sleep
    last_err = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001 通用重试包装，必须吞掉所有异常
            last_err = e
            if i < attempts - 1:
                sleep_s = min(cap, base * (2 ** i)) + random.uniform(0, 1.0)
                _sleep(sleep_s)
    print(f"  ⚠️ 重试 {attempts} 次后仍失败：{last_err}")
    return None


def _parse_iso_datetime(s) -> "datetime | None":
    """解析 ISO 8601 字符串为 datetime（兼容尾随 Z / 时区偏移）。

    失败（含空值）返回 None，由调用方决定回退策略，不抛。
    内部集中处理 `...Z` → `...+00:00` 的兼容转换，避免散落各处重复。
    """
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).strip().replace("Z", "+00:00"))
    except ValueError:
        return None


def _parse_date_arg(token: str):
    """日期参数 -> datetime（P0#15/16：完整 ISO 8601 或 YYYY-MM-DD）。

    用于 --date 固定报告周期（便于复现）。非法输入显式抛 ValueError，
    不再把解析失败静默吞掉。
    """
    s = str(token).strip()
    dt = _parse_iso_datetime(s)
    if dt is not None:
        return dt
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"无法解析 --date 参数（需 YYYY-MM-DD 或 ISO 8601）：{token!r}")


def _parse_snapshot_date(snap: str):
    """快照日期字符串 -> date；解析失败回退 None（P0#17：已支持完整 ISO 8601）。

    返回 `datetime.date`（非 datetime）以兼容 `_leaderboard_freshness` 的
    `report_date.date() - d` 算术；改返回 datetime 需同步下游 `.date()` 调用。
    """
    if not snap:
        return None
    dt = _parse_iso_datetime(snap)
    if dt is not None:
        return dt.date()
    try:
        return datetime.strptime(str(snap).strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def load_json(path, default=None):
    """读取 JSON 文件（best-effort，不抛）。

    文件不存在 / 解析失败均返回 `default`，由调用方决定回退策略。
    集中消除各模块手写 `Path.read_text` + `json.loads` 的重复样板。
    """
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def save_json(path, obj, indent: int = 2) -> None:
    """原子化写入 JSON 文件（先写 .tmp 再 rename，避免半截文件被下游读到）。

    `ensure_ascii=False` 保留中文可读；`indent=2` 与历史产物格式一致。
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=indent), encoding="utf-8")
    tmp.replace(p)


def safe_url(u: str) -> str:
    """仅放行 http(s)/mailto 协议的 URL，其余一律回退 ``'#'``。

    用途：把**外部可控**的 URL（RSS 条目的 link、用户 ``--news-api`` 传入的来源地址）
    写进 ``href`` 前先过一遍，挡掉 ``javascript:`` / ``data:`` 这类危险协议。

    输入：任意字符串；``None`` 与空串视为不放行。
    输出：原字符串（协议在白名单内）或 ``'#'``。
    注意：本函数**不做 HTML 转义**。要写进属性请改用 :func:`safe_href`。
    """
    from urllib.parse import urlparse
    try:
        scheme = urlparse(u or "").scheme.lower()
    except ValueError:
        return "#"
    return u if scheme in ("http", "https", "mailto") else "#"


def safe_href(u: str) -> str:
    """返回可直接写进 ``href="..."`` 的值：协议白名单 + 属性上下文转义。

    两步缺一不可——:func:`safe_url` 挡危险协议，``html.escape(quote=True)``
    挡 ``"`` 提前闭合属性（如 ``https://x/a" onmouseover="alert(1)``）。
    历史上 ``market.py`` 直接拼 ``f'<a href="{u}">'``，两样都没做。
    """
    return html.escape(safe_url(u), quote=True)


def js_str_in_attr(s: str) -> str:
    """把字符串安全放进「HTML 属性里的 JS 单引号字符串字面量」。

    典型上下文：``onclick="switchAudience('X', this)"``。

    两层转义缺一不可：
      1. **JS 层**——先转义 ``\\`` / ``'`` / 换行，否则可闭合 JS 字符串；
      2. **HTML 层**——再做 ``html.escape(quote=True)``，否则 ``"`` 可闭合属性。

    注意**只做 html.escape 是不够的**：浏览器会先对属性值做实体解码，再把结果
    交给 JS 解析，因此 ``&#x27;`` 解码回 ``'`` 后照样能闭合字符串——这正是
    ``insights.py`` 受众 chip 历史上的写法。
    """
    if not s:
        return ""
    js = (s.replace("\\", "\\\\").replace("'", "\\'")
          .replace("\n", "\\n").replace("\r", "\\r"))
    return html.escape(js, quote=True)


__all__ = [
    "_UA", "_PROXY_OVERRIDE", "_SOCKS_ACTIVE",
    "resolve_proxy", "configure_proxy", "_resolved_proxy", "_configure_proxy", "_build_opener",
    "_http_get", "_probe", "_detect_region", "_retry_fetch",
    "_parse_iso_datetime", "_parse_date_arg", "_parse_snapshot_date",
    "load_json", "save_json", "safe_url", "safe_href", "js_str_in_attr",
]