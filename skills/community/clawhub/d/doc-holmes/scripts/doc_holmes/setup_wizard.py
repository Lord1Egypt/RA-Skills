#!/usr/bin/env python3
"""v3.0.0 setup：一键配置端点 + 连通校验 + 引擎指引。

宪章边界：绝不代装任何包（运行时装包是分发审核红线）——引擎缺失时打印
精确安装命令由用户自行执行；本模块只写配置文件（0600）与做一次用户
自己端点的连通校验（凭据由用户显式提供，与 selfcheck --net 同类边界）。
"""

from __future__ import annotations

import json
import os
import stat
import urllib.request

from .endpoints import (DEFAULT_MODEL, ENV_FILE, EndpointError,
                        assert_distribution_safe, load_endpoint_config)


def write_env_file(env_file: str, updates: dict) -> dict:
    """合并写入配置（保留既有未覆盖键，如 ALLOW 标志），文件权限 0600。"""
    from .endpoints import _parse_env_file
    existing = _parse_env_file(env_file)
    existing.update({k: str(v) for k, v in updates.items() if v is not None})
    os.makedirs(os.path.dirname(os.path.realpath(env_file)) or ".", exist_ok=True)
    body = "".join("%s=%s\n" % (k, existing[k]) for k in sorted(existing))
    fd = os.open(env_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(body)
    try:
        os.chmod(env_file, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    return existing


def ping_endpoint(base_url: str, api_key: str, model: str, timeout: int = 30) -> dict:
    """1-token 连通校验（用户自己的端点与凭据；显式发起，非遥测）。"""
    body = json.dumps({"model": model, "messages": [
        {"role": "user", "content": "ping"}], "max_tokens": 1}).encode("utf-8")
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions", data=body, method="POST",
        headers={"Authorization": "Bearer " + api_key,
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return {"ok": True, "detail": "HTTP 200"}
            return {"ok": False, "detail": "HTTP %s" % resp.status}
    except Exception as exc:
        return {"ok": False, "detail": str(exc)[:160]}


def validate_and_write(base_url: str, api_key: str, model: str = None,
                       env_file: str = ENV_FILE, skip_ping: bool = False,
                       timeout: int = 30, allow_coding: bool = None) -> dict:
    """校验 → 写配置。返回 {written, env_file, ping, model}；失败抛 EndpointError/OSError。"""
    if not base_url or not api_key:
        raise EndpointError("--base-url 与 --api-key 必须同时提供")
    if allow_coding is None:
        allow_coding = os.environ.get("DOC_HOLMES_ALLOW_CODING_ENDPOINT") == "1"
    assert_distribution_safe(base_url, allow_coding=allow_coding)
    model = model or DEFAULT_MODEL
    ping = {"ok": True, "detail": "skipped(--skip-ping)"}
    if not skip_ping:
        ping = ping_endpoint(base_url, api_key, model, timeout=timeout)
        if not ping.get("ok"):
            raise EndpointError(
                "端点连通校验失败（%s）。请核对 base-url/api-key/model；"
                "确信端点可用但拒绝探测（如内网白名单），加 --skip-ping 跳过校验强制写入。"
                % ping.get("detail"))
    write_env_file(env_file, {
        "DOC_HOLMES_OPENAI_BASE_URL": base_url.rstrip("/"),
        "DOC_HOLMES_OPENAI_API_KEY": api_key,
        "DOC_HOLMES_MODEL": model,
    })
    return {"written": True, "env_file": env_file, "ping": ping, "model": model}


def status_report(env_file: str = ENV_FILE) -> dict:
    """无参 setup：现状体检（配置/引擎/OCR）+ 逐步指引，信息性输出。"""
    from .engine_babeldoc import EngineNotFoundError, find_engine_bin
    from .ocr_adapter import tesseract_info
    rep = {"env_file": env_file}
    try:
        cfg = load_endpoint_config(env_file=env_file)
        rep["endpoint"] = "%s @ %s" % (cfg.model, cfg.base_url)
    except EndpointError as exc:
        rep["endpoint"] = None
        rep["endpoint_hint"] = str(exc).splitlines()[0]
    try:
        rep["engine"] = find_engine_bin()
    except EngineNotFoundError:
        rep["engine"] = None
        rep["engine_hint"] = ("uv tool install --python 3.12 pdf2zh-next"
                              "（或 pip install pdf2zh-next；本工具绝不代装）")
    tess = tesseract_info()
    rep["ocr"] = bool(tess.get("available"))
    rep["ocr_hint"] = None if rep["ocr"] else "apt install tesseract-ocr（C 级扫描件可选）"
    return rep
