# -*- coding: utf-8 -*-
"""Health Canada Vigilance — 本地批量入库适配器 (T1 三件套之一)。

架构定位
--------
与 FAERS（实时 openFDA API）不同，Canada Vigilance 提供**整库 ASCII 抽取**
（extract_extrait.zip，11 张关系表，`$` 分隔、字段带引号，1965–2026-04-30，月更）。
本模块把整库下载到本地（CT_SAFETY_DATA_DIR/canada，skill 包外），解析后物化
2x2 计数索引，对外暴露与 fetch_faers.fetch_counts **同构**的接口：

    fetch_counts(drug, event=None, field, top, api_key, run, out,
                 date_from, date_to, timeout, retries) -> result dict

result 含 source=="Canada Vigilance" / drug_total / grand_total /
event_total / counts={a,b,c,d,...}。ct_safety.py 的失配比引擎
（disproportionality.compute(a,b,c,d)）因此零改动复用。

2x2 定义（与 FAERS 一致）：
    a = 报告数(药物 D[疑似角色] 且 反应 E 同报告)
    b = drug_total - a
    c = event_total - a
    d = grand_total - a - b - c
    drug_total  = 含疑似药物 D 的报告数
    event_total = 含反应 E 的报告数
    grand_total = 数据集总报告数

列名解析策略：Canada 抽取表的列名以 alias 列表在运行时按 header 解析，
真实文件名/列名确定后只需微调下列 *_ALIASES / SUSPECTED_ROLES。
"""

import os
import sys
import csv
import json
import pickle
import zipfile
from pathlib import Path

# ── 数据目录（skill 包外，避免被发布打包）──────────────────────────────
ENV = os.environ.get("CT_SAFETY_DATA_DIR", str(Path.home() / "ct-safety-data"))
CANADA_DIR = Path(ENV) / "canada"
ZIP_PATH = CANADA_DIR / "extract_extrait.zip"
EXTRACT_DIR = CANADA_DIR / "extracted"
INDEX_PATH = CANADA_DIR / "index.pkl"

# ── 列名 alias（待解压后核实真实 header 微调）─────────────────────────
REPORT_ID_ALIASES = ["REPORT_ID", "REPORT_NO", "REPORTID", "REPORT_NO_9"]
DRUG_NAME_ALIASES = ["DRUGNAME", "DRUG_NAME", "MEDICINAL_PRODUCT", "DRUGNAME_ENG"]
ACTIVE_ING_ALIASES = ["ACTIVE_INGREDIENT_NAME", "ACTIVE_INGREDIENT", "INGREDIENT"]
ROLE_ALIASES = ["ROLE_COD", "DRUG_ROLE", "ROLE"]
REACTION_ALIASES = ["PT_NAME", "REACTION_PT", "REACTION_MEDDRA_PT", "PT", "REAC_OD"]

# 药物角色：疑似（用于 drug 侧计数）。待核实真实取值后微调。
SUSPECTED_ROLES = {"SUS", "SUSPECTED", "1", "PS", "PRIMARY_SUSPECTED"}

# 是否同时把「活性成分」作为可检索药物键（与品牌名并列）。
INDEX_ACTIVE_INGREDIENT = True


def _norm(s):
    return (s or "").strip().lower()


def _resolve_col(header, aliases):
    """在 header 列表中按 alias（大小写不敏感）找列索引；找不到返回 -1。"""
    up = [h.strip().upper() for h in header]
    for a in aliases:
        if a.upper() in up:
            return up.index(a.upper())
    return -1


def _find_table(paths, required_alias_groups):
    """从候选文件列表中挑出含 required alias 组里至少一个列的文件。"""
    best = None
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                r = csv.reader(f, delimiter="$", quotechar='"')
                hdr = next(r, None)
        except Exception:
            continue
        if not hdr:
            continue
        up = {h.strip().upper() for h in hdr}
        score = sum(1 for grp in required_alias_groups
                    if any(a.upper() in up for a in grp))
        if score and (best is None or score > best[1]):
            best = (p, score)
    return best[0] if best else None


def _ensure_extracted():
    """确保抽取文件已解压；返回解压目录 Path。"""
    CANADA_DIR.mkdir(parents=True, exist_ok=True)
    if not EXTRACT_DIR.exists() or not any(EXTRACT_DIR.iterdir()):
        if not ZIP_PATH.exists():
            raise FileNotFoundError(
                "未找到 Canada 整库抽取：%s\n"
                "请先下载 extract_extrait.zip 到该路径（见 SKILL.md / 记忆）。" % ZIP_PATH)
        print("[INFO] 解压 Canada 抽取 %s ..." % ZIP_PATH)
        with zipfile.ZipFile(ZIP_PATH) as z:
            z.extractall(EXTRACT_DIR)
    return EXTRACT_DIR


def _list_txt(paths):
    return [str(p) for p in paths if p.suffix.lower() in (".txt", ".csv", ".dat")]


def build_index(force=False):
    """解析抽取表 → 物化 2x2 计数索引（counts 形式，内存友好）。

    返回并持久化到 INDEX_PATH：
        {"n_total": int,
         "drug_cases": {drug_lower: count},
         "event_cases": {event_lower: count},
         "pair_cases": {(drug_lower, event_lower): count},
         "meta": {...}}
    """
    if INDEX_PATH.exists() and not force:
        with open(INDEX_PATH, "rb") as f:
            return pickle.load(f)

    ext = _ensure_extracted()
    files = _list_txt(sorted(ext.rglob("*")))
    if not files:
        raise RuntimeError("解压后未发现任何 ASCII 数据文件：%s" % ext)

    drug_tbl = _find_table(files, [DRUG_NAME_ALIASES + ACTIVE_ING_ALIASES, ROLE_ALIASES])
    reac_tbl = _find_table(files, [REACTION_ALIASES])
    if not drug_tbl or not reac_tbl:
        raise RuntimeError(
            "未能定位 drug 表(%s) 或 reaction 表(%s)。files=%s"
            % (drug_tbl, reac_tbl, [os.path.basename(f) for f in files]))

    print("[INFO] drug 表=%s | reaction 表=%s" % (
        os.path.basename(drug_tbl), os.path.basename(reac_tbl)))

    # Pass 1: report_id -> 疑似药物列表（品牌名 + 活性成分）
    rid_i = rep_i = dname_i = aing_i = role_i = None
    with open(drug_tbl, "r", encoding="utf-8", errors="replace") as f:
        r = csv.reader(f, delimiter="$", quotechar='"')
        hdr = next(r)
        rid_i = _resolve_col(hdr, REPORT_ID_ALIASES)
        dname_i = _resolve_col(hdr, DRUG_NAME_ALIASES)
        aing_i = _resolve_col(hdr, ACTIVE_ING_ALIASES)
        role_i = _resolve_col(hdr, ROLE_ALIASES)
        drug_cases = {}
        report_drugs = {}
        for row in r:
            if rid_i < 0 or rid_i >= len(row):
                continue
            rid = _norm(row[rid_i])
            if not rid:
                continue
            role = _norm(row[role_i]) if role_i >= 0 else ""
            if role and role not in SUSPECTED_ROLES:
                continue  # 仅计疑似药物
            names = []
            if dname_i >= 0 and dname_i < len(row):
                n = _norm(row[dname_i])
                if n:
                    names.append(n)
            if INDEX_ACTIVE_INGREDIENT and aing_i >= 0 and aing_i < len(row):
                n = _norm(row[aing_i])
                if n:
                    names.append(n)
            if not names:
                continue
            report_drugs[rid] = names
            for n in names:
                drug_cases[n] = drug_cases.get(n, 0) + 1

    # Pass 2: reaction 表 → 与同报告疑似药物求笛卡尔积，累加 pair/event 计数
    event_cases = {}
    pair_cases = {}
    with open(reac_tbl, "r", encoding="utf-8", errors="replace") as f:
        r = csv.reader(f, delimiter="$", quotechar='"')
        hdr = next(r)
        rid_i2 = _resolve_col(hdr, REPORT_ID_ALIASES)
        ev_i = _resolve_col(hdr, REACTION_ALIASES)
        for row in r:
            if rid_i2 < 0 or rid_i2 >= len(row):
                continue
            rid = _norm(row[rid_i2])
            if not rid:
                continue
            ev = _norm(row[ev_i]) if ev_i >= 0 else ""
            if not ev:
                continue
            drugs = report_drugs.get(rid)
            if not drugs:
                continue
            event_cases[ev] = event_cases.get(ev, 0) + 1
            for d in drugs:
                pair_cases[(d, ev)] = pair_cases.get((d, ev), 0) + 1

    n_total = len(report_drugs)
    index = {
        "n_total": n_total,
        "drug_cases": drug_cases,
        "event_cases": event_cases,
        "pair_cases": pair_cases,
        "meta": {
            "source": "Canada Vigilance (Health Canada)",
            "drug_table": os.path.basename(drug_tbl),
            "reaction_table": os.path.basename(reac_tbl),
            "n_drug_keys": len(drug_cases),
            "n_event_keys": len(event_cases),
            "n_pairs": len(pair_cases),
        },
    }
    with open(INDEX_PATH, "wb") as f:
        pickle.dump(index, f, protocol=pickle.HIGHEST_PROTOCOL)
    print("[OK] 索引已构建：n_total=%d, 药物键=%d, 反应键=%d, 药×反应对=%d"
          % (n_total, len(drug_cases), len(event_cases), len(pair_cases)))
    return index


def _resolve_drug(index, q):
    """把查询药名解析为索引中的规范键；精确(ci) → 子串回退。"""
    qn = _norm(q)
    if qn in index["drug_cases"]:
        return qn
    # 子串回退（取最长匹配键，避免 "in" 误中）
    hits = [k for k in index["drug_cases"] if qn in k]
    if hits:
        return max(hits, key=len)
    return None


def _resolve_event(index, e):
    en = _norm(e)
    if en in index["event_cases"]:
        return en
    hits = [k for k in index["event_cases"] if en in k]
    if hits:
        return max(hits, key=len)
    return None


def fetch_counts(drug, event=None, field="drug", top=10, api_key=None,
                 run=False, out=None, date_from=None, date_to=None,
                 timeout=120, retries=3, index=None):
    """与 fetch_faers.fetch_counts 同构的本地批量版。

    注：Canada 整库无 openFDA 式 field 选择/日期窗口 API；date_from/date_to
    在该整库版本暂忽略（抽取已是全量截至 2026-04-30）。field 仅占位兼容签名。
    """
    if not run:
        print("[PREVIEW] 将查询 Canada Vigilance 本地索引 drug=%r event=%r "
              "(use --run 执行)" % (drug, event))
        return None

    if index is None:
        index = build_index()

    key = _resolve_drug(index, drug)
    if key is None:
        print("[WARN] Canada 索引中未匹配到药物 %r（尝试子串也未命中）" % drug)
        return {"source": "Canada Vigilance", "drug": drug, "event": event,
                "error": "drug_not_found", "counts": None}

    drug_total = index["drug_cases"].get(key, 0)
    grand_total = index["n_total"]

    # top events for this drug (pair 计数里以该药为前缀的)
    top_ev = sorted(
        ((ev, c) for (d, ev), c in index["pair_cases"].items() if d == key),
        key=lambda x: -x[1])[:top]
    top_events = [{"term": ev, "count": c} for ev, c in top_ev]

    result = {
        "source": "Canada Vigilance",
        "api": "Health Canada data extract (local bulk)",
        "drug": drug,
        "field": field,
        "date_from": date_from,
        "date_to": date_to,
        "drug_total": drug_total,
        "grand_total": grand_total,
        "top_events": top_events,
        "event": None,
        "counts": None,
    }

    if event:
        ekey = _resolve_event(index, event)
        if ekey is None:
            print("[WARN] Canada 索引中未匹配到反应 %r" % event)
            result["error"] = "event_not_found"
            if out:
                _dump(out, result)
            return result
        a = index["pair_cases"].get((key, ekey), 0)
        event_total = index["event_cases"].get(ekey, 0)
        b = drug_total - a
        c = event_total - a
        d = grand_total - a - b - c
        result["event"] = event
        result["event_total"] = event_total
        result["counts"] = {"a": a, "b": b, "c": c, "d": d,
                            "drug_total": drug_total,
                            "event_total": event_total,
                            "grand_total": grand_total}

    if out:
        _dump(out, result)
    return result


def _dump(out, result):
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("[OK] wrote", out)


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Canada Vigilance 本地批量索引/查询")
    ap.add_argument("--drug", required=True)
    ap.add_argument("--event", default=None)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--build-index", action="store_true",
                    help="仅重建本地 2x2 计数索引")
    ap.add_argument("--index-info", action="store_true",
                    help="打印索引元信息（药/反应键数、总报告数）")
    args = ap.parse_args(argv)

    if args.build_index:
        build_index(force=True)
        return 0
    if args.index_info:
        idx = build_index()
        print(json.dumps(idx["meta"], ensure_ascii=False, indent=2))
        return 0

    res = fetch_counts(args.drug, args.event, top=args.top, run=True, out=args.out)
    if res and args.out is None:
        print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
