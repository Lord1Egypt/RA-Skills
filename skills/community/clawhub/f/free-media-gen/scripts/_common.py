#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""free-media-gen 各脚本的共用工具。

职责：解析 WorkBuddy 路径（经 references/resolve_paths.py）、读取 models.json 与本技能
config.json、并为媒体模型解析 API 密钥。**不写死任何绝对路径**：一切路径均由
resolve_paths 或标准库推导得出。

密钥解析规则（兼顾跨用户可移植）：
  - api_key_ref 形如 "models.json:<id>" 时，先按该 id 精确查找对应的对话模型条目。
  - 找不到时（例如其他用户的 models.json 里条目 id 不同），回退为按**平台主机名**
    匹配：凡 models.json 中 url 主机相同的条目，取其 apiKey。
  这样即使用户的对话模型 id 与作者不同，只要配置过同一平台的密钥，本技能仍可正常工作。
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
REF_DIR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REF_DIR, "references"))

import resolve_paths  # noqa: E402

PROVIDER_HOSTS = {
    "agnes": "api.agnes-ai.cn",
    "sensenova": "token.sensenova.cn",
    "siliconflow": "api.siliconflow.cn",
}

_RESOLVE_CACHE = None


def resolve():
    """返回路径解析结果（带缓存）。"""
    global _RESOLVE_CACHE
    if _RESOLVE_CACHE is None:
        _RESOLVE_CACHE = resolve_paths.collect()
    return _RESOLVE_CACHE


def load_models_json():
    r = resolve()
    p = r["models_json"]
    if not os.path.isfile(p):
        raise FileNotFoundError("未找到 models.json：%s" % p)
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def load_config():
    r = resolve()
    p = r["config_json"]
    if not os.path.isfile(p):
        raise FileNotFoundError("未找到技能配置 config.json：%s" % p)
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def load_media_models():
    return load_config().get("media_models", [])


def get_model_entry(model_id):
    for m in load_media_models():
        if m.get("id") == model_id:
            return m
    return None


def resolve_api_key(ref, provider=None):
    """按 config 中的 api_key_ref 或平台名解析 API 密钥。"""
    models = load_models_json().get("models", []) if isinstance(load_models_json(), dict) else load_models_json()
    # 统一成列表
    if isinstance(models, dict):
        models = models.get("models", [])
    # 1) 先按 ref 精确匹配
    if ref and ref.startswith("models.json:"):
        target_id = ref.split(":", 1)[1]
        for e in models:
            if e.get("id") == target_id:
                return e.get("apiKey")
    # 2) 找不到则按平台主机名回退匹配
    host = PROVIDER_HOSTS.get(provider)
    if host:
        for e in models:
            url = e.get("url", "")
            if host in url:
                return e.get("apiKey")
    # 3) ref 本身就是平台名的情况
    if ref in PROVIDER_HOSTS:
        host = PROVIDER_HOSTS[ref]
        for e in models:
            if host in e.get("url", ""):
                return e.get("apiKey")
    raise KeyError("无法解析 API 密钥：ref=%s，平台=%s" % (ref, provider))


def http_json(url, payload=None, headers=None, method="POST", retries=3, timeout=120):
    """发起 POST/GET 的 JSON 请求，返回 (状态码, 解析后的 JSON 或原始文本)。"""
    headers = headers or {}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers.setdefault("Content-Type", "application/json")
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", "replace")
                status = resp.getcode()
            try:
                return status, json.loads(body)
            except Exception:
                return status, body
        except urllib.error.HTTPError as e:
            last_err = e
            body = e.read().decode("utf-8", "replace") if e.fp else ""
            if e.code >= 400 and e.code < 500:
                return e.code, body  # 永久性错误（4xx），不重试
            time.sleep(2 ** attempt)
        except Exception as e:  # 瞬时错误（超时 / 连接重置）
            last_err = e
            time.sleep(2 ** attempt)
    return getattr(last_err, "code", 0), str(last_err)


def download(url, path, retries=3, timeout=120):
    """把二进制 URL 下载到指定路径，成功返回 True，失败返回 False。"""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "free-media-gen/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp, open(path, "wb") as out:
                out.write(resp.read())
            return True
        except Exception as e:
            last_err = e
            time.sleep(2 ** attempt)
    sys.stderr.write("下载失败：%s -> %s\n" % (url, last_err))
    return False


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)
    return p


def out_name(prefix, ext, seed=None):
    import random
    s = seed if seed is not None else random.randint(100000, 999999)
    return "%s_%s_%d.%s" % (prefix, s, int(time.time()), ext)
