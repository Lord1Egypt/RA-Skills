#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日工作日记归档（通用版）。

读取脚本上一级目录的 config.json 决定归档目标，支持：
  1. 笔记端：在目标笔记本内列目录实时比对标题 -> 已存在跳过（--append 可追加），否则新建并移入
  2. 每个配置的知识库文件夹：列目录比对文件名 -> 同名跳过，否则上传

用法：
  python3 archive_diary.py --date 2026-10-12 --file /path/工作日记_2026-10-12.md
  python3 archive_diary.py --date 2026-10-12 --file ... --dry-run
  python3 archive_diary.py --date 2026-10-12 --file ... --append
"""

import os
import sys
import json
import argparse
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(HERE, "..", "config.json"))
BASE = "https://ima.qq.com"

CLIENT = os.environ.get("IMA_OPENAPI_CLIENTID", "")
APIKEY = os.environ.get("IMA_OPENAPI_APIKEY", "")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(json.dumps({"ok": False,
                          "error": "config.json not found. Copy config.example.json -> config.json and fill ids."},
                         ensure_ascii=False))
        sys.exit(1)
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def api(path, body):
    """IMA OpenAPI 调用。必须用 curl 子进程：Python urllib 会因 header 大小写规范化被 403。"""
    p = subprocess.run(
        ["curl", "-s", "-X", "POST", BASE + path,
         "-H", "ima-openapi-clientid: " + CLIENT,
         "-H", "ima-openapi-apikey: " + APIKEY,
         "-H", "Content-Type: application/json",
         "-d", json.dumps(body, ensure_ascii=False)],
        capture_output=True, text=True,
    )
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"code": -1, "msg": "non-json response: " + (p.stdout or p.stderr)[:300]}


def extract_title(path):
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s:
                    return s.lstrip("#").strip()
    except Exception:
        pass
    return os.path.splitext(os.path.basename(path))[0]


def get_cos_key(path):
    p = subprocess.run(["ima_cos_util", "-f", path], capture_output=True, text=True)
    out = (p.stdout or "").strip()
    return out.splitlines()[-1].strip() if out else ""


def find_note(notebook_id, title):
    """目标笔记本内列目录实时比对标题；notebook_id 为空时查全部笔记。"""
    cursor, fetched = "", 0
    while True:
        body = {"sort_type": 0, "cursor": cursor, "limit": 20}
        body["folder_id"] = notebook_id or ""
        r = api("/openapi/note/v1/list_note", body)
        data = r.get("data") or {}
        items = data.get("note_book_list") or []
        for nb in items:
            if (nb.get("title") or "").strip() == title:
                return nb.get("note_id")
        fetched += len(items)
        if data.get("is_end") or not items or fetched >= 100:
            return None
        cursor = str(fetched)


def archive_note(path, notebook_id, notebook_name, title, dry_run, append):
    existing = find_note(notebook_id, title)
    if existing:
        if dry_run:
            return {"ok": True, "mode": "exists_would_skip", "note_id": existing}
        if not append:
            return {"ok": True, "mode": "exists_skip", "note_id": existing}
        cos_key = get_cos_key(path)
        if not cos_key:
            return {"ok": False, "error": "ima_cos_util returned no cosKey"}
        r = api("/openapi/note/v1/push_note",
                {"note_id": existing, "content_format": 1, "content_cos_key": cos_key})
        return {"ok": r.get("code") == 0, "mode": "append", "note_id": existing}
    if dry_run:
        return {"ok": True, "mode": "would_create"}
    cos_key = get_cos_key(path)
    if not cos_key:
        return {"ok": False, "error": "ima_cos_util returned no cosKey"}
    r = api("/openapi/note/v1/push_note", {"content_format": 1, "content_cos_key": cos_key})
    nid = (r.get("data") or {}).get("note_id")
    if r.get("code") == 0 and nid:
        if notebook_id:
            api("/openapi/note/v1/move_notes",
                {"note_ids": [nid], "target_folder_id": notebook_id,
                 "target_folder_name": notebook_name})
        return {"ok": True, "mode": "create", "note_id": nid}
    return {"ok": False, "mode": "create", "code": r.get("code"), "msg": r.get("msg")}


def kb_exists(kb_id, folder_id, filename):
    cursor, fetched = "", 0
    while True:
        r = api("/openapi/wiki/v1/get_knowledge_list",
                {"cursor": cursor, "limit": 50, "knowledge_base_id": kb_id,
                 "folder_id": folder_id})
        data = r.get("data") or {}
        items = data.get("knowledge_list") or []
        for it in items:
            if (it.get("title") or "").strip() == filename:
                return True
        fetched += len(items)
        if data.get("is_end") or not items or fetched >= 200:
            return False
        cursor = data.get("next_cursor") or ""


def archive_kb(path, kb, filename, dry_run):
    kb_id = kb.get("kb_id")
    folder_id = kb.get("folder_id")
    if not kb_id:
        return {"ok": False, "error": "kb_id empty"}
    if kb_exists(kb_id, folder_id, filename):
        return {"ok": True, "mode": "exists_would_skip" if dry_run else "exists_skip"}
    if dry_run:
        return {"ok": True, "mode": "would_upload"}
    p = subprocess.run(
        ["python3", os.path.join(HERE, "upload_to_kb.py"),
         "--file-path", path, "--knowledge-base-id", kb_id, "--folder-id", folder_id],
        capture_output=True, text=True,
    )
    tail = (p.stdout or p.stderr or "").strip().splitlines()
    return {"ok": p.returncode == 0, "mode": "upload", "log": tail[-1] if tail else ""}


def main():
    ap = argparse.ArgumentParser(description="每日工作日记多通道归档")
    ap.add_argument("--date", required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--append", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    path = os.path.abspath(args.file)
    if not os.path.exists(path):
        print(json.dumps({"ok": False, "error": "file not found: " + path}, ensure_ascii=False))
        sys.exit(1)

    title = extract_title(path)
    filename = os.path.basename(path)
    nb_id = cfg.get("note_notebook_id") or ""
    nb_name = cfg.get("note_notebook_name") or ""
    report = {"date": args.date, "note_title": title, "filename": filename,
              "dry_run": args.dry_run, "results": {}}

    try:
        report["results"]["note"] = archive_note(path, nb_id, nb_name, title, args.dry_run, args.append)
    except Exception as e:  # noqa
        report["results"]["note"] = {"ok": False, "error": str(e)}

    for i, kb in enumerate(cfg.get("knowledge_bases") or []):
        try:
            report["results"]["kb_%d" % i] = archive_kb(path, kb, filename, args.dry_run)
        except Exception as e:  # noqa
            report["results"]["kb_%d" % i] = {"ok": False, "error": str(e)}

    report["ok"] = all(v.get("ok") for v in report["results"].values()) if report["results"] else False
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report["ok"] else 2)


if __name__ == "__main__":
    main()
