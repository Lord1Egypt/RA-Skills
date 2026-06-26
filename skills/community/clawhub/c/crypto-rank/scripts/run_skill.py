#!/usr/bin/env python3
"""ClawHub wrapper for the bundled CryptoRank demo client."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
BUNDLED_SCRIPT = SKILL_ROOT / "assets" / "cryptorank_demo.py"
SUPPORT_LINKS = {
    "community": "https://t.me/hollyink",
    "bot": "https://t.me/yongzhuan_bot",
    "tutorial": "https://www.youtube.com/@0xcii",
}


def load_bundle():
    spec = importlib.util.spec_from_file_location("cryptorank_demo_bundle", BUNDLED_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load bundled client: {BUNDLED_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def with_support_footer(module, text: str, output: str, mode: str, lang: str) -> str:
    if mode == "raw" or output == "json":
        return text
    footer_builder = getattr(module, "support_footer", None)
    if callable(footer_builder):
        return f"{text}\n{footer_builder(lang)}"
    lines = [
        "",
        "如果你在安装、调用或使用中遇到问题，可继续：" if lang == "zh" else "If you run into setup, call, or usage issues, continue here:",
        f"- {'社区排障' if lang == 'zh' else 'Community'}: {SUPPORT_LINKS['community']}",
        f"- {'机器人版本' if lang == 'zh' else 'Bot'}: {SUPPORT_LINKS['bot']}",
        f"- {'视频教程' if lang == 'zh' else 'Tutorial'}: {SUPPORT_LINKS['tutorial']}",
    ]
    return f"{text}\n" + "\n".join(lines)


def normalize_output(module, text: str, output: str, mode: str, limit: int, lang: str, raw_mode: str | None) -> str:
    text = with_support_footer(module, text, output, mode, lang)
    if output == "text":
        return text

    if output == "markdown":
        title = f"# CryptoRank {mode} output"
        if lang == "zh":
            title = f"# CryptoRank {mode} 输出"
        return f"{title}\n\n```text\n{text}\n```"

    payload: dict[str, Any] = {
        "skill": "cryptorank-radar",
        "mode": mode,
        "limit": limit,
        "lang": lang,
        "output": output,
        "source": "free-layer",
        "support_links": SUPPORT_LINKS,
    }
    if raw_mode:
        payload["raw_mode"] = raw_mode
    if mode == "raw":
        payload["data"] = json.loads(text)
    else:
        payload["text"] = text
    return json.dumps(payload, ensure_ascii=False, indent=2)


def build_structured_payload(module, client, mode: str, limit: int, raw_mode: str, lang: str) -> dict[str, Any]:
    if mode == "raw":
        return {
            "mode": mode,
            "raw_mode": raw_mode,
            "data": json.loads(module.json_dump(client, raw_mode, limit)),
        }

    if mode == "radar":
        home = client.homepage()
        top = (home.get("fallbackCoins") or [])[:limit]
        gainers = (home.get("gainersCoins") or [])[:limit]
        losers = (home.get("losersCoins") or [])[:limit]
        funding = (home.get("fallbackRecentFundingRounds") or [])[:limit]
        upcoming = (home.get("upcomingIco") or [])[:limit]
        return {
            "mode": mode,
            "top_coins": [
                {
                    "name": item.get("name"),
                    "symbol": item.get("symbol"),
                    "price": module.money(module.usd_value(item.get("price"))),
                    "market_cap": module.money(module.usd_value(item.get("marketCap"))),
                    "links": module.build_links(("CryptoRank", module.build_price_url(item.get("key")))),
                }
                for item in top
            ],
            "gainers": [
                {
                    "name": item.get("name"),
                    "symbol": item.get("symbol"),
                    "category": module.translate_value(item.get("category"), lang),
                    "change_24h": module.pct(item.get("historyPrice", {}).get("24H")),
                    "links": module.build_links(("CryptoRank", module.build_price_url(item.get("key")))),
                }
                for item in gainers
            ],
            "losers": [
                {
                    "name": item.get("name"),
                    "symbol": item.get("symbol"),
                    "category": module.translate_value(item.get("category"), lang),
                    "change_24h": module.pct(item.get("historyPrice", {}).get("24H")),
                    "links": module.build_links(("CryptoRank", module.build_price_url(item.get("key")))),
                }
                for item in losers
            ],
            "upcoming": [
                {
                    "project": item.get("coin", {}).get("name"),
                    "symbol": item.get("coin", {}).get("symbol"),
                    "date": module.relative_date(item.get("date"), lang),
                    "raise": module.money(item.get("raise")),
                    "links": module.build_links(
                        ("CryptoRank", module.build_price_url(item.get("coin", {}).get("key"))),
                        ("Sale", module.build_funding_url(item.get("coin", {}).get("key"))),
                    ),
                }
                for item in upcoming
            ],
            "funding": [
                {
                    "project": item.get("coin", {}).get("name"),
                    "stage": module.translate_value(item.get("type"), lang),
                    "raise": module.money(item.get("raise")),
                    "funds": module.join_names(item.get("funds"), lang=lang),
                    "links": module.build_links(
                        ("CryptoRank", module.build_price_url(item.get("coin", {}).get("key"))),
                        ("Funding", module.build_funding_url(item.get("coin", {}).get("key"))),
                    ),
                }
                for item in funding
            ],
        }

    if mode == "funding":
        home = client.homepage()
        rounds = (home.get("fallbackRecentFundingRounds") or [])[:limit]
        return {
            "mode": mode,
            "items": [
                {
                    "project": item.get("coin", {}).get("name") or item.get("fund", {}).get("name"),
                    "stage": module.translate_value(item.get("type"), lang),
                    "raise": module.money(item.get("raise")),
                    "date": module.relative_date(item.get("date"), lang),
                    "funds": module.join_names(item.get("funds"), lang=lang),
                    "links": module.build_links(
                        ("CryptoRank", module.build_price_url(item.get("coin", {}).get("key"))),
                        ("Funding", module.build_funding_url(item.get("coin", {}).get("key"))),
                    ),
                }
                for item in rounds
            ],
        }

    if mode == "upcoming":
        page = client.upcoming_page()
        items = (page.get("fallbackRounds", {}).get("data") or [])[:limit]
        return {
            "mode": mode,
            "items": [
                {
                    "project": item.get("name"),
                    "symbol": item.get("symbol"),
                    "sale_type": [module.translate_value(v, lang) for v in item.get("type", [])],
                    "launchpads": module.join_names(item.get("launchpads"), limit=2, lang=lang),
                    "date": module.relative_date(item.get("when"), lang),
                    "links": module.build_links(
                        ("CryptoRank", module.build_price_url(item.get("key"))),
                        ("Sale", module.build_funding_url(item.get("key"))),
                        ("Launchpad", module.build_price_url((item.get("launchpads") or [{}])[0].get("key") if item.get("launchpads") else None)),
                    ),
                }
                for item in items
            ],
        }

    if mode == "airdrops":
        payload = client.airdrops(limit)
        items = (payload.get("data") or [])[:limit]
        return {
            "mode": mode,
            "items": [
                {
                    "project": item.get("coin", {}).get("name"),
                    "symbol": item.get("coin", {}).get("symbol"),
                    "rating": module.compact_number(item.get("rating")),
                    "status": module.translate_value(item.get("status"), lang),
                    "activity_types": module.join_names(item.get("activityTypes"), field="name", limit=2, lang=lang),
                    "links": module.build_links(
                        ("CryptoRank", module.build_price_url(item.get("coin", {}).get("key"))),
                        ("Task", item.get("checkLink")),
                        ("Claim", item.get("linkToClaim")),
                    ),
                }
                for item in items
            ],
        }

    if mode == "brief":
        return {
            "mode": mode,
            "summary": module.daily_brief(client, limit),
            "sections": {
                "funding": build_structured_payload(module, client, "funding", min(limit, 3), raw_mode, lang)["items"],
                "upcoming": build_structured_payload(module, client, "upcoming", min(limit, 3), raw_mode, lang)["items"],
                "airdrops": build_structured_payload(module, client, "airdrops", min(limit, 3), raw_mode, lang)["items"],
            },
        }

    return {"mode": mode}


def execute(
    mode: str = "radar",
    limit: int = 5,
    lang: str = "zh",
    output: str = "json",
    raw_mode: str = "home",
) -> str:
    module = load_bundle()
    module.OUTPUT_LANG = lang
    client = module.CryptoRankClient(lang=lang)

    renderers = {
        "radar": module.homepage_radar,
        "funding": module.funding_radar,
        "upcoming": module.upcoming_radar,
        "airdrops": module.airdrop_radar,
        "brief": module.daily_brief,
    }

    if mode == "raw":
        text = module.json_dump(client, raw_mode, limit)
        if output == "json":
          payload = {
              "skill": "cryptorank-radar",
              "limit": limit,
              "lang": lang,
              "output": output,
              "source": "free-layer",
              "support_links": SUPPORT_LINKS,
              **build_structured_payload(module, client, mode, limit, raw_mode, lang),
          }
          return json.dumps(payload, ensure_ascii=False, indent=2)
        return normalize_output(module, text, output, mode, limit, lang, raw_mode)

    if mode not in renderers:
        raise RuntimeError(f"Unsupported mode: {mode}")

    text = renderers[mode](client, limit)
    if output == "json":
        payload = {
            "skill": "cryptorank-radar",
            "limit": limit,
            "lang": lang,
            "output": output,
            "source": "free-layer",
            "support_links": SUPPORT_LINKS,
            "text": text,
            **build_structured_payload(module, client, mode, limit, raw_mode, lang),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
    return normalize_output(module, text, output, mode, limit, lang, None)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CryptoRank ClawHub skill wrapper")
    parser.add_argument("--mode", choices=["radar", "funding", "upcoming", "airdrops", "brief", "raw"], default="radar")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--lang", choices=["zh", "en"], default=os.environ.get("CRYPTORANK_LANG", "zh"))
    parser.add_argument("--output", choices=["text", "json", "markdown"], default="json")
    parser.add_argument("--raw-mode", choices=["home", "funding", "upcoming", "airdrops"], default="home")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = execute(
            mode=args.mode,
            limit=args.limit,
            lang=args.lang,
            output=args.output,
            raw_mode=args.raw_mode,
        )
    except Exception as exc:  # pragma: no cover - runtime wrapper
        print(
            json.dumps(
                {
                    "skill": "cryptorank-radar",
                    "error": str(exc),
                    "mode": args.mode,
                    "lang": args.lang,
                    "support_links": SUPPORT_LINKS,
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
