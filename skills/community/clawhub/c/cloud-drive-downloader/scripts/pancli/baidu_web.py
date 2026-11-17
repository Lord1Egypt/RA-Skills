#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""百度网盘零客户端网页驱动。

只使用百度网盘官方分享页和官方网页接口，使用进程内 CookieJar 保存匿名网页会话。
不读取浏览器 Cookie，不持久化会话，不输出 Cookie、BDUSS、STOKEN、sekey、sign、timestamp。
遇到验证码、风控、会员或付费限制时安全失败。
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


import http.cookiejar
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

from pancli.webengine import RemoteItem, WebEngineError, WebProbe, download_http_url, safe_rel_path


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)
SHARE_HOST = "https://pan.baidu.com"
COMMON_QUERY = {
    "channel": "chunlei",
    "web": "1",
    "app_id": "250528",
    "clienttype": "0",
}


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _first(mapping: Dict[str, Any], *keys: str, default: str = "") -> str:
    for key in keys:
        value = mapping.get(key)
        if value not in (None, ""):
            return _text(value)
    return default


def _extract_balanced(text: str, start: int, opener: str = "{", closer: str = "}") -> str:
    if start < 0 or start >= len(text) or text[start] != opener:
        return ""
    depth = 0
    quote = ""
    escape = False
    for pos in range(start, len(text)):
        ch = text[pos]
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = ""
            continue
        if ch in ("'", '"'):
            quote = ch
            continue
        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return text[start:pos + 1]
    return ""


def _json_from_javascript_object(text: str) -> Dict[str, Any]:
    """解析页面里近似 JSON 的 window.yunData 对象。"""
    # 优先按 JSON 解析；失败后只提取已知标量字段，避免 eval。
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else {}
    except (TypeError, ValueError):
        pass
    out: Dict[str, Any] = {}
    for key in (
        "shareid", "share_uk", "uk", "loginstate", "sekey", "currentSekey",
        "surl", "shorturl", "bdstoken", "jsToken", "title", "is_vip", "is_svip",
    ):
        pat = re.compile(r"""["']?%s["']?\s*:\s*(?:"([^"]*)"|'([^']*)'|([^,}\s]+))""" % re.escape(key))
        match = pat.search(text)
        if not match:
            continue
        value = next((x for x in match.groups() if x is not None), "")
        if value.lower() in ("true", "false"):
            out[key] = value.lower() == "true"
        else:
            try:
                out[key] = int(value)
            except ValueError:
                out[key] = value
    return out


def _merge_meta(base: Dict[str, Any], extra: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in extra.items():
        if value not in (None, ""):
            base[key] = value
    return base


def _strip_share_prefix(value: str) -> str:
    """去掉 Baidu 分享短链最前面的单个 ``1``，不误删其他数字。"""
    text = _text(value)
    return text[1:] if text.startswith("1") and len(text) > 1 else text


def extract_share_surl(url: str) -> str:
    text = _text(url)
    parsed = urllib.parse.urlparse(text)
    query = urllib.parse.parse_qs(parsed.query)
    for key in ("surl", "shorturl"):
        values = query.get(key) or []
        if values and values[0].strip():
            return _strip_share_prefix(values[0])
    match = re.search(r"/(?:s|share/init)/([A-Za-z0-9_-]+)", parsed.path + ("?" + parsed.query if parsed.query else ""))
    if match:
        return _strip_share_prefix(match.group(1))
    match = re.search(r"/s/([A-Za-z0-9_-]+)", text)
    if match:
        return _strip_share_prefix(match.group(1))
    raise WebEngineError("invalid_url", "无法识别百度网盘分享链接")


def _share_slug(url: str) -> str:
    """返回分享链接中的完整短链标识（通常以 1 开头）。"""
    parsed = urllib.parse.urlparse(_text(url))
    query = urllib.parse.parse_qs(parsed.query)
    for key in ("surl", "shorturl"):
        values = query.get(key) or []
        if values and values[0].strip():
            return values[0].strip()
    match = re.search(r"/s/([A-Za-z0-9_-]+)", parsed.path)
    return match.group(1) if match else ""


def _api_error(errno: int, msg: str, *, action: str = "操作") -> WebEngineError:
    text = _text(msg)
    low = text.lower()
    if errno in (-20, -21) or "验证码" in text or "vcode" in low:
        return WebEngineError("captcha_required", "百度要求验证码，网页官方接口未提供可用验证码；工具不会绕过验证码。", detail=text)
    if errno == 118 or "违规操作" in text:
        return WebEngineError("platform_denied", "百度官方接口返回“违规操作，无法下载”；已按平台限制安全停止。", detail=text)
    if errno in (-6, -64) or "登录" in text:
        return WebEngineError("auth_required", "百度要求登录或当前会话受登录限制；请直接在官方网页登录后重试，不需要向工具粘贴 Cookie。", detail=text)
    if errno in (-9, -12) or "提取码" in text or "密码" in text:
        return WebEngineError("password_invalid", "百度分享提取码错误或提取会话无效。", detail=text)
    if errno in (112, 113) or "会员" in text or "vip" in low or "付费" in text:
        return WebEngineError("member_required", "该文件受百度会员或付费限制；工具不会绕过。", detail=text)
    return WebEngineError("baidu_api_error", "百度官方接口%s失败：errno=%s%s" % (action, errno, ("，" + text) if text else ""), detail=text)


class BaiduWebDriver:
    """百度分享页官方会话驱动。"""

    name = "baidu"

    def __init__(self, cfg: Optional[Dict[str, Any]] = None, target_root: str | Path = ".", **_kwargs):
        self.cfg = cfg or {}
        self.target_root = Path(target_root)
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))
        self.share_url = ""
        self.surl = ""
        self.full_surl = ""
        self.meta: Dict[str, Any] = {}
        self._signature_cache: Dict[str, str] = {}
        self._signature_at = 0.0

    # ------------------------------------------------------------ HTTP
    def _headers(self, *, referer: str = "") -> Dict[str, str]:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": SHARE_HOST,
        }
        if referer:
            headers["Referer"] = referer
        return headers

    def _request(self, url: str, *, method: str = "GET", body: Any = None, referer: str = "", timeout: int = 30):
        data = None
        headers = self._headers(referer=referer)
        if body is not None:
            if isinstance(body, (bytes, bytearray)):
                data = bytes(body)
            else:
                data = urllib.parse.urlencode(body).encode("utf-8")
                headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            return self.opener.open(req, timeout=timeout)
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                raise WebEngineError("auth_required", "百度官方网页拒绝访问（HTTP %s）" % exc.code, http_status=exc.code) from exc
            raise WebEngineError("http_%s" % exc.code, "百度官方网页返回 HTTP %s" % exc.code, retryable=exc.code >= 500, http_status=exc.code) from exc
        except urllib.error.URLError as exc:
            raise WebEngineError("network_error", "连接百度官方网页失败：%s" % exc.reason, retryable=True) from exc

    def _get_text(self, url: str, *, referer: str = "", timeout: int = 30) -> str:
        with self._request(url, referer=referer, timeout=timeout) as resp:
            raw = resp.read()
        for enc in ("utf-8", "gbk", "gb18030"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return raw.decode("utf-8", "replace")

    def _json(self, path: str, *, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None,
              method: str = "GET", referer: str = "", action: str = "请求", form: bool = False) -> Dict[str, Any]:
        merged = dict(COMMON_QUERY)
        merged.update({k: v for k, v in (params or {}).items() if v not in (None, "")})
        url = path if path.startswith("http") else SHARE_HOST + path
        if merged:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(merged)
        payload = None
        if body is not None:
            if form:
                payload = urllib.parse.urlencode(body).encode("utf-8")
            else:
                payload = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers=self._headers(referer=referer or self.share_url), method=method)
        if payload is not None:
            req.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8" if form else "application/json; charset=UTF-8")
        try:
            with self.opener.open(req, timeout=30) as resp:
                parsed = json.loads(resp.read().decode("utf-8", "replace") or "{}")
        except urllib.error.HTTPError as exc:
            raise WebEngineError("http_%s" % exc.code, "百度官方接口返回 HTTP %s" % exc.code, retryable=exc.code >= 500, http_status=exc.code) from exc
        except (urllib.error.URLError, ValueError) as exc:
            raise WebEngineError("network_error", "百度官方接口请求失败：%s" % exc, retryable=True) from exc
        if not isinstance(parsed, dict):
            raise WebEngineError("bad_response", "百度官方接口返回格式异常")
        errno = int(parsed.get("errno") or 0)
        if errno != 0:
            raise _api_error(errno, parsed.get("errmsg") or parsed.get("show_msg") or "", action=action)
        return parsed

    # ------------------------------------------------------------ 页面解析
    def _parse_page_meta(self, html: str) -> Dict[str, Any]:
        meta: Dict[str, Any] = {}
        match = re.search(r"window\.yunData\s*=\s*({.*?})\s*;", html, re.S)
        if match:
            _merge_meta(meta, _json_from_javascript_object(match.group(1)))
        match = re.search(r"window\.currentSekey\s*=\s*['\"]([^'\"]+)['\"]", html, re.S)
        if match:
            meta["sekey"] = urllib.parse.unquote(match.group(1))
        idx = html.find("locals.mset(")
        if idx >= 0:
            brace = html.find("{", idx)
            raw = _extract_balanced(html, brace)
            if raw:
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, dict):
                        _merge_meta(meta, parsed)
                except ValueError:
                    pass
        match = re.search(r'<script[^>]+id=["\']locals-data["\'][^>]*>(.*?)</script>', html, re.S | re.I)
        if match:
            try:
                parsed = json.loads(match.group(1).strip())
                if isinstance(parsed, dict):
                    _merge_meta(meta, parsed)
            except ValueError:
                pass
        return meta

    def _ensure_meta(self, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        merged = dict(self.meta)
        if meta:
            _merge_meta(merged, meta)
        share_id = _first(merged, "shareid", "share_id")
        share_uk = _first(merged, "share_uk", "uk")
        if not share_id or not share_uk:
            raise WebEngineError("bad_share_page", "分享页缺少 shareid/share_uk，可能已失效或页面结构已变化")
        merged["shareid"] = share_id
        merged["share_uk"] = share_uk
        merged.setdefault("surl", self.surl)
        self.meta = merged
        return merged

    def _set_bdclnd(self, randsk: str) -> None:
        value = _text(randsk).replace(";", "").replace("\r", "").replace("\n", "")
        cookie = http.cookiejar.Cookie(
            version=0, name="BDCLND", value=value, port=None, port_specified=False,
            domain=".baidu.com", domain_specified=True, domain_initial_dot=True,
            path="/", path_specified=True, secure=True, expires=None,
            discard=True, comment=None, comment_url=None, rest={}, rfc2109=False,
        )
        self.cookie_jar.set_cookie(cookie)
        self.meta["sekey"] = urllib.parse.unquote(value)

    def _verify_password(self, pwd: str) -> Dict[str, Any]:
        params = {
            "surl": self.surl,
            "t": str(int(time.time() * 1000)),
            **COMMON_QUERY,
        }
        body = {"pwd": _text(pwd), "vcode": "", "vcode_str": ""}
        return self._json("/share/verify", params=params, body=body, method="POST", action="校验提取码", form=True)

    # ------------------------------------------------------------ 驱动接口
    def probe(self, url: str, pwd: str = "") -> WebProbe:
        self.share_url = _text(url)
        self.full_surl = _share_slug(url)
        self.surl = extract_share_surl(url)
        html = self._get_text(self.share_url)
        self.meta = self._parse_page_meta(html)
        self.meta.setdefault("surl", self.surl)
        pwd = _text(pwd)
        requires = ("提取码" in html or "请输入提取码" in html or "verify-form" in html) and not _first(self.meta, "sekey", "currentSekey")
        if pwd and not _first(self.meta, "sekey", "currentSekey"):
            verified = self._verify_password(pwd)
            randsk = _first(verified, "randsk")
            if randsk:
                self._set_bdclnd(randsk)
            follow = "%s/s/1%s" % (SHARE_HOST, self.surl)
            if pwd:
                follow += "?pwd=" + urllib.parse.quote(pwd)
            html = self._get_text(follow, referer=self.share_url)
            _merge_meta(self.meta, self._parse_page_meta(html))
        elif requires and not pwd:
            raise WebEngineError("password_required", "该分享需要提取码；链接已自动读取 pwd 参数，链接里没有时请补提取码。")

        meta = self._ensure_meta()
        if _first(meta, "sekey", "currentSekey"):
            meta["sekey"] = urllib.parse.unquote(_first(meta, "sekey", "currentSekey"))
        title = _first(meta, "title", "share_title", "server_filename")
        if not title:
            match = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
            title = re.sub(r"\s+", " ", match.group(1)).strip() if match else "百度网盘分享"
        login_state = 0
        try:
            login_state = int(meta.get("loginstate") or 0)
        except (TypeError, ValueError):
            login_state = 0
        return WebProbe(
            driver=self.name,
            url=self.share_url,
            title=title,
            share_id=_first(meta, "shareid"),
            share_uk=_first(meta, "share_uk", "uk"),
            surl=self.surl,
            login_state=login_state,
            password_required=requires and not bool(_first(meta, "sekey")),
        )

    def _list_dir(self, path: str = "", root: bool = False, page: int = 1, num: int = 1000,
                  referer: str = "") -> Dict[str, Any]:
        meta = self._ensure_meta()
        params: Dict[str, Any] = {
            "uk": meta.get("share_uk", ""),
            "shareid": meta.get("shareid", ""),
            "order": "name",
            "desc": 0,
            "showempty": 0,
            "page": page,
            "num": num,
            "view_mode": 1,
        }
        if root:
            params.update({"root": 1, "shorturl": self.surl})
        else:
            params.update({"root": 0, "dir": path})
        sekey = _first(meta, "sekey", "currentSekey")
        if sekey:
            params["sekey"] = urllib.parse.unquote(sekey)
        return self._json("/share/list", params=params, referer=referer or self.share_url, action="列目录")

    def _list_all(self, path: str = "", root: bool = False, page_size: int = 1000) -> List[Dict[str, Any]]:
        """按官方分页参数取完整目录，避免大目录只取到第一页。"""
        out: List[Dict[str, Any]] = []
        page = 1
        while page <= 1000:
            response = self._list_dir(path=path, root=root, page=page, num=page_size)
            batch = response.get("list") or []
            if not isinstance(batch, list) or not batch:
                break
            out.extend(batch)
            if len(batch) < page_size:
                break
            page += 1
        return out

    def list_tasks(self, probe: WebProbe) -> List[Dict[str, Any]]:
        """递归列目录，返回逐文件任务（保持同名目录结构）。"""
        root_items = self._list_all(root=True)
        root_name = safe_rel_path(Path(probe.title).name or "百度网盘分享", fallback="百度网盘分享")
        tasks: List[Dict[str, Any]] = []
        visited: set[str] = set()

        def walk(items: List[Dict[str, Any]], rel_dir: str, depth: int = 0) -> None:
            if depth > 64:
                raise WebEngineError("too_deep", "分享目录层级过深，已安全停止（>64 层）")
            for raw in items:
                if not isinstance(raw, dict):
                    continue
                name = _text(raw.get("server_filename") or raw.get("filename") or raw.get("name")) or "未命名"
                remote_path = _text(raw.get("path") or raw.get("remote_path"))
                is_dir = _text(raw.get("isdir")) in ("1", "true", "True") or bool(raw.get("is_dir"))
                try:
                    size = int(raw.get("size") or 0)
                except (TypeError, ValueError):
                    size = 0
                rel = str(Path(rel_dir) / safe_rel_path(name, fallback="未命名")) if rel_dir else safe_rel_path(name, fallback="未命名")
                if is_dir:
                    if not remote_path or remote_path in visited:
                        continue
                    visited.add(remote_path)
                    children = self._list_all(path=remote_path, root=False)
                    walk(children, rel, depth + 1)
                    continue
                remote_id = _text(raw.get("fs_id") or raw.get("fid") or raw.get("id"))
                if not remote_id:
                    continue
                tasks.append({
                    "name": name,
                    "rel_path": rel,
                    "remote_id": remote_id,
                    "remote_path": remote_path,
                    "size": max(0, size),
                    "isdir": False,
                })

        # 单文件分享通常 root list 直接返回文件；分享根目录本身只作为 rel 根。
        if len(root_items) == 1 and _text(root_items[0].get("isdir")) in ("1", "true", "True"):
            walk(root_items, "", 0)
        else:
            walk(root_items, root_name, 0)
        tasks.sort(key=lambda x: x.get("rel_path", ""))
        probe.items = [RemoteItem(name=t["name"], size=t["size"], remote_id=t["remote_id"], remote_path=t["remote_path"], rel_path=t["rel_path"]) for t in tasks]
        probe.total_files = len(tasks)
        probe.total_bytes = sum(int(t.get("size") or 0) for t in tasks)
        return tasks

    def _download_signature(self) -> Dict[str, str]:
        if self._signature_cache and time.time() - self._signature_at < 60:
            return dict(self._signature_cache)
        data = self._json(
            "/share/tplconfig",
            params={"surl": self.full_surl or self.surl, "fields": "sign,timestamp,jsToken", "view_mode": 1},
            referer=self.share_url,
            action="获取下载签名",
        )
        result = data.get("result") if isinstance(data.get("result"), dict) else {}
        payload = data.get("data") if isinstance(data.get("data"), dict) else {}
        merged = dict(result)
        merged.update(payload)
        for key in ("sign", "timestamp", "jsToken"):
            if data.get(key) not in (None, ""):
                merged[key] = data.get(key)
        if not merged.get("sign") or merged.get("timestamp") in (None, ""):
            raise WebEngineError("sign_missing", "百度官方页面未返回下载签名；页面结构可能变化")
        self._signature_cache = {k: _text(v) for k, v in merged.items() if k in ("sign", "timestamp", "jsToken")}
        self._signature_at = time.time()
        return dict(self._signature_cache)

    def resolve_download_url(self, probe: WebProbe, task: Dict[str, Any], *, index: int = 1) -> str:
        meta = self._ensure_meta()
        sig = self._download_signature()
        params = {
            "sign": sig.get("sign", ""),
            "timestamp": sig.get("timestamp", ""),
        }
        if sig.get("jsToken"):
            params["jsToken"] = sig["jsToken"]
        remote_id = task.get("remote_id", "")
        fid = int(remote_id) if str(remote_id).isdigit() else remote_id
        body: Dict[str, Any] = {
            "encrypt": 0,
            "type": "dlink",
            "product": "share",
            "uk": meta.get("share_uk", ""),
            "primaryid": meta.get("shareid", ""),
            "fid_list": json.dumps([fid], ensure_ascii=False, separators=(",", ":")),
            "vip": 0,
        }
        if task.get("remote_path"):
            body["path_list"] = json.dumps([task["remote_path"]], ensure_ascii=False, separators=(",", ":"))
        sekey = _first(meta, "sekey", "currentSekey")
        if sekey:
            body["extra"] = json.dumps({"sekey": urllib.parse.unquote(sekey)}, ensure_ascii=False, separators=(",", ":"))
        data = self._json("/api/sharedownload", params=params, body=body, method="POST", referer=self.share_url, action="获取下载直链", form=True)
        dlink = _find_dlink(data)
        if not dlink:
            raise WebEngineError("dlink_missing", "百度官方接口未返回下载直链")
        if not dlink.startswith(("http://", "https://")):
            raise WebEngineError("dlink_invalid", "百度官方接口返回的下载直链格式异常")
        return dlink

    def download(self, direct_url: str, dest: str | Path, *, progress=None, task_control=None) -> Dict[str, Any]:
        return download_http_url(
            direct_url,
            dest,
            referer=self.share_url or SHARE_HOST + "/",
            user_agent=USER_AGENT,
            retries=3,
            progress=progress,
            task_control=task_control,
            opener=self.opener,
        )


def _find_dlink(value: Any) -> str:
    """从官方返回结构中提取直链；不返回其他字段。"""
    if isinstance(value, str):
        return value if value.startswith(("http://", "https://")) else ""
    if isinstance(value, list):
        for item in value:
            found = _find_dlink(item)
            if found:
                return found
        return ""
    if not isinstance(value, dict):
        return ""
    for key in ("dlink", "download_url", "url"):
        direct = value.get(key)
        if isinstance(direct, str) and direct.startswith(("http://", "https://")):
            return direct
    for key in ("dlink_list", "list", "data", "result"):
        found = _find_dlink(value.get(key))
        if found:
            return found
    return ""
