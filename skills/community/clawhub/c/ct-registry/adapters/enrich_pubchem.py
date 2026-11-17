#!/usr/bin/env python3
"""enrich_pubchem.py - PubChem PUG-REST drug->CID/props/targets / 药物->靶点映射.

Reads public data only. / 仅读公开数据。

设计约束（ct-base §13.5 / P0-B 优雅降级）：PubChem 富化为"可选增强"，绝不
应因其失败（药物未被 PubChem 收录、网络 404、超时）而拖垮整个注册库检索。
因此：404 / 未收录 -> 视为"无富化结果"（exit 0 + 空记录 + status=not_found）；
其它网络异常 -> 同样降级（exit 0 + status=error），由调用方决定是否继续。
"""
import argparse
import json
import urllib.error
import urllib.parse
import urllib.request

PUB = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"


class DrugNotFound(Exception):
    """PubChem 未收录该药名（PUGREST 404 或空 CID 列表）。"""


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ct-registry/0.1", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # PUGREST.NotFound -> 药物未被收录，转为业务级"未找到"（非致命）
        if e.code == 404:
            raise DrugNotFound("HTTP 404 PUGREST.NotFound")
        raise


def cid_of(name):
    d = _get(f"{PUB}/compound/name/{urllib.parse.quote(name)}/cids/JSON")
    cids = (d.get("IdentifierList") or {}).get("CID") or []
    if not cids:
        raise DrugNotFound("empty CID list")
    return cids[0]


def props_of(name):
    d = _get(f"{PUB}/compound/name/{urllib.parse.quote(name)}/property/MolecularWeight,IUPACName,IsomericSMILES/JSON")
    props = (d.get("PropertyTable") or {}).get("Properties") or []
    if not props:
        raise DrugNotFound("empty property table")
    return props[0]


def targets_of(cid):
    try:
        d = _get(f"{PUB}/compound/cid/{cid}/assaysummary/JSON")
        genes = set()
        for row in d.get("Table", {}).get("Rows", []):
            g = row.get("GeneSymbol")
            if g:
                genes.add(g)
        return sorted(genes)
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser(description="PubChem drug->target (public).")
    ap.add_argument("--drug", required=True)
    ap.add_argument("--targets", action="store_true", help="include gene targets / 含靶点基因")
    ap.add_argument("--out", default="pubchem.json")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()

    if not args.run:
        print(f"[pubchem][PREVIEW] would enrich drug='{args.drug}' (add --run to execute)")
        return

    # 优雅降级：药物未被 PubChem 收录 / 网络异常 -> 写空结果、exit 0，
    # 绝不影响调用方（ct_registry.py）的注册库检索主流程。
    try:
        cid = cid_of(args.drug)
    except DrugNotFound:
        print(f"[pubchem][WARN] PubChem 未收录 '{args.drug}'（PUGREST 404 / 空结果），"
              f"跳过化合物富化（不影响注册库检索）。")
        out = {"source": "PUBCHEM", "records": [], "status": "not_found",
               "drug": args.drug,
               "note": "drug not found in PubChem; enrichment skipped (non-fatal)"}
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        return
    except (urllib.error.URLError, OSError) as e:
        print(f"[pubchem][WARN] PubChem 访问异常（{e}），跳过化合物富化（不影响注册库检索）。")
        out = {"source": "PUBCHEM", "records": [], "status": "error",
               "drug": args.drug, "note": f"pubchem network error: {e}"}
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        return

    rec = {"drug": args.drug, "cid": cid, "props": props_of(args.drug)}
    if args.targets:
        rec["targets"] = targets_of(cid)
    out = {"source": "PUBCHEM", "records": [rec]}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[pubchem] {args.drug} -> CID {cid} -> {args.out}")


if __name__ == "__main__":
    main()
