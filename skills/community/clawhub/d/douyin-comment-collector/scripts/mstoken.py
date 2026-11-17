"""抖音 msToken 自动换发（低风险移植，无 a_bogus / 无浏览器）。

来源：开源 DouYin_Spider 的 ``utils/mstoken.py`` + ``utils/strdata_pure.py`` + ``utils/fingerprint.py``。

思路：向字节官方的 mssdk 上报端点（``https://mssdk.bytedance.com``）POST 一段
**静态指纹 + RC4 加密**的 ``strData``，服务端在响应头 ``x-ms-token`` 下发一个真实可用的 msToken。

────────────────────────────────────────────────────────────────────────────
为何低风险（不踩签名逆向红线）：
- **不逆向 a_bogus / X-Bogus**：本模块只调用字节自己的 SDK 端点换 token，
  相当于「向官方要」，而非伪造签名去对抗风控。
- **无浏览器**：纯 httpx POST，可在无头服务器跑，是评论通道「抢页面签名」之外
  的**独立 token 源**。
- **600s 惰性缓存**：避免高频请求触发风控。

调用 ``get_mstoken(cookie_str)`` 返回非空字符串即成功；失败返回空串（调用方应降级）。
"""

from __future__ import annotations

import json
import logging
import random
import re
import time
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

_REPORT_URL = "https://mssdk.bytedance.com/web/common?ms_appid=6383"
_TTL = 600  # 秒（开源同值，抖音 msToken 有效期约 10 分钟）

# RC4 + 自定义 base64 字符表（开源 CUSTOM 常量，逐字符一致）
_CUSTOM_B64 = "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe"

# 静态指纹模板（开源 FINGERPRINT_TEMPLATE，纯预设，无真实设备信息）
_FINGERPRINT_TEMPLATE = (
    '{"tokenList":[],"navigator":{"appCodeName":"Mozilla","appMinorVersion":"undefined",'
    '"appName":"Netscape","appVersion":"5.0 (Windows)","buildID":"undefined","doNotTrack":"null",'
    '"msDoNotTrack":"undefined","oscpu":"undefined","platform":"Win32","product":"Gecko",'
    '"productSub":"20030107","cpuClass":"undefined","vendor":"Google Inc.","vendorSub":"undefined",'
    '"deviceMemory":"8","language":"zh-CN","systemLanguage":"undefined","userLanguage":"undefined",'
    '"webdriver":"false","cookieEnabled":1,"vibrate":4,"credentials":4,"storage":4,'
    '"requestMediaKeySystemAccess":4,"hardwareConcurrency":12,"maxTouchPoints":-1,'
    '"languages":"zh-CN,zh","touchEvent":1,"touchstart":2},"wID":{"load":0,"nap":"6",'
    '"nativeLength":33,"jsFontsList":"0","timestamp":"1784564385945","timezone":8,"magic":3,'
    '"canvas":"-1","wProps":374262,"dProps":2,"jsv":"","browserType":0,"iframe":2,"aid":0,'
    '"msgType":1,"privacyMode":0,"aidList":[],"index":1},"window":{"Image":3,"isSecureContext":4,'
    '"ActiveXObject":4,"toolbar":4,"locationbar":4,"external":4,"mozRTCPeerConnection":4,'
    '"postMessage":3,"webkitRequestAnimationFrame":4,"BluetoothUUID":4,"netscape":4,"localStorage":11,'
    '"sessionStorage":11,"indexDB":4,"devicePixelRatio":1,"location":"https://www.douyin.com/"},'
    '"webgl":{},"document":{"characterSet":"UTF-8","compatMode":"undefined","documentMode":"undefined",'
    '"layers":4,"all":4,"images":4},"screen":{"innerWidth":1707,"innerHeight":809,"outerWidth":1707,'
    '"outerHeight":912,"screenX":0,"screenY":0,"pageXOffset":0,"pageYOffset":0,"availWidth":1707,'
    '"availHeight":912,"sizeWidth":1707,"sizeHeight":960,"clientWidth":1697,"clientHeight":809,'
    '"colorDepth":24,"pixelDepth":24},"plugins":{"plugin":[],"pv":"0"},"custom":{}}'
)

_GEO_PRESETS = (
    (1920, 937, 1920, 1040, 1920, 1040, 1920, 1080),
    (1366, 637, 1366, 728, 1366, 728, 1366, 768),
    (1536, 737, 1536, 824, 1536, 824, 1536, 864),
    (1440, 773, 1440, 860, 1440, 860, 1440, 900),
    (1280, 593, 1280, 680, 1280, 680, 1280, 720),
)

# 进程级指纹档案（UA/几何/硬件统一，进程内稳定）
_PROFILE: Optional[dict] = None


def _get_profile() -> dict:
    """进程级指纹档案（开源 get_profile 同构，纯静态预设）。"""
    global _PROFILE
    if _PROFILE is None:
        geo = random.choice(_GEO_PRESETS)
        _PROFILE = {
            "ua": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            ),
            "cpu_core_num": "12",
            "device_memory": "8",
            "geo": geo,
        }
    return _PROFILE


# ----------------------------------------------------------------------
# 纯算法（RC4 + 自定义 b64），可单测，不发网络
# ----------------------------------------------------------------------
def rc4(key: bytes, data: bytes) -> bytes:
    """RC4 流密码（开源同构）。"""
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) & 255
        s[i], s[j] = s[j], s[i]
    out = bytearray()
    i = j = 0
    for b in data:
        i = (i + 1) & 255
        j = (j + s[i]) & 255
        s[i], s[j] = s[j], s[i]
        out.append(b ^ s[(s[i] + s[j]) & 255])
    return bytes(out)


def b64_custom_encode(data: bytes) -> str:
    """自定义 base64（字符表 _CUSTOM_B64，开源同构）。"""
    out = []
    n = len(data)
    for idx in range(0, n, 3):
        chunk = data[idx : idx + 3]
        b0 = chunk[0]
        b1 = chunk[1] if len(chunk) > 1 else 0
        b2 = chunk[2] if len(chunk) > 2 else 0
        trip = (b0 << 16) | (b1 << 8) | b2
        out.append(_CUSTOM_B64[(trip >> 18) & 63])
        out.append(_CUSTOM_B64[(trip >> 12) & 63])
        out.append(_CUSTOM_B64[(trip >> 6) & 63] if len(chunk) > 1 else "=")
        out.append(_CUSTOM_B64[trip & 63] if len(chunk) > 2 else "=")
    return "".join(out)


def encode_strdata(plaintext_bytes: bytes, nonce: int) -> str:
    """明文 → RC4(nonce) 加密 → 自定义 b64（带 0x41+nonce 前缀）。"""
    cipher = rc4(bytes([nonce]), plaintext_bytes)
    raw = bytes([0x41, nonce]) + cipher
    return b64_custom_encode(raw)


def build_fingerprint() -> str:
    """用静态模板 + 进程级档案构造指纹 JSON 字符串。"""
    prof = _get_profile()
    g = prof["geo"]
    fp = json.loads(_FINGERPRINT_TEMPLATE)
    fp["navigator"]["hardwareConcurrency"] = int(prof["cpu_core_num"])
    fp["navigator"]["deviceMemory"] = prof["device_memory"]
    fp["screen"].update(
        {
            "innerWidth": g[0],
            "innerHeight": g[1],
            "outerWidth": g[2],
            "outerHeight": g[3],
            "availWidth": g[4],
            "availHeight": g[5],
            "sizeWidth": g[6],
            "sizeHeight": g[7],
            "clientWidth": g[0] - 10,
            "clientHeight": g[1],
        }
    )
    fp["wID"]["timestamp"] = str(int(time.time() * 1000))
    return json.dumps(fp, ensure_ascii=False, separators=(",", ":"))


def build_report_body() -> str:
    """构造 mssdk 上报体（开源 build_report_body 同构）。"""
    plaintext = build_fingerprint()
    nonce = random.randint(0, 255)
    str_data = encode_strdata(plaintext.encode("utf-8"), nonce)
    envelope = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": str_data,
        "tspFromClient": int(time.time() * 1000),
        "ulr": 0,
    }
    return json.dumps(envelope, ensure_ascii=False, separators=(",", ":"))


# ----------------------------------------------------------------------
# 缓存 + 换发
# ----------------------------------------------------------------------
class _MstokenCache:
    """进程内 600s 惰性缓存（开源 _cache 同构，线程安全由调用方保证）。"""

    __slots__ = ("_token", "_ts", "_ttl")

    def __init__(self, ttl: int = _TTL):
        self._token = ""
        self._ts = 0.0
        self._ttl = ttl

    def get(self) -> str:
        if self._token and (time.time() - self._ts < self._ttl):
            return self._token
        return ""

    def put(self, token: str) -> None:
        self._token = token
        self._ts = time.time()


_DEFAULT_CACHE = _MstokenCache()


def get_mstoken(
    cookie_str: str = "",
    *,
    use_cache: bool = True,
    timeout: float = 25.0,
    cache: Optional[_MstokenCache] = None,
) -> str:
    """向 mssdk 上报换发一个真实 msToken（无 a_bogus、无浏览器）。

    Args:
        cookie_str: 可选抖音 cookie（用于提取 ``ttwid``；服务端也可在无 cookie 时下发 token）。
        use_cache: 是否启用 600s 惰性缓存。
        timeout: 请求超时（秒）。
        cache: 测试可注入的缓存实例。

    Returns:
        非空 msToken 字符串；换发失败返回空串（调用方应降级）。
    """
    cache = cache or _DEFAULT_CACHE
    if use_cache:
        cached = cache.get()
        if cached:
            return cached

    envelope = build_report_body()
    ttwid = ""
    m = re.search(r"ttwid=([^;]+)", cookie_str or "")
    if m:
        ttwid = m.group(1)
    headers = {
        "user-agent": _get_profile()["ua"],
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://www.douyin.com",
        "referer": "https://www.douyin.com/",
        "cookie": f"ttwid={ttwid}" if ttwid else "",
    }
    try:
        resp = httpx.post(
            _REPORT_URL,
            content=envelope.encode("utf-8"),
            headers=headers,
            timeout=timeout,
        )
        token = resp.headers.get("x-ms-token", "")
        if not token:
            m2 = re.search(r"msToken=([^;]+)", resp.headers.get("set-cookie", ""))
            token = m2.group(1) if m2 else ""
        if token:
            cache.put(token)
            logger.info("[mstoken] 换发成功（缓存 %ds）", _TTL)
        else:
            logger.warning("[mstoken] 响应未携带 x-ms-token（status=%s）", resp.status_code)
        return token
    except Exception as exc:  # noqa: BLE001 - 换发失败不应阻断采集主链路
        logger.warning("[mstoken] 换发失败: %s", exc)
        return ""
