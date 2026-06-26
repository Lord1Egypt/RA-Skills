#!/usr/bin/env python3
"""
abs_search.py — Natural language → ABS dataset mapper

Maps user queries to ABS dataflow IDs using a curated lookup table
with fuzzy fallback via the cached catalog. Recognises ambiguity types
(frequency, geography, measure, series) and provides structured suggestions.

Usage:
    abs_search.py <query>
    abs_search.py --json <query>      # Output JSON (includes ambiguity info)
    abs_search.py --list              # List all curated datasets
"""

import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Ambiguity type definitions
# ---------------------------------------------------------------------------
# When multiple datasets match, classify why.
AMBIGUITY_TYPES = {
    "frequency": "Multiple frequencies available (e.g. monthly vs quarterly)",
    "geography": "Multiple geography levels available (e.g. national vs state vs SA2)",
    "measure": "Multiple measures available (e.g. index vs % change vs level)",
    "series": "Multiple related series available (e.g. original vs seasonally adjusted)",
    "dataset": "Multiple distinct datasets cover this topic",
}

# ---------------------------------------------------------------------------
# Curated lookup table: keywords → dataflow IDs (preferred first)
# IDs and versions verified against ABS API 2025
# ---------------------------------------------------------------------------
CURATED: list[dict] = [
    # Consumer prices / inflation
    {"terms": ["cpi", "consumer price", "inflation", "headline cpi", "all groups cpi"],
     "id": "CPI", "version": "2.0.0",
     "name": "Consumer Price Index (Quarterly)", "cat_no": "6401.0",
     "notes": "Quarterly. All groups, capital cities. TSEST=10 for original.",
     "ambiguity_tags": ["frequency"],
     "intent_group": "prices"},
    {"terms": ["cpi monthly", "monthly cpi", "monthly inflation", "monthly price", "cpi indicator"],
     "id": "CPI_M", "version": "1.2.0",
     "name": "Monthly CPI Indicator", "cat_no": "6484.0",
     "notes": "Monthly CPI indicator, experimental series.",
     "ambiguity_tags": ["frequency"],
     "intent_group": "prices"},
    {"terms": ["cpi weights", "basket weights", "expenditure class"],
     "id": "CPI_WEIGHTS", "version": "1.0.0",
     "name": "CPI Weights", "cat_no": "6401.0",
     "notes": "CPI expenditure class weights.",
     "ambiguity_tags": [],
     "intent_group": "prices"},
    # Wages / earnings
    {"terms": ["wpi", "wage price", "wages", "wage growth", "salary growth", "wage index", "earnings growth"],
     "id": "WPI", "version": "1.2.0",
     "name": "Wage Price Index", "cat_no": "6345.0",
     "notes": "Quarterly. Private and public sector wages.",
     "ambiguity_tags": [],
     "intent_group": "wages"},
    # Producer prices
    {"terms": ["ppi", "producer price", "input prices", "industry prices", "producer inflation"],
     "id": "PPI", "version": "1.1.3",
     "name": "Producer Price Indexes by Industry", "cat_no": "6427.0",
     "notes": "Quarterly. Industry-level PPI.",
     "ambiguity_tags": ["series"],
     "intent_group": "prices"},
    {"terms": ["ppi final demand", "final demand ppi", "final stage prices"],
     "id": "PPI_FD", "version": "1.1.0",
     "name": "Producer Price Indexes, Final Demand", "cat_no": "6427.0",
     "notes": "Quarterly. Final demand stage PPI.",
     "ambiguity_tags": ["series"],
     "intent_group": "prices"},
    # Property prices / dwelling prices
    {"terms": ["rppi", "residential property price", "house price index", "property price index",
               "dwelling price index"],
     "id": "RPPI", "version": "1.0.0",
     "name": "Residential Property Price Index", "cat_no": "6416.0",
     "notes": "Quarterly. Capital city residential property prices. Note: latest data is ~2021-Q4; use RES_DWELL_ST for current data.",
     "ambiguity_tags": ["geography", "series"],
     "intent_group": "housing"},
    {"terms": ["residential dwellings state", "dwelling values state", "mean dwelling price", "dwelling mean price",
               "house price state", "property value"],
     "id": "RES_DWELL_ST", "version": "1.0.0",
     "name": "Residential Dwellings: Values by State", "cat_no": "6416.0",
     "notes": "Quarterly. Mean dwelling value and number by state/territory. More current than RPPI.",
     "ambiguity_tags": ["geography"],
     "intent_group": "housing"},
    {"terms": ["residential dwellings gccsa", "dwelling transfers", "median dwelling price", "property transfers"],
     "id": "RES_DWELL", "version": "1.0.0",
     "name": "Residential Dwellings: Medians by GCCSA", "cat_no": "6416.0",
     "notes": "Quarterly. Unstratified medians and transfer counts by GCCSA.",
     "ambiguity_tags": ["geography"],
     "intent_group": "housing"},
    # Labour force (main series)
    {"terms": ["lf", "labour force", "labor force", "unemployment", "employment level",
               "employed persons", "jobs", "labour market", "labor market"],
     "id": "LF", "version": "1.0.0",
     "name": "Labour Force (Monthly)", "cat_no": "6202.0",
     "notes": "Monthly. Key labour force estimates. TSEST=20 for seasonally adjusted.",
     "ambiguity_tags": ["measure", "series"],
     "intent_group": "labour"},
    {"terms": ["lf ages", "labour force age", "unemployment by age", "employment by age", "youth unemployment"],
     "id": "LF_AGES", "version": "1.0.0",
     "name": "Labour Force: Age Groups", "cat_no": "6202.0",
     "notes": "Monthly. Labour force by detailed age groups.",
     "ambiguity_tags": ["geography"],
     "intent_group": "labour"},
    {"terms": ["underemployment", "underutilisation", "underutilization", "underemployed", "participation rate",
               "participation", "labour force size", "lf under"],
     "id": "LF_UNDER", "version": "1.0.1",
     "name": "Labour Force: Underemployment and Underutilisation", "cat_no": "6202.0",
     "notes": "Monthly. Contains underemployment, underutilisation, participation rate, and labour force size.",
     "ambiguity_tags": ["measure"],
     "intent_group": "labour"},
    {"terms": ["labour force education", "educational attendance labour", "students employment"],
     "id": "LF_EDU", "version": "1.0.0",
     "name": "Labour Force Educational Attendance", "cat_no": "6202.0",
     "notes": "Monthly. Labour force by educational attendance.",
     "ambiguity_tags": [],
     "intent_group": "labour"},
    # Job vacancies
    {"terms": ["jv", "job vacancies", "vacancies", "open positions", "unfilled positions", "hiring"],
     "id": "JV", "version": "1.0",
     "name": "Job Vacancies", "cat_no": "6354.0",
     "notes": "Quarterly. Total job vacancies by sector and industry.",
     "ambiguity_tags": [],
     "intent_group": "labour"},
    # National accounts / GDP
    {"terms": ["gdp", "gross domestic product", "national accounts aggregates", "economic growth", "ana agg",
               "real gdp", "gdp growth"],
     "id": "ANA_AGG", "version": "1.0.0",
     "name": "Australian National Accounts Key Aggregates", "cat_no": "5206.0",
     "notes": "Quarterly. GDP and key national accounts aggregates.",
     "ambiguity_tags": ["measure", "series"],
     "intent_group": "national_accounts"},
    {"terms": ["gdp expenditure", "gdp e", "household consumption", "government expenditure",
               "investment", "final demand components"],
     "id": "ANA_EXP", "version": "1.0.0",
     "name": "National Accounts - GDP (Expenditure)", "cat_no": "5206.0",
     "notes": "Quarterly. GDP from expenditure approach.",
     "ambiguity_tags": ["series"],
     "intent_group": "national_accounts"},
    {"terms": ["gdp income", "gdp i", "compensation of employees", "gross operating surplus",
               "mixed income"],
     "id": "ANA_INC", "version": "1.0.0",
     "name": "National Accounts - GDP (Income)", "cat_no": "5206.0",
     "notes": "Quarterly. GDP from income approach.",
     "ambiguity_tags": ["series"],
     "intent_group": "national_accounts"},
    {"terms": ["gdp production", "gdp p", "gva", "gross value added", "industry gdp", "industry output"],
     "id": "ANA_IND_GVA", "version": "1.0.0",
     "name": "National Accounts - GDP (Production/GVA)", "cat_no": "5206.0",
     "notes": "Quarterly. GVA by industry.",
     "ambiguity_tags": ["series"],
     "intent_group": "national_accounts"},
    {"terms": ["state final demand", "sfd", "state gdp", "state accounts", "state economy"],
     "id": "ANA_SFD", "version": "1.0.0",
     "name": "National Accounts - State Final Demand", "cat_no": "5206.0",
     "notes": "Quarterly. Final demand by state and territory.",
     "ambiguity_tags": ["geography"],
     "intent_group": "national_accounts"},
    # Population / ERP
    {"terms": ["erp quarterly", "quarterly population", "population quarterly",
               "population estimates quarterly", "population", "erp"],
     "id": "ERP_Q", "version": "1.0.0",
     "name": "Quarterly Population Estimates (ERP)", "cat_no": "3101.0",
     "notes": "Quarterly ERP by state/territory, sex and age.",
     "ambiguity_tags": ["frequency", "geography"],
     "intent_group": "demography"},
    {"terms": ["erp sa2", "population sa2", "population small area", "suburb population",
               "sa2 population"],
     "id": "ERP_ASGS2021", "version": "1.0.0",
     "name": "ERP by SA2 (ASGS 2021)", "cat_no": "3218.0",
     "notes": "Annual. ERP by SA2 geography (ASGS Edition 3), 2001 onwards.",
     "ambiguity_tags": ["geography"],
     "intent_group": "demography"},
    {"terms": ["erp lga", "population lga", "population local government", "lga population",
               "council population"],
     "id": "ABS_ANNUAL_ERP_LGA2024", "version": "1.0.0",
     "name": "ERP by LGA (2024)", "cat_no": "3218.0",
     "notes": "Annual. ERP by LGA, age and sex.",
     "ambiguity_tags": ["geography"],
     "intent_group": "demography"},
    # Births / deaths / natural change
    {"terms": ["births", "birth rate", "fertility", "live births", "registered births", "total fertility"],
     "id": "BIRTHS_SUMMARY", "version": "1.0.0",
     "name": "Registered Births Summary", "cat_no": "3301.0",
     "notes": "Annual. Summary births by state/territory, 1975 onwards.",
     "ambiguity_tags": [],
     "intent_group": "demography"},
    {"terms": ["births mother age", "age of mother", "fertility by age", "maternal age"],
     "id": "BIRTHS_AGE_MOTHER", "version": "1.0.0",
     "name": "Births by Age of Mother", "cat_no": "3301.0",
     "notes": "Annual. Registered births by age of mother, 1975 onwards.",
     "ambiguity_tags": [],
     "intent_group": "demography"},
    {"terms": ["deaths", "death rate", "mortality", "registered deaths", "mortality rate"],
     "id": "DEATHS_AGESPECIFIC_OCCURENCEYEAR", "version": "1.0.0",
     "name": "Deaths by Year of Occurrence", "cat_no": "3302.0",
     "notes": "Annual. Age-specific death rates by sex and state.",
     "ambiguity_tags": [],
     "intent_group": "demography"},
    # Migration
    {"terms": ["nom", "net overseas migration", "overseas migration", "permanent arrivals",
               "international migration", "net migration"],
     "id": "NOM_CY", "version": "1.0.0",
     "name": "Net Overseas Migration (Calendar Year)", "cat_no": "3412.0",
     "notes": "Annual (calendar year). NOM arrivals, departures, net by state/territory, age, sex.",
     "ambiguity_tags": ["geography"],
     "intent_group": "demography"},
    {"terms": ["net interstate migration", "nim", "interstate migration", "internal migration"],
     "id": "NIM_CY", "version": "1.0.0",
     "name": "Interstate Migration (Calendar Year)", "cat_no": "3101.0",
     "notes": "Annual (calendar year). Interstate migration by state/territory.",
     "ambiguity_tags": ["geography"],
     "intent_group": "demography"},
    # International trade in goods
    {"terms": ["itgs", "international trade goods", "merchandise trade", "exports imports goods",
               "trade balance", "goods trade", "exports", "imports", "current account goods"],
     "id": "ITGS", "version": "1.2.0",
     "name": "International Trade in Goods", "cat_no": "5368.0",
     "notes": "Monthly. Exports and imports of merchandise goods. DATA_ITEM=170 for trade balance.",
     "ambiguity_tags": ["measure"],
     "intent_group": "trade"},
    {"terms": ["merchandise exports", "commodity exports", "export commodities"],
     "id": "MERCH_EXP", "version": "1.0.0",
     "name": "Merchandise Exports by Commodity", "cat_no": "5368.0",
     "notes": "Monthly. Exports by SITC commodity and country.",
     "ambiguity_tags": [],
     "intent_group": "trade"},
    {"terms": ["merchandise imports", "commodity imports", "import commodities"],
     "id": "MERCH_IMP", "version": "1.0.0",
     "name": "Merchandise Imports by Commodity", "cat_no": "5368.0",
     "notes": "Monthly. Imports by SITC commodity and country.",
     "ambiguity_tags": [],
     "intent_group": "trade"},
    # Trade in services
    {"terms": ["trade services", "services exports", "services imports", "ebops",
               "international services trade"],
     "id": "TRADE_SERV_CNTRY_CY", "version": "1.0.0",
     "name": "International Trade in Services by Country (Calendar Year)", "cat_no": "5368.0",
     "notes": "Annual. Services trade by EBOPS classification and country.",
     "ambiguity_tags": ["frequency"],
     "intent_group": "trade"},
    # Retail trade
    {"terms": ["rt", "retail trade", "retail sales", "retail turnover"],
     "id": "RT", "version": "1.0.0",
     "name": "Retail Trade (DISCONTINUED June 2025)", "cat_no": "8501.0",
     "notes": "DISCONTINUED after June 2025. Use HSI_M (Household Spending Indicator) or BUSINESS_TURNOVER instead.",
     "ambiguity_tags": [],
     "intent_group": "consumer"},
    # Household spending (RT replacement)
    {"terms": ["household spending", "hsi", "consumer spending", "hsi monthly", "spending indicator"],
     "id": "HSI_M", "version": "1.6.0",
     "name": "Monthly Household Spending Indicator", "cat_no": "8501.0",
     "notes": "Monthly. Experimental replacement for Retail Trade (RT). Available from late 2022.",
     "ambiguity_tags": [],
     "intent_group": "consumer"},
    # Business turnover
    {"terms": ["business turnover", "monthly business indicator", "industry turnover"],
     "id": "BUSINESS_TURNOVER", "version": "1.3.0",
     "name": "Monthly Business Turnover Indicator", "cat_no": "8501.0",
     "notes": "Monthly. Business turnover by industry division.",
     "ambiguity_tags": [],
     "intent_group": "business"},
    # Housing finance / lending
    {"terms": ["lend housing", "lending indicators", "housing finance", "new loan commitments",
               "mortgages", "home loans", "loan commitments"],
     "id": "LEND_HOUSING", "version": "1.1",
     "name": "Lending Indicators Housing Finance", "cat_no": "5601.0",
     "notes": "Monthly. New loan commitments for housing.",
     "ambiguity_tags": [],
     "intent_group": "housing"},
    # Building activity
    {"terms": ["building activity", "construction", "dwellings approved", "building commencements",
               "building approvals", "construction activity"],
     "id": "BUILDING_ACTIVITY", "version": "1.0.0",
     "name": "Building Activity", "cat_no": "8752.0",
     "notes": "Quarterly. Building commencements, completions and work done.",
     "ambiguity_tags": [],
     "intent_group": "housing"},
]

# ---------------------------------------------------------------------------
# Ambiguity classification helpers
# ---------------------------------------------------------------------------

# Map intent groups to clarifying questions
CLARIFYING_QUESTIONS = {
    "prices": {
        "frequency": "Do you want monthly or quarterly data? (Monthly CPI Indicator is experimental; Quarterly CPI is the official series.)",
        "measure": "Do you want the index level, quarterly % change, or annual % change?",
    },
    "labour": {
        "measure": "Do you want the unemployment rate, participation rate, employment level, or underemployment rate?",
        "series": "Do you want seasonally adjusted (TSEST=20) or original (TSEST=10) data?",
        "geography": "Do you want national totals or state/territory breakdowns?",
    },
    "national_accounts": {
        "series": "Do you want GDP from expenditure, income, or production approach? Or the key aggregates (ANA_AGG)?",
        "measure": "Do you want the level (chain volume), quarterly % change, or annual % change?",
        "geography": "Do you want national data or state final demand by state?",
    },
    "demography": {
        "geography": "Do you want national/state data (ERP_Q), SA2 (ERP_ASGS2021), or LGA (ABS_ANNUAL_ERP_LGA2024)?",
        "frequency": "Do you want quarterly estimates or annual (SA2/LGA)?",
    },
    "housing": {
        "geography": "Do you want national mean price (RES_DWELL_ST), city-level index (RPPI), or GCCSA medians (RES_DWELL)?",
        "series": "Note: RPPI has stale data in the API (~2021). RES_DWELL_ST is current to latest quarter.",
    },
    "trade": {
        "measure": "Do you want the trade balance, total exports, or total imports? (All from ITGS dataset.)",
        "frequency": "Goods trade is monthly (ITGS); services trade is annual (TRADE_SERV_CNTRY_CY).",
    },
}


def _detect_ambiguity(results: list, query: str) -> dict:
    """
    Given a list of matching datasets, detect ambiguity types and generate
    structured suggestions grouped by ambiguity type.
    """
    if len(results) <= 1:
        return {}

    # Collect all ambiguity tags
    all_tags = set()
    for r in results:
        for tag in r.get("ambiguity_tags", []):
            all_tags.add(tag)

    # Get intent groups
    intent_groups = set(r.get("intent_group", "other") for r in results)

    ambiguity = {}

    for tag in all_tags:
        # Get datasets with this tag
        tagged = [r for r in results if tag in r.get("ambiguity_tags", [])]
        if tagged:
            ambiguity[tag] = {
                "type_description": AMBIGUITY_TYPES.get(tag, tag),
                "datasets": [{"id": r["id"], "name": r["name"], "notes": r.get("notes", "")} for r in tagged],
            }
            # Add clarifying question if we have one for this intent group
            for ig in intent_groups:
                q = CLARIFYING_QUESTIONS.get(ig, {}).get(tag)
                if q:
                    ambiguity[tag]["clarifying_question"] = q
                    break

    return ambiguity


# ---------------------------------------------------------------------------

def search(query: str, limit: int = 10) -> list:
    """Map a natural language query to candidate ABS dataflows."""
    q = query.lower().strip()
    tokens = q.split()
    scored = []
    for entry in CURATED:
        all_terms = " ".join(entry["terms"]).lower()
        # Exact term match
        exact = any(q == t for t in entry["terms"])
        # Token overlap
        overlap = sum(1 for tok in tokens if tok in all_terms)
        # Substring match
        substr = any(t in q or q in t for t in entry["terms"])
        score = (10 if exact else 0) + overlap * 2 + (1 if substr else 0)
        if score > 0:
            scored.append((score, entry))
    scored.sort(key=lambda x: -x[0])
    results = [e for _, e in scored[:limit]]

    # Fuzzy fallback via cached catalog
    if not results:
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            import abs_cache
            catalog = abs_cache.load_catalog()
            catalog_hits = abs_cache.search(query, catalog, limit=limit)
            results = [
                {"id": h["id"], "version": h["version"], "name": h["name"],
                 "terms": [], "cat_no": "", "notes": "(catalog match)",
                 "ambiguity_tags": [], "intent_group": "other"}
                for h in catalog_hits
            ]
        except Exception:
            pass

    return results


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    as_json = False
    if args[0] == "--json":
        as_json = True
        args = args[1:]
    elif args[0] == "--list":
        for entry in CURATED:
            print(f"{entry['id']:40s}  {entry['name']}")
        sys.exit(0)

    if not args:
        print("Usage: abs_search.py <query>")
        sys.exit(1)

    query_str = " ".join(args)
    results = search(query_str)
    ambiguity = _detect_ambiguity(results, query_str)

    if as_json:
        output = {
            "query": query_str,
            "results": results,
            "ambiguity": ambiguity,
        }
        print(json.dumps(output, indent=2))
    else:
        if not results:
            print(f"No datasets found for: {query_str!r}")
            print("Try: abs_search.py --list")
        else:
            print(f"Found {len(results)} dataset(s) for: {query_str!r}\n")
            for r in results:
                discontinued = "DISCONTINUED" in r.get("notes", "").upper()
                flag = " ⚠️  DISCONTINUED" if discontinued else ""
                print(f"  ID:      {r['id']}  (v{r['version']}){flag}")
                print(f"  Name:    {r['name']}")
                if r.get("cat_no"):
                    print(f"  Cat No:  {r['cat_no']}")
                if r.get("notes"):
                    print(f"  Notes:   {r['notes']}")
                print()

            # Print ambiguity hints if any
            if ambiguity:
                print("─" * 50)
                print("Ambiguity detected — multiple datasets match your query:\n")
                for tag, info in ambiguity.items():
                    print(f"  [{tag.upper()}] {info['type_description']}")
                    if "clarifying_question" in info:
                        print(f"  → {info['clarifying_question']}")
                    print()


if __name__ == "__main__":
    main()
