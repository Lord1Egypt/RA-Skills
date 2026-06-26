#!/usr/bin/env python3
"""
Deep dive into a single basket — fetches detail, token analysis, and graph data
in one call.

Usage:
  python3 fetch_basket_detail.py <slug-or-name> [--include=detail,tokens,graph]

Arguments:
  slug-or-name  Basket slug (e.g., "defense-mode") or partial name for fuzzy match
  --include     Comma-separated sections to fetch. Default: detail,tokens,graph (all)
                Options: detail, tokens, graph

Examples:
  python3 fetch_basket_detail.py war-mode
  python3 fetch_basket_detail.py "defense" --include=tokens
  python3 fetch_basket_detail.py made-in-america --include=detail,graph
"""

import json, sys, urllib.request

BASE_URL = "https://backend.cesto.co"
TIMEOUT = 15


def fetch(path):
    try:
        req = urllib.request.Request(f"{BASE_URL}{path}")
        resp = urllib.request.urlopen(req, timeout=TIMEOUT)
        return json.loads(resp.read().decode())
    except Exception:
        return None


def safe_num(val, default=None):
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def find_basket(query):
    """Find basket by slug or fuzzy name match from /products list."""
    products = fetch("/products")
    if not products:
        return None, None

    query_lower = query.lower().strip()

    # Try exact slug match first
    for p in products:
        if p.get("slug", "").lower() == query_lower:
            return p, products

    # Try partial name match
    for p in products:
        if query_lower in p.get("name", "").lower():
            return p, products

    # Try partial slug match
    for p in products:
        if query_lower in p.get("slug", "").lower():
            return p, products

    return None, products


def parse_args():
    slug_or_name = None
    include = {"detail", "tokens", "graph"}

    for arg in sys.argv[1:]:
        if arg.startswith("--include="):
            include = set(arg.split("=", 1)[1].split(","))
        elif not slug_or_name:
            slug_or_name = arg

    return slug_or_name, include


def main():
    slug_or_name, include = parse_args()

    if not slug_or_name:
        print(json.dumps({"error": True, "message": "Please provide a basket slug or name"}))
        sys.exit(1)

    basket_list_item, all_products = find_basket(slug_or_name)

    if not basket_list_item:
        available = [{"name": p.get("name"), "slug": p.get("slug")} for p in (all_products or [])]
        print(json.dumps({
            "error": True,
            "message": f"No basket found matching '{slug_or_name}'",
            "availableBaskets": available
        }))
        sys.exit(1)

    slug = basket_list_item.get("slug", "")
    basket_id = basket_list_item.get("id", "")
    result = {}

    # Fetch detail via /products/{slug}
    if "detail" in include:
        detail = fetch(f"/products/{slug}")
        if detail:
            min_inv_raw = safe_num(detail.get("minimumInvestment"), 0)

            # Parse allocations from definition.nodes
            defn = detail.get("definition") or {}
            nodes = defn.get("nodes", []) if isinstance(defn, dict) else []
            allocations = []
            for node in nodes:
                params = node.get("parameters", {}) or {}
                amount_expr = params.get("amount", "")
                # Extract percentage from "{{ $input.amount * 0.22 }}" pattern
                pct = None
                if isinstance(amount_expr, str) and "*" in amount_expr:
                    try:
                        pct = round(float(amount_expr.split("*")[-1].strip().rstrip("}").strip()) * 100, 2)
                    except (ValueError, IndexError):
                        pass

                allocations.append({
                    "token": node.get("label", ""),
                    "nodeId": node.get("id", ""),
                    "percentage": pct,
                    "description": node.get("description", ""),
                })

            # Performance from detail response
            tp = detail.get("tokenPerformance") or {}
            tp7 = detail.get("tokenPerformance7d") or {}
            tp30 = detail.get("tokenPerformance30d") or {}

            result["basket"] = {
                "id": basket_id,
                "name": detail.get("name", ""),
                "slug": slug,
                "category": detail.get("category", ""),
                "description": detail.get("description", ""),
                "riskLevel": detail.get("riskLevel", ""),
                "minInvestmentUSDC": min_inv_raw / 1_000_000 if min_inv_raw else 0,
                "strategy": defn.get("about", "") if isinstance(defn, dict) else "",
                "allocations": allocations,
                "performance": {
                    "return1y": safe_num(tp.get("avgPercentChange")),
                    "return7d": safe_num(tp7.get("return", tp7.get("avgPercentChange")) if tp7 else None),
                    "return30d": safe_num(tp30.get("return", tp30.get("avgPercentChange")) if tp30 else None),
                    "annualizedReturn": safe_num(tp.get("annualizedReturn")),
                },
            }
        else:
            result["basket"] = None

    # Fetch token analysis via /products/{id}/analyze
    if "tokens" in include and basket_id:
        analyze_data = fetch(f"/products/{basket_id}/analyze")
        if analyze_data and isinstance(analyze_data, dict):
            node_analyses = analyze_data.get("nodeAnalyses", [])
            result["tokens"] = []
            for na in node_analyses:
                md = na.get("marketData") or {}
                tp = md.get("tokenPerformance") or {}
                result["tokens"].append({
                    "nodeId": na.get("id", ""),
                    "inputSymbol": na.get("inputSymbol", ""),
                    "outputSymbol": na.get("outputSymbol", ""),
                    "protocol": na.get("protocol", ""),
                    "currentPrice": safe_num(tp.get("currentPrice")),
                    "priceChange24h": safe_num(tp.get("priceChange24h")),
                    "priceChange7d": safe_num(tp.get("priceChange7d")),
                    "priceChange30d": safe_num(tp.get("priceChange30d")),
                    "priceChange1y": safe_num(tp.get("priceChange1y")),
                })
        else:
            result["tokens"] = None

    # Fetch graph via /products/{id}/graph
    if "graph" in include and basket_id:
        graph_data = fetch(f"/products/{basket_id}/graph")
        if graph_data and isinstance(graph_data, dict):
            series = graph_data.get("timeSeries", [])
            metrics = graph_data.get("metrics") or {}

            if series:
                values = [(s.get("timestamp", ""), s.get("portfolioValue", 0)) for s in series if s.get("portfolioValue") is not None]
                sp500 = [s.get("sp500Value", 0) for s in series if s.get("sp500Value") is not None]

                start_val = values[0][1] if values else 0
                end_val = values[-1][1] if values else 0
                sp_start = sp500[0] if sp500 else 0
                sp_end = sp500[-1] if sp500 else 0

                best = max(values, key=lambda x: x[1]) if values else ("", 0)
                worst = min(values, key=lambda x: x[1]) if values else ("", 0)

                has_liquidations = any(s.get("isLiquidated", False) for s in series)

                result["graph"] = {
                    "startValue": start_val,
                    "endValue": round(end_val, 2),
                    "totalReturn": metrics.get("totalReturn", round((end_val - start_val) / start_val * 100, 2) if start_val else 0),
                    "sp500Return": round((sp_end - sp_start) / sp_start * 100, 2) if sp_start else 0,
                    "volatility": metrics.get("volatility"),
                    "maxDrawdown": metrics.get("maxDrawdown"),
                    "sharpe": metrics.get("sharpe"),
                    "bestDay": {"date": best[0], "value": round(best[1], 2)},
                    "worstDay": {"date": worst[0], "value": round(worst[1], 2)},
                    "hasLiquidations": has_liquidations,
                    "dataPoints": len(series),
                }
            else:
                result["graph"] = None
        else:
            result["graph"] = None

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
