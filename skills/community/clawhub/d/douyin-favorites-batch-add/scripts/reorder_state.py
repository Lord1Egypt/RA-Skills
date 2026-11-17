#!/usr/bin/env python3
"""按最新表格重排抖音入夹队列顺序（保留进度字段），幂等。

用法: python reorder_state.py "C:/path/MyLike_分类结果_YYYY-MM-DD.xlsx"
"""
import json
import os
import sys
import datetime

import openpyxl

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "douyin-queue", "state.json")


def main(xlsx):
    wb = openpyxl.load_workbook(xlsx, read_only=True)
    fs = wb["文件夹清单"]
    order = []
    for row in fs.iter_rows(min_row=2, values_only=True):
        if row[1]:
            order.append(row[1])
    wb.close()

    st = json.load(open(STATE, encoding="utf-8"))
    old = {f["name"]: f for f in st["folders"]}
    missing = [n for n in order if n not in old]
    extra = [n for n in old if n not in set(order)]
    if missing or extra:
        print(json.dumps({"ok": False, "missing_in_state": missing, "not_in_table": extra}, ensure_ascii=False))
        return 1

    st["folders"] = [old[n] for n in order]
    st["source"] = os.path.basename(xlsx)
    st["updated"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    tmp = STATE + ".tmp"
    json.dump(st, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(tmp, STATE)

    print(json.dumps({
        "ok": True,
        "folders": len(st["folders"]),
        "remaining": sum(f["total"] - f["cursor"] for f in st["folders"]),
        "done": sum(1 for f in st["folders"] if f["status"] == "done"),
        "head": [f["name"] for f in st["folders"][:3]],
        "source": st["source"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
