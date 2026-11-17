#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""百度网盘官方扫码登录桥（对齐 2026-10-15 已验证成功版本）。

流程：官方 passport getqrcode(JSONP) -> 百度App扫码 -> channel/unicast 取 channel_v
      -> qrbdusslogin(JSONP) 取 session.bduss/ptoken/stokenList -> 写入 BaiduPCS-Go。

安全边界：
- 只调用 passport.baidu.com 官方扫码接口；不读浏览器 Cookie、不绕过验证码/风控。
- BDUSS / PTOKEN / STOKEN 只在内存与 BaiduPCS-Go 本机配置间流转，不打印、不落日志、不进聊天。

用法：
    python3 scripts/pancli/baidu_login.py --engine /path/to/BaiduPCS-Go
    python3 scripts/pancli/baidu_login.py --engine /path/to/BaiduPCS-Go --json
"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import argparse
import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36")
# 安全修复：二维码含登录能力，改用系统临时目录 + 0600 权限，且跨平台（Windows 无 /tmp）
QR_DEFAULT = str(Path(tempfile.gettempdir()) / "pan-baidu-login-qr.png")


def _secure_qr_file(path: str) -> str:
    """确保二维码文件权限 0600（POSIX）；Windows 忽略权限位。"""
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def unique_qr_path(base=QR_DEFAULT):
    """每次登录用唯一文件名；同名文件会被展示端/浏览器按路径缓存，导致扫到旧码报"二维码错误"。"""
    root, dot, ext = base.rpartition(".")
    stamp = time.strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(3)
    if not dot:
        return "%s-%s" % (base, stamp)
    return "%s-%s.%s" % (root, stamp, ext)


class QRLoginError(RuntimeError):
    pass


def _req_jsonp(url, callback, timeout=35):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Referer": "https://pan.baidu.com/",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read().decode("utf-8", "replace")
    start = data.find(callback + "(")
    if start < 0:
        raise QRLoginError("回调数据格式异常")
    start += len(callback) + 1
    end = data.rfind(")")
    if end <= start:
        raise QRLoginError("回调数据结束位置异常")
    body = data[start:end].strip()
    try:
        return json.loads(body)
    except ValueError:
        return json.loads(body.replace("'", '"').replace("\\", ""))


def _gid():
    return (secrets.token_hex(4).upper() + "-" + secrets.token_hex(2).upper()
            + "-4" + secrets.token_hex(2)[:3].upper()
            + "-8" + secrets.token_hex(2)[:3].upper()
            + "-" + secrets.token_hex(6).upper())


def get_qrcode(qr_out):
    """取官方登录二维码：返回 (gid, sign)；图片写入 qr_out。"""
    now = int(time.time() * 1000)
    gid = _gid()
    cb = "tangram_guid_%d" % now
    q = urllib.parse.urlencode({
        "lp": "pc", "qrloginfrom": "pc", "gid": gid, "callback": cb,
        "apiver": "v3", "tt": now + 21232, "tpl": "netdisk", "_": now + 4,
    })
    data = _req_jsonp("https://passport.baidu.com/v2/api/getqrcode?" + q, cb)
    if int(data.get("errno", -1)) != 0:
        raise QRLoginError("获取二维码失败 errno=%s" % data.get("errno"))
    imgurl = str(data.get("imgurl") or "")
    if imgurl.startswith("//"):
        imgurl = "https:" + imgurl
    elif not imgurl.startswith("http"):
        imgurl = "https://" + imgurl.lstrip("/")
    ireq = urllib.request.Request(imgurl, headers={
        "User-Agent": UA, "Referer": "https://pan.baidu.com/", "Accept": "image/*"})
    with urllib.request.urlopen(ireq, timeout=25) as r:
        img = r.read()
    if len(img) < 100:
        raise QRLoginError("二维码图片为空")
    with open(qr_out, "wb") as fh:
        fh.write(img)
    _secure_qr_file(qr_out)
    return gid, str(data.get("sign") or "")


def poll_confirm(gid, sign, timeout_s=180):
    """长轮询 channel/unicast，扫到并确认后返回 channel_v 里的 v。"""
    end = time.time() + timeout_s
    while time.time() < end:
        now = int(time.time() * 1000)
        cb = "tangram_guid_%d" % now
        q = urllib.parse.urlencode({
            "channel_id": sign, "tpl": "netdisk", "gid": gid,
            "callback": cb, "apiver": "v3", "tt": now + 5, "_": now + 10})
        try:
            data = _req_jsonp("https://passport.baidu.com/channel/unicast?" + q, cb, timeout=40)
            cv = data.get("channel_v") or ""
            if isinstance(cv, str) and cv:
                try:
                    cvobj = json.loads(cv)
                except ValueError:
                    cvobj = {}
                v = cvobj.get("v") if isinstance(cvobj, dict) else ""
                if v:
                    return v
        except Exception:
            pass
        time.sleep(1.5)
    return None


def _extract_stoken(stoken_list, fallback=""):
    if isinstance(stoken_list, list):
        for item in stoken_list:
            s = str(item)
            if s.startswith("netdisk#") and "#" in s:
                return s.split("#", 1)[1].strip('"')
    text = str(stoken_list or "").replace("&quot;", '"')
    for item in text.split(","):
        item = item.strip()
        if item.startswith('"netdisk#') or item.startswith("netdisk#"):
            parts = item.strip('"').split("#")
            if len(parts) >= 2:
                return parts[1].strip('"')
    return fallback or ""


def fetch_credentials(channel_v):
    """用 channel_v(即 v) 换 BDUSS/PTOKEN/STOKEN。"""
    now = int(time.time() * 1000)
    cb = "bd__cbs__ay6xvs"
    q = urllib.parse.urlencode({
        "v": now, "bduss": channel_v, "loginVersion": "v4", "qrcode": "1",
        "tpl": "netdisk", "apiver": "v3", "tt": now, "traceid": "",
        "time": now + 225, "alg": "v3", "callback": cb,
        "u": "https://pan.baidu.com/disk/home"})
    data = _req_jsonp("https://passport.baidu.com/v3/login/main/qrbdusslogin?" + q, cb)
    err = str((data.get("errInfo") or {}).get("no", "0"))
    if err not in ("0", "None", ""):
        raise QRLoginError(data.get("message") or (data.get("errInfo") or {}).get("msg") or "扫码登录失败")
    d = data.get("data") or {}
    sess = d.get("session") or {}
    bduss = str(sess.get("bduss") or "")
    ptoken = str(sess.get("ptoken") or "")
    stoken = _extract_stoken(sess.get("stokenList"), sess.get("stoken") or "")
    user = d.get("user") or {}
    uid = _parse_uid(user.get("userId"), user.get("uid"), sess.get("ubi"), d.get("u"))
    name = str(user.get("displayName") or user.get("username") or "").strip()
    if not bduss:
        raise QRLoginError("扫码结果缺少 BDUSS")
    return bduss, ptoken, stoken, uid, name


def _parse_uid(*vals):
    for v in vals:
        if v is None:
            continue
        m = re.search(r"(\d{4,})", str(v))
        if m:
            n = int(m.group(1))
            if n > 0:
                return n
    return 0


def config_dir_for(engine):
    """BaiduPCS-Go 配置目录：显式环境变量优先，否则取可执行文件同目录。"""
    env = (os.environ.get("BAIDUPCS_GO_CONFIG_DIR") or "").strip()
    if env:
        return env
    return os.path.dirname(os.path.abspath(engine))


def write_login_config(engine, bduss, ptoken, stoken, uid, name):
    """直接写 BaiduPCS-Go 的 pcs_config.json（对齐已验证成功版本）。

    不依赖 `BaiduPCS-Go login` 子进程；文件 0600，原子替换。
    """
    cfg_dir = config_dir_for(engine)
    os.makedirs(cfg_dir, mode=0o700, exist_ok=True)
    cfg_path = os.path.join(cfg_dir, "pcs_config.json")
    try:
        with open(cfg_path, encoding="utf-8") as fh:
            cfg = json.load(fh)
        if not isinstance(cfg, dict):
            cfg = {}
    except Exception:
        cfg = {}
    cfg["baidu_active_uid"] = uid
    cfg["baidu_user_list"] = [{
        "uid": uid, "name": name or str(uid), "sex": "default", "age": 0.0,
        "bduss": bduss, "ptoken": ptoken, "stoken": stoken,
        "baiduid": "", "sboxtkn": "",
        "cookies": "BDUSS=%s;PTOKEN=%s;STOKEN=%s;" % (bduss, ptoken, stoken),
        "accesstoken": "", "workdir": "/",
    }]
    tmp = cfg_path + ".tmp." + secrets.token_hex(4)
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False, indent=2)
    os.chmod(tmp, 0o600)
    os.replace(tmp, cfg_path)
    return cfg_path


def who_uid(engine):
    try:
        proc = subprocess.run([engine, "who"], capture_output=True, text=True, timeout=15)
        m = re.search(r"uid:\s*([1-9][0-9]*)", proc.stdout or "")
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


def run(engine, qr_out=None, timeout_s=180, emit_json=False):
    qr_out = unique_qr_path(qr_out or QR_DEFAULT)
    result = {"ok": False, "engine": engine, "qr_path": qr_out, "stage": "start", "uid": 0}
    try:
        gid, sign = get_qrcode(qr_out)
    except Exception as exc:
        result["error"] = "qrcode_failed: %s" % exc
        return result
    result["stage"] = "await_scan"
    if not emit_json:
        print("QR_READY %s" % qr_out, flush=True)
    channel_v = poll_confirm(gid, sign, timeout_s)
    if not channel_v:
        result["error"] = "scan_timeout_or_cancelled"
        result["stage"] = "timeout"
        return result
    result["stage"] = "confirmed"
    try:
        bduss, ptoken, stoken, uid, name = fetch_credentials(channel_v)
    except Exception as exc:
        result["error"] = "bduss_failed: %s" % exc
        result["stage"] = "bduss"
        return result
    result["stage"] = "logged_in"
    try:
        result["config_path"] = write_login_config(engine, bduss, ptoken, stoken, uid, name)
    except Exception as exc:
        result["error"] = "config_write_failed: %s" % exc
        result["stage"] = "config"
        return result
    result["uid"] = uid or who_uid(engine)
    result["ok"] = bool(bduss and stoken and result["uid"])
    if not result["ok"]:
        result["error"] = "incomplete_login_state"
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description="百度网盘官方扫码登录 -> BaiduPCS-Go")
    ap.add_argument("--engine", required=True, help="BaiduPCS-Go 可执行文件路径")
    ap.add_argument("--qr-out", default="", help="二维码 png 输出路径（默认自动加时间戳，避免缓存旧码）")
    ap.add_argument("--timeout", type=int, default=180, help="等待扫码秒数")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出结果（不打印中间提示）")
    a = ap.parse_args(argv)
    res = run(a.engine, a.qr_out or None, a.timeout, emit_json=a.json)
    if a.json:
        print(json.dumps(res, ensure_ascii=False))
    elif res.get("ok"):
        print("LOGIN_OK uid=%s" % res.get("uid"))
    else:
        print("LOGIN_FAIL %s" % res.get("error", ""))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
