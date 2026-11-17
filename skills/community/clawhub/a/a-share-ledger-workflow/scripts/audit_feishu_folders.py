#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出飞书股票工作流各文件夹的实际文档，与本地索引对账找重名/孤儿。"""
import os
import json
import ssl
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_ledgers_to_feishu import token  # noqa: E402
# ── 数据根目录（环境变量；未设置即报错，不回落任何具体路径）──────────────
_D = os.environ.get("STOCK_DATA_DIR", "").rstrip("/")
if not _D:
    raise SystemExit(
        "🔴 未设置环境变量 STOCK_DATA_DIR（你的股票数据根目录）。\n"
        '   例：export STOCK_DATA_DIR="$HOME/stock_data"\n'
        "   目录结构见 README「数据目录约定」。"
    )



T = token()
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def lst(ftok):
    out, pt = [], ""
    while True:
        u = ("https://open.feishu.cn/open-apis/drive/v1/files?folder_token=" + ftok
             + "&page_size=50&order_by=CreatedTime&direction=DESC")
        if pt:
            u += "&page_token=" + pt
        r = urllib.request.Request(u, headers={"Authorization": f"Bearer {T}"})
        d = json.load(urllib.request.urlopen(r, timeout=40, context=CTX))
        if d.get("code") != 0:
            print(f"   ❌ code={d.get('code')} msg={d.get('msg')}")
            return None
        dat = d.get("data") or {}
        out += dat.get("files") or []
        if not dat.get("has_more"):
            break
        pt = dat.get("next_page_token", "")
    return out


FOLDERS = {
    "根目录":      os.environ.get("FEISHU_FOLDER_TOKEN", "").strip(),
    "01_候选台账": os.environ.get("FEISHU_FOLDER_LEDGERS", "").strip(),
    "02_方向研究": os.environ.get("FEISHU_FOLDER_DIRECTION", "").strip(),
    "04_自动通知": os.environ.get("FEISHU_FOLDER_NOTICE", "").strip(),
}
listing = {}
if not FOLDERS["根目录"]:
    print("ℹ️ 未配置飞书文件夹 token（FEISHU_FOLDER_TOKEN 等）"
          "→ 跳过飞书审计。配置方法见 README。", file=sys.stderr)
    raise SystemExit(0)
for nm, tk in FOLDERS.items():
    fs = lst(tk)
    if fs is None:
        continue
    listing[nm] = fs
    print(f"[{nm}] {len(fs)} 项")
    for f in fs:
        print(f"   {f.get('type'):9s} {f.get('token')}  {f.get('name')}")

print("\n===== 重名检查 =====")
for nm, fs in listing.items():
    docs = [f for f in fs if f.get("type") == "docx"]
    seen = {}
    for f in docs:
        seen.setdefault(f["name"], []).append(f["token"])
    dup = {k: v for k, v in seen.items() if len(v) > 1}
    print(f"[{nm}] docx {len(docs)} 份｜重名 {len(dup)} 组")
    for k, v in sorted(dup.items()):
        print(f"   🔴 「{k}」× {len(v)}：{v}")

idx = json.load(open(_D + "/.feishu_docs.json", encoding="utf-8"))
print("\n===== 与本地索引对账 =====")
print("索引 01_候选台账:", len(idx["ledgers"]), "｜02_方向研究:", len(idx.get("direction", {})))
for nm, fs in listing.items():
    if not fs:
        continue
    cloud = {f["name"] for f in fs if f.get("type") == "docx"}
    if nm == "02_方向研究":
        local = set(idx.get("direction", {}).keys())
    elif nm == "01_候选台账":
        local = {f"{k} 跟踪台账" for k in idx["ledgers"]}
    else:
        continue
    only_cloud = sorted(cloud - local)
    only_local = sorted(local - cloud)
    print(f"\n[{nm}] 云端多出 {len(only_cloud)}｜本地索引多出 {len(only_local)}")
    for x in only_cloud:
        print(f"   ☁️ 仅在云端：{x}")
    for x in only_local:
        print(f"   💾 仅索引有：{x}")
