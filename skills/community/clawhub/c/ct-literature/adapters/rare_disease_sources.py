"""rare_disease_sources.py — 罕见病/遗传病专源检索（ct-literature 补充模块）。

向后兼容：所有函数均可在无 API key 时 graceful 降级（返回空结果 + skipped 状态），
不影响 ct-literature 主流程。

数据源：
- Orphanet (orpha.net) — 罕见病本体、流行病学、基因关联
- OMIM (omim.org) — 基因-疾病关联、表型
- ClinVar (ncbi.nlm.nih.gov/clinvar) — 基因变异-疾病关联

API key 配置（可选）：
- ORPHA_API_KEY — Orphanet API key（https://www.orpha.net/）
- OMIM_API_KEY — OMIM API key（https://omim.org/help/api）

无 key 时：返回 skipped 状态 + 文档链接，不阻塞主流程。
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from typing import Any

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
ORPHA_API_KEY = os.environ.get("ORPHA_API_KEY", "")
OMIM_API_KEY = os.environ.get("OMIM_API_KEY", "")

ORPHA_BASE_URL = "https://api.orphadata.com"
OMIM_BASE_URL = "https://api.omim.org/api"
CLINVAR_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# ---------------------------------------------------------------------------
# 通用 HTTP 工具
# ---------------------------------------------------------------------------
def _http_get_json(url: str, timeout: int = 15, headers: dict | None = None) -> dict | None:
    """GET JSON，失败返回 None。"""
    try:
        req = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return None


def _http_get_text(url: str, timeout: int = 15) -> str | None:
    """GET text，失败返回 None。"""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError):
        return None


# ---------------------------------------------------------------------------
# Orphanet
# ---------------------------------------------------------------------------
def search_orphanet(disease_name: str) -> dict:
    """按疾病名称搜索 Orphanet。

    返回标准化结果：
    {
        "source": "Orphanet",
        "status": "ok" | "skipped" | "error",
        "disease": str,
        "results": list[dict],  # 每个含 orpha_number, name, prevalence, gene, url
        "note": str,
    }
    """
    if not ORPHA_API_KEY:
        return {
            "source": "Orphanet",
            "status": "skipped",
            "disease": disease_name,
            "results": [],
            "note": "ORPHA_API_KEY 未配置；跳过 Orphanet 检索。申请 key: https://www.orpha.net/",
        }

    url = f"{ORPHA_BASE_URL}/disease/search?query={urllib.parse.quote(disease_name)}&key={ORPHA_API_KEY}"
    data = _http_get_json(url)
    if not data or "data" not in data:
        return {
            "source": "Orphanet",
            "status": "error",
            "disease": disease_name,
            "results": [],
            "note": f"Orphanet API 调用失败或无结果: {url}",
        }

    results = []
    for item in data.get("data", []):
        results.append({
            "orpha_number": item.get("orphaNumber", ""),
            "name": item.get("name", ""),
            "prevalence": item.get("prevalence", ""),
            "gene": item.get("gene", ""),
            "url": f"https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=EN&Expert={item.get('orphaNumber', '')}",
        })

    return {
        "source": "Orphanet",
        "status": "ok",
        "disease": disease_name,
        "results": results,
        "note": f"命中 {len(results)} 条罕见病记录",
    }


# ---------------------------------------------------------------------------
# OMIM
# ---------------------------------------------------------------------------
def search_omim(gene_or_disease: str) -> dict:
    """按基因或疾病名称搜索 OMIM。

    返回标准化结果：
    {
        "source": "OMIM",
        "status": "ok" | "skipped" | "error",
        "query": str,
        "results": list[dict],  # 每个含 mim_number, title, gene, phenotype, url
        "note": str,
    }
    """
    if not OMIM_API_KEY:
        return {
            "source": "OMIM",
            "status": "skipped",
            "query": gene_or_disease,
            "results": [],
            "note": "OMIM_API_KEY 未配置；跳过 OMIM 检索。申请 key: https://omim.org/help/api",
        }

    url = f"{OMIM_BASE_URL}/entry/search?search={urllib.parse.quote(gene_or_disease)}&apiKey={OMIM_API_KEY}&format=json"
    data = _http_get_json(url)
    if not data or "omim" not in data:
        return {
            "source": "OMIM",
            "status": "error",
            "query": gene_or_disease,
            "results": [],
            "note": f"OMIM API 调用失败或无结果: {url}",
        }

    results = []
    for entry in data.get("omim", {}).get("searchResponse", {}).get("entryList", []):
        entry_data = entry.get("entry", {})
        results.append({
            "mim_number": entry_data.get("mimNumber", ""),
            "title": entry_data.get("titles", {}).get("preferredTitle", ""),
            "gene": entry_data.get("geneSymbol", ""),
            "phenotype": entry_data.get("phenotype", ""),
            "url": f"https://omim.org/entry/{entry_data.get('mimNumber', '')}",
        })

    return {
        "source": "OMIM",
        "status": "ok",
        "query": gene_or_disease,
        "results": results,
        "note": f"命中 {len(results)} 条 OMIM 记录",
    }


# ---------------------------------------------------------------------------
# ClinVar
# ---------------------------------------------------------------------------
def search_clinvar(gene: str) -> dict:
    """按基因符号搜索 ClinVar 变异摘要。

    返回标准化结果：
    {
        "source": "ClinVar",
        "status": "ok" | "error",
        "gene": str,
        "results": list[dict],  # 每个含 variation_id, clinical_significance, condition, url
        "note": str,
    }
    """
    # 先搜索
    search_url = f"{CLINVAR_BASE_URL}/esearch.fcgi?db=clincvar&term={urllib.parse.quote(gene)}&retmode=json&retmax=10"
    search_data = _http_get_json(search_url)
    if not search_data or "esearchresult" not in search_data:
        return {
            "source": "ClinVar",
            "status": "error",
            "gene": gene,
            "results": [],
            "note": f"ClinVar 搜索失败: {search_url}",
        }

    ids = search_data.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return {
            "source": "ClinVar",
            "status": "ok",
            "gene": gene,
            "results": [],
            "note": f"ClinVar 中无 {gene} 的变异记录",
        }

    # 获取摘要
    summary_url = f"{CLINVAR_BASE_URL}/esummary.fcgi?db=clincvar&term={urllib.parse.quote(gene)}&retmode=json"
    summary_data = _http_get_json(summary_url)

    results = []
    if summary_data and "result" in summary_data:
        for uid in ids[:10]:
            entry = summary_data.get("result", {}).get(uid, {})
            results.append({
                "variation_id": uid,
                "clinical_significance": entry.get("clinical_significance", {}).get("description", ""),
                "condition": entry.get("condition", ""),
                "url": f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{uid}/",
            })

    return {
        "source": "ClinVar",
        "status": "ok",
        "gene": gene,
        "results": results,
        "note": f"命中 {len(results)} 条 ClinVar 变异记录",
    }


# ---------------------------------------------------------------------------
# 统一入口
# ---------------------------------------------------------------------------
def search_rare_disease(disease_name: str, gene: str | None = None) -> dict:
    """统一罕见病检索入口。

    返回：
    {
        "disease": str,
        "gene": str | None,
        "sources": {
            "orphanet": dict,
            "omim": dict,
            "clinvar": dict | None,
        },
        "total_results": int,
        "note": str,
    }
    """
    orpha_result = search_orphanet(disease_name)
    omim_result = search_omim(gene or disease_name)
    clinvar_result = search_clinvar(gene) if gene else None

    total = len(orpha_result.get("results", [])) + len(omim_result.get("results", []))
    if clinvar_result:
        total += len(clinvar_result.get("results", []))

    return {
        "disease": disease_name,
        "gene": gene,
        "sources": {
            "orphanet": orpha_result,
            "omim": omim_result,
            "clinvar": clinvar_result,
        },
        "total_results": total,
        "note": f"罕见病检索完成，共 {total} 条结果",
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    import argparse
    ap = argparse.ArgumentParser(description="罕见病/遗传病专源检索")
    ap.add_argument("--disease", required=True, help="疾病名称")
    ap.add_argument("--gene", help="基因符号（可选）")
    ap.add_argument("--output", help="输出 JSON 文件路径")
    args = ap.parse_args()

    result = search_rare_disease(args.disease, args.gene)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"OK 结果已写入: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
