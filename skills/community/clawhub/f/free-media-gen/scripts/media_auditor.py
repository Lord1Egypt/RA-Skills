#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""free-media-gen 媒体模型审计脚本。

职责：
  1) 解析 WorkBuddy 路径（经 references/resolve_paths.py，跨用户可移植）
  2) 用已配置的平台密钥拉取各平台 /v1/models 目录，筛出图像/视频类候选
  3) 与 config.json 现有条目、以及已知"不纳入"清单比对，算出 新增/移除/待确认
  4) 对新增的图像类候选做活体测试（默认开启，--no-live 可关闭以省额度）
  5) 更新 config.json 的 status 字段
  6) 在工作区输出带日期的审计报告：免费生图生视频模型审计_YYYY-MM-DD.md
     （滚动更新：发现旧日期同名文件则改名为今天再覆盖，始终只保留一份权威文档）

用法:
  python media_auditor.py [--no-live] [--workspace DIR] [--providers agnes,sensenova]
输出: {"ok":true, "report":..., "added":[...], "removed":[...], "candidates":[...]}
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(SKILL_DIR, "templates", "audit_report.md")

# 平台目录端点（用 models.json 中该平台条目的 url 反推 base）
CATALOG_PATH = {
    "agnes": "/models",
    "sensenova": "/models",
    "siliconflow": "/models",
}

# 判定为媒体模型的关键词（小写匹配）
MEDIA_HINTS = ("image", "video", "kolors", "u1", "flux", "sd", "stable",
               "nano-banana", "imagen", "midjourney", "kling", "seedance")
# 明确排除的非媒体/已知付费关键词
EXCLUDE_HINTS = ("embedding", "rerank", "asr", "tts", "whisper", "ocr", "moderation")


def base_for(provider, models):
    """从 models.json 中该平台任一条目的 url 反推 base。

    注意：只剥离具体的操作路径（/chat/completions 等），**不能剥离 /v1**，
    因为目录端点是 {base}/models 而非 {host}/models —— 剥离 /v1 会导致
    SiliconFlow 等平台返回 404、Agnes 返回 403。
    """
    host = C.PROVIDER_HOSTS.get(provider)
    if not host:
        return None
    for e in models:
        if host in e.get("url", ""):
            u = e["url"].rstrip("/")
            for suffix in ("/chat/completions", "/completions", "/v1beta/openai",
                           "/v1beta", "/v4"):
                if u.endswith(suffix):
                    u = u[: -len(suffix)]
                    break
            return u
    return None


def fetch_catalog(provider, key, base):
    """返回 (status, model_id_list)。"""
    st, body = C.http_json(base + CATALOG_PATH[provider], None,
                           {"Authorization": "Bearer %s" % key}, method="GET",
                           retries=2, timeout=30)
    ids = []
    if isinstance(body, dict):
        data = body.get("data") or body.get("models") or []
        for m in data:
            mid = m.get("id") or m.get("name") or m.get("model")
            if mid:
                ids.append(str(mid).replace("models/", ""))
    return st, ids


def looks_media(mid):
    low = mid.lower()
    if any(x in low for x in EXCLUDE_HINTS):
        return False
    return any(x in low for x in MEDIA_HINTS)


def live_test_image(provider, key, base, mid, endpoint_hint):
    """对图像候选做一次最小生成测试。返回 (ok, detail)。"""
    url = endpoint_hint or (base + "/images/generations")
    payload = {"model": mid, "prompt": "a red circle", "n": 1, "size": "512x512"}
    st, body = C.http_json(url, payload,
                           {"Authorization": "Bearer %s" % key,
                            "Content-Type": "application/json"},
                           method="POST", retries=1, timeout=90)
    ok = st == 200 and isinstance(body, dict) and (body.get("data") or body.get("images"))
    return bool(ok), {"http": st, "resp": str(body)[:300]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-live", action="store_true", help="跳过活体测试（省额度）")
    ap.add_argument("--workspace", default=None)
    ap.add_argument("--providers", default=None, help="逗号分隔，默认全部")
    args = ap.parse_args()

    models = C.load_models_json()
    if isinstance(models, dict):
        models = models.get("models", [])
    cfg = C.load_config()
    media = cfg.get("media_models", [])
    known_ids = {m["id"] for m in media}
    excluded = {e["id"] for e in cfg.get("excluded_models", [])}

    providers = (args.providers.split(",") if args.providers
                 else ["agnes", "sensenova", "siliconflow"])

    # 若用户完全没有配置任何平台密钥 -> 首装引导分支
    available = []
    for p in providers:
        host = C.PROVIDER_HOSTS.get(p)
        if any(host in (e.get("url", "") or "") for e in models):
            available.append(p)

    if not available:
        print(json.dumps({
            "ok": False,
            "error": "no_provider_key",
            "note": ("未检测到任何可服务免费媒体模型的平台密钥。"
                     "请先到下列站点申请免费 API 并配置到 WorkBuddy 自定义模型："
                     "Agnes https://agnes-ai.cn ｜ 商汤 https://www.sensenova.cn ｜ "
                     "硅基流动 https://cloud.siliconflow.cn")
        }, ensure_ascii=False))
        sys.exit(2)

    candidates, added, unreachable = [], [], []
    for p in available:
        try:
            key = C.resolve_api_key(p, p)
        except Exception as e:
            unreachable.append({"provider": p, "error": str(e)})
            continue
        base = base_for(p, models)
        if not base:
            continue
        st, ids = fetch_catalog(p, key, base)
        if st != 200:
            unreachable.append({"provider": p, "http": st})
            continue
        for mid in ids:
            if mid in known_ids or not looks_media(mid):
                continue
            if mid in excluded:
                continue  # 已知付费/不纳入，审计时不再重复提示
            candidates.append({"provider": p, "id": mid})
        time.sleep(0.5)

    # 活体测试新增图像候选
    for c in candidates:
        if args.no_live:
            c["live"] = "已跳过"
            continue
        try:
            key = C.resolve_api_key(c["provider"], c["provider"])
            base = base_for(c["provider"], models)
            ok, detail = live_test_image(c["provider"], key, base, c["id"], None)
            c["live"] = "通过" if ok else "失败"
            c["detail"] = detail
            if ok:
                added.append(c)
        except Exception as e:
            c["live"] = "出错"
            c["detail"] = str(e)
        time.sleep(1)

    # 写回 config.json：仅把活体测试通过的新模型加入
    if added:
        for c in added:
            media.append({
                "id": c["id"],
                "provider": c["provider"],
                "modality": "image",
                "endpoint": (base_for(c["provider"], models) or "") + "/images/generations",
                "api_key_ref": "models.json:%s" % _first_id(models, c["provider"]),
                # 重要：活体测试只证明"能调用"，不证明"免费"。
                # 脚本不掌握各平台定价，一律按未核实处理，避免把付费模型
                # （如 SiliconFlow 的 Z-Image / ERNIE-Image-Turbo 系列）
                # 误标为 free 混入"免费生媒体"主清单。
                # 人工核对官方定价页后，再手动置 free=true / status=verified。
                "free": False,
                "needs_vpn": False,
                "watermark_removable": False,
                "default_size": "1024x1024",
                "features": ("审计自动发现：活体生成测试通过。免费策略【未核实】——"
                             "脚本不掌握平台定价，需人工核对官方定价页后手动置 "
                             "free=true / status=verified"),
                "status": "unverified",
            })
        cfg["media_models"] = media
        with open(C.resolve()["config_json"], "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

    # 生成审计报告（滚动：改名为今天再覆盖）
    ws = args.workspace or C.resolve()["workspace_root"]
    os.makedirs(ws, exist_ok=True)
    today = date.today().isoformat()
    fname = "免费生图生视频模型审计_%s.md" % today
    target = os.path.join(ws, fname)
    for fn in os.listdir(ws):
        if re.match(r"^免费生图生视频模型审计_\d{4}-\d{2}-\d{2}\.md$", fn) and fn != fname:
            try:
                os.remove(os.path.join(ws, fn))
            except Exception:
                pass

    body = _render_report(today, media, candidates, added, unreachable, available,
                          bool(args.no_live))
    with open(target, "w", encoding="utf-8") as f:
        f.write(body)

    print(json.dumps({"ok": True, "report": target, "added": [c["id"] for c in added],
                      "candidates": [c["id"] for c in candidates],
                      "unreachable": unreachable}, ensure_ascii=False))


def _first_id(models, provider):
    host = C.PROVIDER_HOSTS.get(provider)
    for e in models:
        if host in e.get("url", ""):
            return e.get("id")
    return ""


def _render_report(today, media, candidates, added, unreachable, available, no_live):
    """优先用 templates/audit_report.md 模板渲染；模板缺失则回退内置格式。"""
    live_note = "（本次已跳过活体测试）" if no_live else ""

    included_rows = []
    for m in media:
        included_rows.append("| `%s` | %s | %s | %s | %s | %s | %s |" % (
            m.get("id"), m.get("provider"),
            "图" if m.get("modality") == "image" else "视频",
            "✅" if m.get("free") else "❌",
            "是" if m.get("needs_vpn") else "否",
            m.get("status"), m.get("features", "")))

    if candidates:
        cand_lines = ["| 模型 | 平台 | 活体测试 |", "|---|---|---|"]
        for c in candidates:
            cand_lines.append("| `%s` | %s | %s |" % (
                c["id"], c["provider"], c.get("live", "-")))
    else:
        cand_lines = ["_本次未发现新的媒体类候选模型。_"]

    if added:
        changes = "**新增（活体测试通过）：** " + "、".join(
            "`%s`" % c["id"] for c in added)
    else:
        changes = "_本次无新增条目。_"

    if unreachable:
        un_lines = ["", "**不可达 / 失败的平台：**"]
        for u in unreachable:
            un_lines.append("- %s：%s" % (u.get("provider"),
                                          u.get("http") or u.get("error")))
    else:
        un_lines = []

    data = {
        "DATE": today,
        "PROVIDERS": "、".join(available) if available else "（无）",
        "INCLUDED_ROWS": "\n".join(included_rows),
        "CANDIDATES_BLOCK": "\n".join(cand_lines),
        "LIVE_NOTE": live_note,
        "CHANGES": changes,
        "UNREACHABLE_BLOCK": "\n".join(un_lines),
    }

    if os.path.isfile(TEMPLATE):
        try:
            with open(TEMPLATE, "r", encoding="utf-8") as f:
                tpl = f.read()
            for k, v in data.items():
                tpl = tpl.replace("{{%s}}" % k, v)
            return tpl
        except Exception:
            pass

    # 回退：内置格式
    return "\n".join([
        "# 免费生图 / 生视频模型审计 %s" % today,
        "",
        "## 一、审计范围", "",
        "已检测到平台密钥：" + (data["PROVIDERS"]),
        "",
        "## 二、当前纳入的媒体模型", "",
        "| 模型 | 平台 | 模态 | 免费 | 需 VPN | 状态 | 特点 |",
        "|---|---|---|---|---|---|---|",
        data["INCLUDED_ROWS"], "",
        "## 三、新发现的候选模型" + live_note, "",
        data["CANDIDATES_BLOCK"], "",
        "## 四、本次变更", "",
        data["CHANGES"],
    ] + un_lines + [
        "", "## 五、维护提醒", "",
        "- 密钥以明文存于 `models.json`，建议定期在平台控制台轮换。",
        "- 免费策略可能变动（如 Agnes Video 2.5 Flash 为限时免费），建议按需复检。",
        "",
    ])


if __name__ == "__main__":
    main()
