#!/usr/bin/env python3
"""Validate a content plan's structure and references to supplied facts."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


class PlanError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PlanError(f"cannot read JSON file {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise PlanError(f"{path} must contain a JSON object")
    return data


def nonempty(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PlanError(f"{where} must be a non-empty string")
    return value.strip()


def validate(facts_doc: dict[str, Any], plan: dict[str, Any]) -> None:
    facts = facts_doc.get("facts")
    if not isinstance(facts, list):
        raise PlanError("facts.facts must be a list")
    index: dict[str, dict[str, Any]] = {}
    for i, fact in enumerate(facts):
        if not isinstance(fact, dict):
            raise PlanError(f"facts.facts[{i}] must be an object")
        fid = nonempty(fact.get("id"), f"facts.facts[{i}].id")
        nonempty(fact.get("claim"), f"facts.facts[{i}].claim")
        status = fact.get("status")
        if not isinstance(status, str) or status not in {"verified", "unverified"}:
            raise PlanError(f"facts.facts[{i}].status must be verified or unverified")
        if status == "verified":
            nonempty(fact.get("source"), f"facts.facts[{i}].source")
        if fid in index:
            raise PlanError(f"duplicate fact id: {fid}")
        index[fid] = fact

    for key in ("audience", "keyword", "promise", "hook", "title_direction", "share_motivation"):
        nonempty(plan.get(key), f"plan.{key}")
    opening = plan.get("opening_evidence")
    if not isinstance(opening, dict):
        raise PlanError("plan.opening_evidence must be an object")
    seconds = opening.get("seconds")
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not 0 <= seconds <= 12:
        raise PlanError("plan.opening_evidence.seconds must be between 0 and 12")
    nonempty(opening.get("beat"), "plan.opening_evidence.beat")
    beats = plan.get("beats")
    if not isinstance(beats, list) or not beats:
        raise PlanError("plan.beats must be a non-empty list")
    if plan.get("cta") is not None and (not isinstance(plan["cta"], str) or not plan["cta"].strip()):
        raise PlanError("plan.cta must be null or a non-empty string")
    unknowns = plan.get("unknowns")
    if not isinstance(unknowns, list) or any(not isinstance(x, str) or not x.strip() for x in unknowns):
        raise PlanError("plan.unknowns must be a list of non-empty strings")

    for label, item in [("opening_evidence", opening), *[(f"beats[{i}]", b) for i, b in enumerate(beats)]]:
        if label.startswith("beats["):
            if not isinstance(item, dict):
                raise PlanError(f"plan.{label} must be an object")
            order = item.get("order")
            if isinstance(order, bool) or not isinstance(order, int) or order < 1:
                raise PlanError(f"plan.{label}.order must be a positive integer")
            nonempty(item.get("text"), f"plan.{label}.text")
        refs = item.get("fact_ids")
        if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref.strip() for ref in refs):
            raise PlanError(f"plan.{label}.fact_ids must be a list of non-empty strings")
        for ref in refs:
            fact = index.get(ref)
            if fact is None:
                raise PlanError(f"plan.{label} references unknown fact id {ref!r}")
            if fact["status"] != "verified":
                raise PlanError(f"plan.{label} references unverified fact id {ref!r}")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: validate_plan.py FACTS.json PLAN.json", file=sys.stderr)
        return 2
    try:
        validate(load_json(Path(argv[1])), load_json(Path(argv[2])))
    except PlanError as exc:
        print(f"invalid: {exc}", file=sys.stderr)
        return 1
    print("valid: structure and verified fact references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
