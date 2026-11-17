#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 01_候选台账 里的重复文档：每个名称只保留索引登记的那一份。

用法：python3 dedup_feishu.py          # 空跑，只打印
      python3 dedup_feishu.py --apply  # 真正删除（进回收站，可恢复）
"""
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



APPLY = "--apply" in sys.argv
T = token()
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
LEDGERS = os.environ.get("FEISHU_FOLDER_LEDGERS", "").strip()   # 01_候选台账
if not LEDGERS:
    print("ℹ️ 未配置 FEISHU_FOLDER_LEDGERS（01_候选台账 文件夹 token）"
          "→ 跳过飞书去重。配置方法见 README。", file=sys.stderr)
    raise SystemExit(0)
INDEX = _D + "/.feishu_docs.json"


def api(method, path):
    r = urllib.request.Request("https://open.feishu.cn/open-apis" + path,
                               headers={"Authorization": f"Bearer {T}"}, method=method)
    return json.load(urllib.request.urlopen(r, timeout=40, context=CTX))


def lst(ftok):
    out, pt = [], ""
    while True:
        u = ("/drive/v1/files?folder_token=" + ftok
             + "&page_size=50&order_by=CreatedTime&direction=DESC")
        if pt:
            u += "&page_token=" + pt
        d = api("GET", u)
        dat = d.get("data") or {}
        out += dat.get("files") or []
        if not dat.get("has_more"):
            break
        pt = dat.get("next_page_token", "")
    return out


idx = json.load(open(INDEX, encoding="utf-8"))
keep = set(idx["ledgers"].values())
files = [f for f in lst(LEDGERS) if f.get("type") == "docx"]
groups = {}
for f in files:
    groups.setdefault(f["name"], []).append(f)

del_list, missing = [], []
for name, fs in sorted(groups.items()):
    if len(fs) == 1:
        continue
    kept = [f for f in fs if f["token"] in keep]
    if not kept:
        missing.append(name)
        continue
    for f in fs:
        if f["token"] != kept[0]["token"]:
            del_list.append((name, f["token"]))

print(f"01_候选台账：docx {len(files)} 份｜唯一名称 {len(groups)} 个｜待删重复 {len(del_list)} 份")
for name, tok in del_list:
    print(f"   🗑  {name}  {tok}")
if missing:
    print("⚠️ 以下名称在索引里找不到登记 token，**不删**，请人工确认：")
    for m in missing:
        print(f"   · {m}")

if not APPLY:
    print("\n（空跑，未删除。加 --apply 执行）")
    sys.exit(0)

ok = bad = 0
for name, tok in del_list:
    try:
        r = api("DELETE", f"/drive/v1/files/{tok}?type=docx")
        if r.get("code") == 0:
            print(f"   ✅ 已删除 {name} {tok}")
            ok += 1
        else:
            print(f"   ❌ 删除失败 {name} {tok}：code={r.get('code')} msg={r.get('msg')}")
            bad += 1
    except Exception as e:
        print(f"   ❌ 删除异常 {name} {tok}：{type(e).__name__}: {e}")
        bad += 1
print(f"\n📊 删除成功 {ok}｜失败 {bad}")

left = [f for f in lst(LEDGERS) if f.get("type") == "docx"]
g2 = {}
for f in left:
    g2.setdefault(f["name"], []).append(f["token"])
dup2 = {k: v for k, v in g2.items() if len(v) > 1}
print(f"复查：剩余 docx {len(left)} 份｜唯一名称 {len(g2)} 个｜仍重名 {len(dup2)} 组")
for k, v in dup2.items():
    print(f"   🔴 {k} × {len(v)}")
