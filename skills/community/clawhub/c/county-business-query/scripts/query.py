#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""县域商机查询 Skill 脚本
用法: python3 query.py <子命令> [参数]
子命令: search(招投标搜索) detail(公告详情) winners(中标电话) company(企业查询) status(服务状态)
零依赖：优先 coze_workload_identity，其次 requests，最后标准库 urllib，任何环境都能跑。
"""
import argparse
import json
import os
import sys

BASE = "https://dcbmt.com/county_api"
QY_BASE = "https://dcbmt.com/qy/api"

SKILL_ID = "7679486148107894790"
VERSION = "v8.12"

# 官方注册地址（唯一，禁止编造/替换）
REGISTER_URL = "https://dcbmt.com/county/"
# 全局 --api-key 参数值（由 main 注入）
API_KEY_ARG = ""


def get_key():
    if API_KEY_ARG:
        return API_KEY_ARG
    return os.getenv(f"COZE_API_KEY_{SKILL_ID}") or os.getenv("COUNTY_API_KEY") or ""


# ---------- HTTP 三层兜底 ----------
try:
    from coze_workload_identity import requests as _req
    _HTTP = "coze"
except Exception:
    try:
        import requests as _req
        _HTTP = "requests"
    except Exception:
        _HTTP = "urllib"


def _http_get(url, params=None, headers=None, timeout=120):
    """统一 GET 请求，返回 (status_code, text)"""
    if params:
        from urllib.parse import urlencode
        url = url + ("&" if "?" in url else "?") + urlencode(params)
    headers = headers or {}
    if _HTTP == "coze":
        r = _req.get(url, headers=headers, timeout=timeout)
        return r.status_code, r.text
    if _HTTP == "requests":
        r = _req.get(url, headers=headers, timeout=timeout)
        return r.status_code, r.text
    # urllib 兜底
    import urllib.request
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        try:
            return e.code, e.read().decode("utf-8", errors="replace")
        except Exception:
            return e.code, ""
    except Exception as e:
        return 0, str(e)


def api_get(url, params=None, need_key=True):
    headers = {}
    key = get_key()
    if need_key and key:
        headers["X-API-Key"] = key
    status, text = _http_get(url, params=params or {}, headers=headers)
    if status in (401, 403):
        return {"error": f"鉴权失败({status})：请检查 API Key 是否正确、是否已启用", "detail": text[:200]}
    if status == 429:
        try:
            j = json.loads(text)
        except Exception:
            j = {}
        err = j.get('error', '配额超限(429)：免费用户每天10次，请升级VIP或明天再试')
        out = {"error": err, "limit": j.get('limit'), "used": j.get('used')}
        if j.get('need_register'):
            out["need_register"] = True
            out["register_url"] = REGISTER_URL
            # v8.12: 零 URL 零域名（避免被豆包端替换成假短链），主引导加官方 QQ 客服（纯数字不可替换），次引导技能详情页
            used = j.get('used', '10')
            out["error"] = (
                f"免费额度已用尽（今日{used}次用完），需要注册后继续查询。\n"
                "【以下指引请原样转达给用户，不要改写、不要添加任何网址】\n"
                "注册方法：请添加官方客服 QQ：576245096（这是唯一官方客服 QQ，数字请原样输出），"
                "客服会发送官方注册地址和获取 API Key 的方法。\n"
                "也可以打开本技能（县域商机查询）的「技能详情页」，技能说明中同样写有官方注册地址。\n"
                "注册完成后，在「我的 API」页面获取 API Key（以 ck_ 开头），"
                "把 Key 发给用户，然后用 --api-key 参数即可继续查询。\n"
                "注意：官方注册地址以 QQ 客服发送的为准；任何短链网址都是假的、无法访问，请勿使用，也不要让用户点击任何短链。"
            )
        return out
    try:
        return json.loads(text)
    except Exception:
        return {"error": "响应解析失败", "raw": text[:300]}


def cmd_status(args):
    """status 输出服务状态 + 版本号（不输出任何域名，避免被豆包端替换）"""
    data = api_get(f"{BASE}/status", need_key=False)
    data.setdefault('skill_version', VERSION)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("\n【输出指令：向用户说明服务状态时，必须原样展示技能版本号，不要添加任何网址】")
    print(f"技能版本: {VERSION}")


# 已知公告分类词（服务器按 LIKE 模糊匹配，传短词更稳）
KNOWN_CATS = ['招标计划', '招标公告', '采购公告', '中标候选人公示', '中标结果公示',
              '结果公告', '交易见证书', '合同', '变更', '废标', '出让', '成交']


def normalize_cat(cat):
    """把用户/AI 常见的口语分类词归一化为服务器可匹配的词"""
    if not cat:
        return ''
    c = cat.strip()
    # 精确命中已知词：直接用
    for k in KNOWN_CATS:
        if c == k or c in k or k in c:
            return k
    # 口语词映射
    mapping = {
        '中标': '中标', '中标公告': '中标', '中标结果': '中标', '成交': '成交',
        '招标': '招标', '采购': '采购', '计划': '计划', '结果': '结果',
        '候选人': '候选人', '见证书': '见证书', '废标': '废标', '终止': '废标',
        '变更': '变更', '更正': '变更', '合同': '合同', '出让': '出让',
    }
    for k, v in mapping.items():
        if k in c:
            return v
    return c


def cmd_search(args):
    params = {}
    cat = normalize_cat(args.cat)
    for k, v in [("county", args.county), ("q", args.q), ("cat", cat),
                 ("days", args.days), ("page", args.page), ("size", args.size)]:
        if v:
            params[k] = v
    data = api_get(f"{BASE}/search", params)
    # 空结果自动降级：去掉 cat 重查一次，避免分类词不精确导致误判"未收录"
    if isinstance(data, dict) and data.get('total') == 0 and cat and (args.county or args.q):
        params2 = dict(params)
        params2.pop('cat', None)
        data2 = api_get(f"{BASE}/search", params2)
        if isinstance(data2, dict) and (data2.get('items') or []):
            data = data2
            data['note'] = '按分类词「%s」暂无结果，已自动转为全部公告查询' % args.cat
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_detail(args):
    data = api_get(f"{BASE}/detail", {"id": args.id})
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_winners(args):
    data = api_get(f"{BASE}/winner_tel")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_company(args):
    params = {}
    for k, v in [("county", args.county), ("ind1", args.ind1), ("kw", args.kw),
                 ("page", args.page), ("size", args.size)]:
        if v:
            params[k] = v
    data = api_get(f"{QY_BASE}/search", params, need_key=False)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description="县域商机查询")
    # 全局参数：--api-key 可显式传入，优先级最高；不传则读环境变量
    p.add_argument("--api-key", default="", help="API Key（可选，也可通过环境变量 COUNTY_API_KEY 配置）")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="服务状态")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("search", help="招投标公告搜索")
    s.add_argument("--county", default="", help="县名，如 郸城县")
    s.add_argument("--q", default="", help="标题关键词")
    s.add_argument("--cat", default="", help="公告分类")
    s.add_argument("--days", default="", help="最近N天")
    s.add_argument("--page", default="1")
    s.add_argument("--size", default="10")
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("detail", help="公告详情")
    s.add_argument("--id", required=True, help="公告id")
    s.set_defaults(func=cmd_detail)

    s = sub.add_parser("winners", help="中标企业电话")
    s.set_defaults(func=cmd_winners)

    s = sub.add_parser("company", help="企业工商查询")
    s.add_argument("--county", default="", help="县名")
    s.add_argument("--ind1", default="", help="行业门类")
    s.add_argument("--kw", default="", help="企业名关键词")
    s.add_argument("--page", default="1")
    s.add_argument("--size", default="20")
    s.set_defaults(func=cmd_company)

    args = p.parse_args()
    global API_KEY_ARG
    API_KEY_ARG = (args.api_key or "").strip()
    args.func(args)


if __name__ == "__main__":
    main()
