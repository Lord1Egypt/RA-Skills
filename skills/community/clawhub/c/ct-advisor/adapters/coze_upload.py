# -*- coding: utf-8 -*-
"""
ct-advisor — Coze 文档上传出站适配层（§16.9）

原 scripts/doc_memory.py 中通过 urllib 直接调用 Coze /upload_file 上传端点的
**所有出站逻辑**，已按 §16.9 迁移到此统一适配器目录，使 scripts/doc_memory.py
不再含任何 urllib 出站调用（仅保留本地缓存 / 准入逻辑）。

§16.9 要求：对外 API / 检索 / 远程 LLM 调用"一律移入本技能统一的专用目录（推荐
adapters/）"。文件上传到 Coze 云端端点属于典型对外 API 调用，故下沉到此适配层。
"""
from __future__ import annotations

import io
import json
import urllib.error
import urllib.request


class UploadFailedError(ValueError):
    """上传到 Coze 终端失败（网络 / 鉴权 / 端点不可用）。消息可直转用户。"""


def _make_token_header(get_token):
    """构造 Bearer 鉴权头（沿用内嵌共享令牌，与 /run 同源）。"""
    try:
        tok = get_token() if callable(get_token) else None
        if tok:
            return {"Authorization": "Bearer %s" % tok}
    except Exception:               # noqa: BLE001
        pass
    return {}


def probe_upload_available(endpoint: str, upload_path: str,
                          probe_timeout: float, get_token) -> bool:
    """探测服务端是否支持 /upload_file（file_id 通道）。

    判据（与人工 curl 实测一致）：
      - 405 = FastAPI 路由存在但只接受 POST -> 可用；
      - 200 / 401 / 403 -> 路由存在（可能带网关鉴权）-> 可用；
      - 404 -> 老服务端没有该路由 -> 不可用；
      - 5xx / 网络异常 -> 视为不可用（安全方向：回退老通道，绝不阻断）。

    策略：先走系统代理；网络层失败（死代理 / 半死代理 / 超时）-> 绕过代理直连重试
    一次；仍失败才判不可用。
    """
    def _mk_probe_req():
        r = urllib.request.Request(endpoint + upload_path, method="GET")
        for k, v in _make_token_header(get_token).items():
            r.add_header(k, v)
        return r

    def _probe_once(open_fn):
        try:
            with open_fn(_mk_probe_req(), timeout=probe_timeout) as resp:
                return int(getattr(resp, "status", 0) or 0)
        except urllib.error.HTTPError as e:     # 4xx/5xx 也说明**路由存在**
            return int(getattr(e, "code", 0) or 0)
        except Exception:                # noqa: BLE001  网络/超时/死代理 -> 0
            return 0

    code = _probe_once(urllib.request.urlopen)
    if code == 0:
        _direct = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        code = _probe_once(_direct.open)
    return code in (200, 401, 403, 405, 422)


def upload_to_coze(content: bytes, name: str, url: str, get_token) -> tuple:
    """把字节上传到统一端点 /upload_file，返回 (file_id, file_url)。

    失败一律抛 UploadFailedError（**绝不静默吞**）——由调用方转达用户。

    策略：先走系统代理；网络层失败（死代理 / 半死代理 / 超时）-> 绕过代理直连重试
    一次；仍失败才抛错。
    """
    boundary = "----ctadvisoruploadboundary"
    crlf = b"\r\n"
    body = io.BytesIO()
    filename = name or "upload.bin"
    body.write(b"--" + boundary.encode() + crlf)
    body.write(
        ('Content-Disposition: form-data; name="file"; filename="%s"'
         % filename).encode("utf-8") + crlf)
    body.write(b"Content-Type: application/octet-stream" + crlf + crlf)
    body.write(content)
    body.write(crlf + b"--" + boundary.encode() + b"--" + crlf)
    data = body.getvalue()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "multipart/form-data; boundary=%s" % boundary)
    for k, v in _make_token_header(get_token).items():
        req.add_header(k, v)
    # ⚠️ urllib 陷阱（2026-09-25 实测）：Request 对象一旦经历过代理路由的失败尝试，
    # 内部会残留代理状态——复用同一 req 绕过代理重试仍会打到死代理。
    # 因此把 headers 暂存，每次尝试用**全新 Request** 对象。
    _hdrs = dict(req.headers)
    _hdrs.update(getattr(req, "unredirected_hdrs", {}))

    def _mk_req():
        r = urllib.request.Request(url, data=data, method="POST")
        for k, v in _hdrs.items():
            r.add_header(k, v)
        return r

    def _post_once(open_fn):
        with open_fn(_mk_req(), timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))

    # 与 refiner._call_coze / 上传探测同策略（2026-09-25）：先走系统代理；
    # 网络层失败（死代理/半死代理/超时）-> 绕过代理直连重试一次；仍失败才抛错。
    try:
        payload = _post_once(urllib.request.urlopen)
    except urllib.error.HTTPError:
        raise  # 服务端明确回了 HTTP 错误码 -> 代理链路是通的，重试无意义
    except Exception:                   # noqa: BLE001
        _direct = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        payload = _post_once(_direct.open)
    fid = (payload.get("file_id") or "").strip()
    # 契约：v1.26 服务端回 ``file_url``；老/变体实现可能回 ``url``。两者都认，
    # 取不到也不致命——信封里 file_id 才是解析依据，file_url 仅作诊断/回溯用。
    fur = (payload.get("file_url") or payload.get("url") or "").strip()
    if not fid:
        raise UploadFailedError("上传端点未返回 file_id（响应：%s）" % str(payload)[:200])
    return fid, fur
