#!/usr/bin/env python3
"""个人数据权限、脱敏与安全诊断的公共实现。"""
import json
import os
import re


def ensure_private_dir(path):
    os.makedirs(path, mode=0o700, exist_ok=True)
    if os.path.islink(path):
        raise ValueError(f"个人数据目录不能是符号链接: {path}")
    os.chmod(path, 0o700)


def atomic_write_text(path, text):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, mode=0o700, exist_ok=True)
    tmp = f"{path}.tmp.{os.getpid()}"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
        os.chmod(path, 0o600)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def atomic_write_json(path, obj, *, indent=None):
    atomic_write_text(path, json.dumps(obj, ensure_ascii=False, indent=indent))


def secure_tree(root):
    if not os.path.exists(root):
        return
    if os.path.islink(root):
        raise ValueError(f"个人数据目录不能是符号链接: {root}")
    os.chmod(root, 0o700)
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs:
            path = os.path.join(base, name)
            if not os.path.islink(path):
                os.chmod(path, 0o700)
        for name in files:
            path = os.path.join(base, name)
            if not os.path.islink(path):
                os.chmod(path, 0o600)


def schema_outline(obj, depth=0):
    if depth >= 8:
        return "<...>"
    if isinstance(obj, dict):
        return {str(k): schema_outline(v, depth + 1)
                for k, v in list(obj.items())[:40]}
    if isinstance(obj, list):
        return [schema_outline(obj[0], depth + 1)] if obj else []
    return f"<{type(obj).__name__}>"


def redact_sensitive(text):
    value = str(text or "")
    value = re.sub(r"-----BEGIN [^-]+-----.*?-----END [^-]+-----",
                   "<PRIVATE_KEY>", value, flags=re.S)
    value = re.sub(r"https?://[^\s<>\"')\]]+", "<URL>", value, flags=re.I)
    value = re.sub(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", "Bearer <REDACTED>",
                   value, flags=re.I)
    value = re.sub(
        r"(?i)\b(access[_-]?token|refresh[_-]?token|api[_-]?key|app[_-]?secret|"
        r"secret|password|passwd|pwd|cookie|authorization|session[_-]?key)\b"
        r"(\s*[:=]\s*)(\"[^\"]*\"|'[^']*'|[^\s,;，。；]+)",
        r"\1\2<REDACTED>", value)
    value = re.sub(r"(密码|口令|密钥|令牌)(\s*[:：=]?\s*)([^\s，。；]+)",
                   r"\1\2<REDACTED>", value)
    value = re.sub(r"ssh-(?:rsa|ed25519)\s+[A-Za-z0-9+/=]+", "<SSH_KEY>", value)
    value = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
                   "<EMAIL>", value)
    value = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "<IP>", value)
    value = re.sub(r"(?<!\d)1[3-9]\d{9}(?!\d)", "<PHONE>", value)
    value = re.sub(r"\b(?:ou|oc|om)_[A-Za-z0-9_-]{6,}\b|\baib[A-Za-z0-9_-]{6,}",
                   "<ID>", value)
    value = re.sub(r"(?<![A-Za-z0-9])[A-Za-z0-9_-]{32,}(?![A-Za-z0-9])",
                   "<TOKEN>", value)
    return value


def usable_style_text(text):
    value = str(text or "").strip()
    if len(value) < 2:
        return False
    markers = ("<file ", "<card ", "<folder ", "<audio ", "<video ",
               "<forwarded_messages>", "[Invalid", "[Sticker]")
    return not any(marker in value for marker in markers)
