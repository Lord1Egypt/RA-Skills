#!/usr/bin/env python3
"""
scan_queries.py — Genera URLs/queries por plataforma a partir del perfil
y la config. El agente toma esta lista y usa sus tools (WebFetch, browser)
para extraer las ofertas reales.

No scrapea — solo construye la "lista de tareas" de scan.

Uso:
    python3 scan_queries.py --profile profile.json --config config.json
    python3 scan_queries.py --profile profile.json --config config.json --json
"""

import argparse
import json
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _quote(s: str) -> str:
    return urllib.parse.quote_plus(s)


def queries_linkedin(profile: dict, config: dict) -> list[dict]:
    out = []
    plat = config.get("platforms", {}).get("linkedin", {})
    if not plat.get("enabled"):
        return out
    queries = plat.get("search_queries") or []
    if not queries:
        # fallback a títulos preferidos
        queries = config.get("candidate", {}).get("preferred_titles") or ["Senior Backend Engineer remote"]
    filters = plat.get("filters") or {}
    for q in queries:
        params = {"keywords": q}
        if filters.get("remote_only"):
            params["f_WT"] = "2"
        if filters.get("posted_within_days"):
            seconds = int(filters["posted_within_days"]) * 86400
            params["f_TPR"] = f"r{seconds}"
        url = "https://www.linkedin.com/jobs/search/?" + urllib.parse.urlencode(params)
        out.append({
            "platform": "linkedin",
            "query": q,
            "url": url,
            "method": "fetch",
            "extraction_hint": "Parsear cards de la grilla — clase 'job-search-card' o similar. Title, company, location, link al detalle.",
        })
    return out


def queries_remoteok(profile: dict, config: dict) -> list[dict]:
    plat = config.get("platforms", {}).get("remoteok", {})
    if not plat.get("enabled"):
        return []
    out = [{
        "platform": "remoteok",
        "query": "all",
        "url": "https://remoteok.com/api",
        "method": "api",
        "extraction_hint": "JSON array. Filtrar items con tags que crucen profile.skills.* o tags configurados.",
    }]
    for tag in plat.get("tags", []):
        out.append({
            "platform": "remoteok",
            "query": f"tag={tag}",
            "url": f"https://remoteok.com/remote-{tag}-jobs",
            "method": "fetch",
            "extraction_hint": "Filtrar por tag en HTML — fallback si la API tiene rate limit.",
        })
    return out


def queries_weworkremotely(profile: dict, config: dict) -> list[dict]:
    plat = config.get("platforms", {}).get("weworkremotely", {})
    if not plat.get("enabled"):
        return []
    out = []
    for cat in plat.get("categories", ["programming"]):
        out.append({
            "platform": "weworkremotely",
            "query": f"category={cat}",
            "url": f"https://weworkremotely.com/categories/remote-{cat}-jobs.rss",
            "method": "rss",
            "extraction_hint": "RSS estándar. <item> con <title>, <link>, <description>, <pubDate>.",
        })
    return out


def queries_wellfound(profile: dict, config: dict) -> list[dict]:
    plat = config.get("platforms", {}).get("wellfound", {})
    if not plat.get("enabled"):
        return []
    filters = plat.get("filters") or {}
    params = {}
    if filters.get("remote_ok"):
        params["remote"] = "true"
    if filters.get("min_salary_usd"):
        params["salary_min"] = str(filters["min_salary_usd"])
    base = "https://wellfound.com/jobs"
    url = base + ("?" + urllib.parse.urlencode(params) if params else "")
    return [{
        "platform": "wellfound",
        "query": "filtered",
        "url": url,
        "method": "fetch",
        "extraction_hint": "Sin login solo se ve resumen. Para detalles avisar al usuario que abra el link.",
    }]


def queries_getonboard(profile: dict, config: dict) -> list[dict]:
    plat = config.get("platforms", {}).get("getonboard", {})
    if not plat.get("enabled"):
        return []
    out = []
    cats = plat.get("categories", ["programming"])
    remote = "yes" if plat.get("remote_only", True) else "no"
    for cat in cats:
        url = f"https://www.getonbrd.com/search-jobs/category/{cat}/remote/{remote}"
        out.append({
            "platform": "getonboard",
            "query": f"category={cat} remote={remote}",
            "url": url,
            "method": "fetch",
            "extraction_hint": "Cards de jobs con salario en USD frecuentemente expuesto. Buena señal LATAM.",
        })
    return out


def queries_torre(profile: dict, config: dict) -> list[dict]:
    plat = config.get("platforms", {}).get("torre", {})
    if not plat.get("enabled"):
        return []
    titles = config.get("candidate", {}).get("preferred_titles", [])
    out = []
    for t in titles[:3]:
        out.append({
            "platform": "torre",
            "query": t,
            "url": f"https://torre.co/search/jobs?q={_quote(t)}",
            "method": "fetch",
            "extraction_hint": "Backed por API en /api/entities/_searchStream — POST con body. Si tools soportan POST, usar API.",
        })
    return out


def queries_workana(profile: dict, config: dict) -> list[dict]:
    plat = config.get("platforms", {}).get("workana", {})
    if not plat.get("enabled"):
        return []
    titles = config.get("candidate", {}).get("preferred_titles", [])
    out = []
    for t in titles[:2]:
        out.append({
            "platform": "workana",
            "query": t,
            "url": f"https://www.workana.com/jobs?query={_quote(t)}",
            "method": "fetch",
            "extraction_hint": "Mayormente freelance. Filtrar por tipo full-time si busca empleo.",
        })
    return out


def queries_hn(profile: dict, config: dict) -> list[dict]:
    plat = config.get("platforms", {}).get("hn_who_is_hiring", {})
    if not plat.get("enabled"):
        return []
    return [{
        "platform": "hn_who_is_hiring",
        "query": "latest_thread",
        "url": "https://news.ycombinator.com/submitted?id=whoishiring",
        "method": "fetch",
        "extraction_hint": (
            "Tomar el post más reciente titulado 'Ask HN: Who is hiring?'. "
            "Cada top-level comment es una oferta individual. Filtrar por 'REMOTE' "
            "en el primer paréntesis del comment."
        ),
    }]


def queries_company_pages(profile: dict, config: dict) -> list[dict]:
    plat = config.get("platforms", {}).get("company_pages", {})
    if not plat.get("enabled"):
        return []
    out = []
    for company in plat.get("companies", []):
        out.append({
            "platform": "company_page",
            "query": company,
            "url": f"https://www.google.com/search?q={_quote('site:greenhouse.io ' + company + ' OR site:lever.co ' + company + ' OR site:ashbyhq.com ' + company)}",
            "method": "search",
            "extraction_hint": (
                "Buscar la career page real de la empresa en ATS comunes (Greenhouse/Lever/Ashby). "
                "Una vez identificada, fetch directo a la página de jobs y parsear listings."
            ),
            "company": company,
        })
    return out


HANDLERS = [
    queries_linkedin,
    queries_remoteok,
    queries_weworkremotely,
    queries_wellfound,
    queries_getonboard,
    queries_torre,
    queries_workana,
    queries_hn,
    queries_company_pages,
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    config = json.loads(args.config.read_text(encoding="utf-8"))

    all_queries = []
    for h in HANDLERS:
        all_queries.extend(h(profile, config))

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_queries": len(all_queries),
        "queries": all_queries,
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"# Scan queries — {len(all_queries)} totales")
        print(f"# Generado: {payload['generated_at']}\n")
        by_platform: dict = {}
        for q in all_queries:
            by_platform.setdefault(q["platform"], []).append(q)
        for plat, items in by_platform.items():
            print(f"## {plat} ({len(items)})")
            for q in items:
                print(f"  • [{q['method']}] {q['query']}")
                print(f"    {q['url']}")
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
