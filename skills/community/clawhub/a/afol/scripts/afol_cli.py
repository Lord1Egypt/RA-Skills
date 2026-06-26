#!/usr/bin/env python3
"""Deterministic router for the AFOL meta skill."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Provider:
    name: str
    env_vars: tuple[str, ...]
    optional_env_vars: tuple[str, ...] = ()


PROVIDERS: tuple[Provider, ...] = (
    Provider("rebrickable", ("REBRICKABLE_API_KEY",), ("REBRICKABLE_USER_TOKEN",)),
    Provider("brickset", ("BRICKSET_API_KEY",), ("BRICKSET_USER_HASH", "BRICKSET_USERNAME", "BRICKSET_PASSWORD")),
    Provider("bricklink", ("BRICKLINK_API_CONSUMER_KEY", "BRICKLINK_API_CONSUMER_SECRET", "BRICKLINK_API_TOKEN_VALUE", "BRICKLINK_API_TOKEN_SECRET")),
    Provider("brickowl", ("BRICKOWL_API_KEY",)),
    Provider("brickeconomy", ("BRICKECONOMY_API_KEY",)),
)

KEYWORDS: tuple[tuple[tuple[str, ...], tuple[str, ...], str], ...] = (
    (("worth", "value", "valuation", "forecast", "roi", "growth", "investment", "sales ledger", "portfolio"), ("brickeconomy", "bricklink"), "valuation/forecasting workflow"),
    (("price", "pricing", "price guide", "market", "buy", "sell", "order", "inventory", "listing", "feedback", "coupon", "store"), ("bricklink", "brickowl"), "marketplace workflow"),
    (("brickowl",), ("brickowl",), "BrickOwl-specific workflow"),
    (("bricklink",), ("bricklink",), "BrickLink-specific workflow"),
    (("instruction", "instructions", "review", "reviews", "image", "images", "rating", "owned", "wanted", "brickset"), ("brickset", "rebrickable"), "Brickset metadata/collection workflow"),
    (("part", "parts", "inventory", "element", "color", "theme", "build", "buildable", "lost", "minifig", "set", "catalog", "rebrickable"), ("rebrickable", "brickset"), "catalog/identity workflow"),
)


def provider_ready(provider: Provider) -> bool:
    return all(os.environ.get(name) for name in provider.env_vars)


def credentials() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for provider in PROVIDERS:
        missing_required = [name for name in provider.env_vars if not os.environ.get(name)]
        optional_set = [name for name in provider.optional_env_vars if os.environ.get(name)]
        rows.append(
            {
                "provider": provider.name,
                "ready": not missing_required,
                "missing_required": missing_required,
                "optional_set": optional_set,
            }
        )
    return rows


def route(task: str) -> dict[str, object]:
    normalized = task.lower()
    selected: tuple[str, ...] = ("rebrickable", "brickset")
    reason = "default catalog/identity workflow"

    for keywords, providers, keyword_reason in KEYWORDS:
        if any(keyword in normalized for keyword in keywords):
            selected = providers
            reason = keyword_reason
            break

    return {
        "task": task,
        "reason": reason,
        "providers": list(selected),
        "load_skills": list(selected),
        "notes": notes_for(selected),
    }


def notes_for(providers: Iterable[str]) -> list[str]:
    provider_set = set(providers)
    notes: list[str] = ["Read-only by default; writes require explicit user intent and provider --yes/dry-run guards."]
    if "brickeconomy" in provider_set:
        notes.append("Use BrickEconomy for set/minifig value, forecasts, growth, ROI, collection valuation, and sales-ledger analysis.")
    if "bricklink" in provider_set or "brickowl" in provider_set:
        notes.append("Resolve item identity, color, condition, quantity, and currency before comparing marketplace prices.")
    if "rebrickable" in provider_set:
        notes.append("Use Rebrickable as the catalog backbone for set, part, minifig, element, color, and inventory lookup.")
    if "brickset" in provider_set:
        notes.append("Use Brickset for rich set metadata, images, instructions, reviews, and owned/wanted context.")
    return notes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Route AFOL collector tasks to provider skills.")
    sub = parser.add_subparsers(dest="command", required=True)

    route_parser = sub.add_parser("route", help="Suggest provider skills for a user task")
    route_parser.add_argument("task", nargs="+", help="User task text")

    sub.add_parser("credentials", help="Report provider credential readiness without values")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "route":
        print(json.dumps(route(" ".join(args.task)), indent=2, sort_keys=True))
        return 0
    if args.command == "credentials":
        print(json.dumps(credentials(), indent=2, sort_keys=True))
        return 0
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
