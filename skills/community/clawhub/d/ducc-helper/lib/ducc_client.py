#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DUCC（泰山配置中心）内网接口公共客户端层。

统一封装：
  - 认证：复用 jme_auth 从本机京ME客户端零配置换出 sso.jd.com（唯一 Cookie）
  - 必带头：请求真实域名 pserve.jd.com，每个请求带两个自定义头：
      * config-env : online(生产) / pre(预发)
      * x-proxy-opts : 网关代理路由，生产/预发 target 不同（见 ENV_PROXY）
  - code→ID 解析：用户只给 code(pop_customs_center / center_config / common)，
    自动调 search 接口反查出数字 ID(nsId / cId / profileId)。

所有业务脚本都基于本模块。接口基址与字段细节见 references/api.md。

【环境区分】（实测，最关键的地基）
  生产 online : x-proxy-opts target = http://console.ducc.jd.com
  预发 pre    : x-proxy-opts target = http://pre.console.ducc.jd.local
  两个头必须配套切换。预发未开放时，pre 读到 data:[] 或 503「环境不存在」。
"""

import json
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jme_auth  # noqa: E402

BASE = "http://pserve.jd.com/api/duccApi"   # 真实域名（http，非 taishan）

# config-env → x-proxy-opts target
ENV_PROXY = {
    "online": "http://console.ducc.jd.com",
    "pre": "http://pre.console.ducc.jd.local",
}

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


def log(msg):
    print(f"[ducc] {msg}", file=sys.stderr)


def normalize_env(env):
    """环境归一化：prod/生产/online → online；pre/预发/yufa → pre。默认 online。"""
    if env in (None, "", "online", "prod", "生产", "prd"):
        return "online"
    if env in ("pre", "预发", "yufa", "preview"):
        return "pre"
    return env


class DuccClient:
    """DUCC 接口客户端。构造时取一次 sso cookie，之后复用。"""

    def __init__(self, env="online", force_refresh=False):
        self.cookie = jme_auth.get_sso_cookie(force_refresh=force_refresh)
        self.env = normalize_env(env)
        self._ns_cache = {}      # code -> ns dict
        self._cfg_cache = {}     # (nsId, code) -> cfg dict
        self._prof_cache = {}    # (nsId, cId, code) -> profile dict

    # ── 底层请求 ──────────────────────────────────────────────────────
    def _headers(self, env=None, json_body=False):
        e = normalize_env(env) if env else self.env
        target = ENV_PROXY.get(e, ENV_PROXY["online"])
        proxy = json.dumps({"target": target, "pathRewrite": {"^/api/duccApi": "/"}})
        h = {
            "Cookie": self.cookie,
            "Accept": "application/json, text/plain, */*",
            "User-Agent": _UA,
            "config-env": e,
            "x-proxy-opts": proxy,
        }
        if json_body:
            h["Content-Type"] = "application/json"
        return h

    def get(self, path, env=None):
        """GET，path 为 /api/duccApi 之后的部分。返回 (status_code, parsed_json_or_none)。"""
        url = f"{BASE}{path}"
        try:
            resp = requests.get(url, headers=self._headers(env=env), timeout=40)
        except requests.exceptions.RequestException as e:
            log(f"请求失败：{url} -> {e}")
            return -1, None
        return self._parse(resp)

    def post(self, path, body, env=None):
        url = f"{BASE}{path}"
        try:
            resp = requests.post(url, headers=self._headers(env=env, json_body=True),
                                 data=json.dumps(body), timeout=60)
        except requests.exceptions.RequestException as e:
            log(f"请求失败：{url} -> {e}")
            return -1, None
        return self._parse(resp)

    def put(self, path, body=None, env=None):
        url = f"{BASE}{path}"
        try:
            resp = requests.put(url, headers=self._headers(env=env, json_body=body is not None),
                                data=json.dumps(body) if body is not None else None, timeout=60)
        except requests.exceptions.RequestException as e:
            log(f"请求失败：{url} -> {e}")
            return -1, None
        return self._parse(resp)

    def delete(self, path, body=None, env=None):
        url = f"{BASE}{path}"
        try:
            resp = requests.delete(url, headers=self._headers(env=env, json_body=body is not None),
                                   data=json.dumps(body) if body is not None else None, timeout=60)
        except requests.exceptions.RequestException as e:
            log(f"请求失败：{url} -> {e}")
            return -1, None
        return self._parse(resp)

    @staticmethod
    def _parse(resp):
        body = resp.text or ""
        if not body.strip():
            return resp.status_code, None
        try:
            return resp.status_code, resp.json()
        except ValueError:
            return resp.status_code, {"_raw": body[:500]}

    @staticmethod
    def ok(data):
        """DUCC 业务成功判定：{code:200,...}。"""
        return isinstance(data, dict) and data.get("code") == 200

    # ── code → ID 解析 ────────────────────────────────────────────────
    # 注意：命名空间、配置文件列表是"环境无关"的元数据，一律用 online 解析；
    # 只有 profile（生产配置/预发配置）和配置项才随 env 切换。
    def resolve_ns(self, ns):
        """命名空间：传数字→当详情查；传 code→search 反查。返回 ns dict（含 id/code/name）。"""
        if isinstance(ns, int) or (isinstance(ns, str) and ns.isdigit()):
            _, data = self.get(f"/v1/namespace/{ns}", env="online")
            return data.get("data") if self.ok(data) else None
        if ns in self._ns_cache:
            return self._ns_cache[ns]
        # search 全量翻找（命名空间数量少）
        _, data = self.get("/v1/namespaces/search?page=1&size=1000", env="online")
        if not self.ok(data):
            return None
        for item in data.get("data", []):
            if item.get("code") == ns:
                self._ns_cache[ns] = item
                return item
        return None

    def resolve_config(self, ns_id, cfg):
        """配置文件：传数字→直接用；传 code→在该 ns 下 search 反查。返回 cfg dict（含 id/code/name）。"""
        if isinstance(cfg, int) or (isinstance(cfg, str) and cfg.isdigit()):
            return {"id": int(cfg), "code": None}
        key = (ns_id, cfg)
        if key in self._cfg_cache:
            return self._cfg_cache[key]
        _, data = self.get(
            f"/v1/namespace/{ns_id}/configs/search?page=1&size=1000&dataTypes=0,2&filterNoProfile=true",
            env="online")
        if not self.ok(data):
            return None
        for item in data.get("data", []):
            if item.get("code") == cfg:
                self._cfg_cache[key] = item
                return item
        return None

    def resolve_profile(self, ns_id, cfg_id, prof, env=None):
        """profile（生产配置/预发配置，如 dev/common）：传数字→直接用；传 code→profiles/search 反查。"""
        if isinstance(prof, int) or (isinstance(prof, str) and prof.isdigit()):
            return {"id": int(prof), "code": None}
        key = (ns_id, cfg_id, prof)
        if key in self._prof_cache:
            return self._prof_cache[key]
        _, data = self.get(
            f"/admin/v2/namespace/{ns_id}/profiles/search?page=1&size=1000&configType=0", env=env)
        if not self.ok(data):
            return None
        for item in data.get("data", []):
            if item.get("code") == prof:
                self._prof_cache[key] = item
                return item
        return None

    def resolve_all(self, ns, cfg=None, prof=None, env=None):
        """一次性解析 ns/cfg/prof 三级 code→ID。返回 (ns_dict, cfg_dict, prof_dict)，缺项为 None。"""
        ns_d = self.resolve_ns(ns)
        if not ns_d:
            return None, None, None
        cfg_d = prof_d = None
        if cfg is not None:
            cfg_d = self.resolve_config(ns_d["id"], cfg)
            if cfg_d and prof is not None:
                prof_d = self.resolve_profile(ns_d["id"], cfg_d["id"], prof, env=env)
        return ns_d, cfg_d, prof_d

    # ── 当前用户 ──────────────────────────────────────────────────────
    def current_erp(self):
        """当前登录用户 erp（发布 submitter 用）。走 GET /v1/login/user 的 data.code。"""
        if getattr(self, "_erp", None):
            return self._erp
        _, data = self.get("/v1/login/user", env="online")
        self._erp = (data.get("data") or {}).get("code") if self.ok(data) else None
        return self._erp


def add_common_args(ap):
    """给 argparse 添加所有脚本共用的认证/环境参数。"""
    ap.add_argument("--env", default="online",
                    help="环境：online/生产(默认) 或 pre/预发。预发未开放时读到空或503")
    ap.add_argument("--force-refresh", action="store_true",
                    help="强制刷新京ME token（忽略缓存，token 过期报错时用）")
    ap.add_argument("--clear-cache", action="store_true",
                    help="清除本地 token 缓存后退出")


def emit(obj):
    """统一 stdout 输出 JSON。"""
    print(json.dumps(obj, ensure_ascii=False, indent=2))
