#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把一次 cron 通知的 markdown 追加到飞书云文档「04_自动通知」里该任务的专属文档。

本工作流要求的三通道：**飞书 IM ＋ 邮件 ＋ 飞书云文档「04_自动通知」留档**。
🔴 唯一例外：**第7步／持仓类通知不上云文档**（只走飞书 + 邮件）。

用法：
  python3 feishu_append_notice.py --task "<cron 任务全名>" --file /tmp/xxx.md
  python3 feishu_append_notice.py --task "<cron 任务全名>" --text "一行结论"

规则：
  - 一任务一文档（本工作流）。文档名 = 任务名去掉「持仓监控｜/候选监控｜/方向监控｜/第N步｜」前缀。
  - **追加**，不覆盖（保留历史）。
  - 🔴 静默判定（无实质变化）时**不要调用本脚本** —— 无变化不新增内容。
  - 🔴 持仓类任务（任务名含「持仓」）**直接拒绝**：持仓通知不出云文档。
  - 索引 .feishu_docs.json 的 "notices": {任务全名: doc_token}；缺则新建，建完立即落盘（防重名）。
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_ledgers_to_feishu import (INDEX, WRITER, api, load_index, token)  # noqa: E402

FOLDER = os.environ.get("FEISHU_FOLDER_NOTICE", "").strip()   # 04_自动通知（自建后填环境变量）
PREFIX_RE = re.compile(r"^(持仓监控|候选监控|方向监控|第\d步)｜")

# 🔴 云文档隐私：持仓数量/成本/盈亏一律不落云文档
PRIVACY = (
    (r"\d{3,6}\s*股", "疑似持股数"),
    (r"加权成本\s*[|｜:：]\s*\d", "疑似加权成本"),
    (r"(已实现|未实现)盈亏\s*[|｜:：]\s*[-−\d]", "疑似盈亏金额"),
)


def doc_title(task_name: str) -> str:
    return PREFIX_RE.sub("", task_name).strip()


def extract_body(text: str, src_name: str) -> str:
    """cron 输出文件是**完整对话记录**（含 Prompt 与技能全文）。

    🔴 不能整份灌进云文档 —— 会把提示词、技能正文一起泄到云端（实测踩到）。
    只取最后一次 `## Response` 之后的正文；没有该标记则原样返回（调用方应确认）。
    """
    m = list(re.finditer(r"^##\s*Response\s*$", text, re.M))
    if not m:
        return text.strip()
    return text[m[-1].end():].strip()


def main() -> None:
    if not FOLDER:
        print("ℹ️ 未配置 FEISHU_FOLDER_NOTICE（04_自动通知 文件夹 token）"
              "→ 跳过云文档留档。配置方法见 README。", file=sys.stderr)
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, help="cron 任务全名（jobs.json 里的 name）")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="要追加的 markdown 文件（cron 输出或纯正文）")
    src.add_argument("--text", help="要追加的短文本")
    ap.add_argument("--replace", action="store_true",
                    help="覆盖而非追加（用于修正误写内容）")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if "持仓" in a.task:
        sys.exit(f"🔴 拒绝：任务「{a.task}」属第7步／持仓类 —— 持仓通知不上云文档，"
                 f"只发飞书 + 邮件。")

    if a.file:
        p = pathlib.Path(a.file)
        if not p.exists():
            sys.exit(f"🔴 取数失败 · 待追加文件不存在：{p}")
        raw = p.read_text(encoding="utf-8")
        body = extract_body(raw, p.name)
        if body == raw.strip() and "## Response" not in raw and len(raw) > 4000:
            sys.exit("🔴 拒绝：输入文件像完整对话记录但没有 `## Response` 标记 —— "
                     "整份写入会把提示词泄到云端。请手工截取正文后再传。")
    else:
        body = a.text

    if not body.strip():
        sys.exit("🔴 拒绝：内容为空（静默判定下不应调用本脚本）")
    for rx, why in PRIVACY:
        m = re.search(rx, body)
        if m:
            sys.exit(f"🔴 拒绝：内容命中云文档隐私项「{why}」（{m.group(0)[:24]}）—— "
                     f"持仓数据不上云文档。")

    title = doc_title(a.task)
    idx = load_index()
    notices = idx.setdefault("notices", {})
    doc = notices.get(a.task, "")

    if a.dry_run:
        print(f"任务：{a.task}\n文档名：{title}\n目录：04_自动通知 {FOLDER}\n"
              f"已有 token：{doc or '（无，将新建）'}\n内容 {len(body)} 字符")
        return

    T = token()
    if not doc:
        r = api("POST", T, "/docx/v1/documents", {"folder_token": FOLDER, "title": title})
        doc = (r.get("data") or {}).get("document", {}).get("document_id", "")
        if not doc:
            sys.exit(f"🔴 建文档失败：{r.get('msg')}")
        notices[a.task] = doc
        INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  🆕 新建文档「{title}」 {doc}")

    from datetime import date
    stamp = date.today().isoformat()
    tmp = pathlib.Path(tempfile.gettempdir()) / f"notice_{stamp}.md"
    tmp.write_text(body, encoding="utf-8")
    cmd = ["python3", WRITER, str(tmp), "--doc", doc,
           "--title", f"{title} · {stamp}"]
    if not a.replace:
        cmd.append("--append")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    tail = (r.stdout or r.stderr).strip().splitlines()
    print(f"  {'✅' if r.returncode == 0 else '❌'} 追加到「{title}」 {tail[-1] if tail else ''}"[:150])
    print(f"  🔗 云文档 token：{doc}（在你的飞书云空间对应文件夹查看）")
    if r.returncode != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
