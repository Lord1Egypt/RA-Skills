"""Read reusable results from an explicitly supplied verifier artifact."""

from __future__ import annotations

import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from verifier_models import AuditResult, CanonicalRecord

AUDIT_SCHEMA = "biomedical-reference-verifier.audit.v1"
INDEX_SCHEMA = "biomedical-reference-verifier.index.v1"


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _norm(value: Any) -> str:
    return re.sub(r"[\W_]+", " ", str(value or "").casefold()).strip()


def _result_keys(row: dict[str, Any]) -> list[str]:
    original = str(row.get("original") or "").strip()
    title = _norm(row.get("parsed_title"))
    year = str(row.get("parsed_year") or "").strip()
    doi = str(row.get("parsed_doi") or "").lower().strip().removeprefix("https://doi.org/")
    authors = row.get("parsed_authors") or []
    first_author = _norm(authors[0] if isinstance(authors, list) and authors else "")
    journal = _norm(row.get("parsed_journal"))
    keys = [f"exact:{original}", f"text:{_norm(original)}"] if original else []
    if doi and title and year:
        keys.append(f"doi:{doi}|{title}|{year}")
    if title and first_author and year and journal:
        keys.append(f"meta:{title}|{first_author}|{year}|{journal}")
    return keys


def prior_result_for_entry(rows: dict[str, dict[str, Any]], entry: Any) -> dict[str, Any] | None:
    probe = {
        "original": entry.original,
        "parsed_title": entry.title,
        "parsed_year": entry.year,
        "parsed_doi": entry.doi,
        "parsed_authors": entry.authors,
        "parsed_journal": entry.journal,
    }
    for key in _result_keys(probe):
        if key in rows:
            row = rows[key]
            saved = row.get("source_fields")
            if not isinstance(saved, dict):
                continue
            fields = ("title", "authors", "year", "journal", "doi", "pmid", "volume", "issue", "pages", "article_number", "urls")
            if all(_norm(saved.get(field)) == _norm(getattr(entry, field)) for field in fields):
                return row
    return None


def audit_to_index(payload: dict[str, Any], warnings: list[str] | None = None) -> dict[str, Any]:
    rows = payload.get("results", [])
    if not isinstance(rows, list):
        raise ValueError("Audit artifact must contain a results list")
    valid_rows = [row for row in rows if isinstance(row, dict) and str(row.get("original") or "").strip()]
    if warnings is not None and len(valid_rows) != len(rows):
        warnings.append(f"Skipped {len(rows) - len(valid_rows)} invalid audit result row(s).")
    return {
        "schema": INDEX_SCHEMA,
        "audit_metadata": {k: v for k, v in payload.items() if k != "results"},
        "entries": [
            {
                "key": str(row.get("original") or "").strip(),
                "result": row,
            }
            for row in valid_rows
        ],
    }


def index_to_audit(payload: dict[str, Any], warnings: list[str] | None = None) -> dict[str, Any]:
    if payload.get("schema") != INDEX_SCHEMA:
        raise ValueError(f"Expected schema {INDEX_SCHEMA}")
    metadata = payload.get("audit_metadata") or {}
    if not isinstance(metadata, dict):
        raise ValueError("Index audit_metadata must be an object")
    entries = payload.get("entries") or []
    if not isinstance(entries, list):
        raise ValueError("Index entries must be a list")
    valid = [entry["result"] for entry in entries if isinstance(entry, dict) and isinstance(entry.get("result"), dict)]
    if warnings is not None and len(valid) != len(entries):
        warnings.append(f"Skipped {len(entries) - len(valid)} invalid index entry or result(s).")
    audit = dict(metadata)
    audit["results"] = valid
    return audit


def normalize_artifact(payload: dict[str, Any]) -> dict[str, Any]:
    return index_to_audit(payload) if payload.get("schema") == INDEX_SCHEMA else payload


def load_prior_results(path: str, warnings: list[str] | None = None, *, pipeline: str | None = None, mode: str = "balanced", channels: list[str] | None = None, policy_version: str | None = None) -> dict[str, dict[str, Any]]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read prior artifact: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Prior artifact must be a JSON object")
    payload = index_to_audit(payload, warnings) if payload.get("schema") == INDEX_SCHEMA else payload
    rows = payload.get("results", [])
    if not isinstance(rows, list):
        raise ValueError("Prior artifact results must be a list")
    reusable = {}
    skipped = 0
    for row in rows:
        if not isinstance(row, dict):
            skipped += 1
            continue
        original = str(row.get("original") or "").strip()
        status = str(row.get("status") or "")
        valid = isinstance(row.get("canonical"), dict) and isinstance(row.get("source_fields"), dict)
        if valid:
            canonical = row["canonical"]
            valid = isinstance(canonical.get("source"), str) and isinstance(canonical.get("title"), str) and bool(canonical.get("title"))
            valid = valid and isinstance(canonical.get("authors"), list) and all(isinstance(a, str) for a in canonical.get("authors", []))
            valid = valid and all(isinstance(canonical.get(f, ""), str) for f in ("year", "doi", "pmid", "journal", "volume", "issue", "pages"))
        valid = valid and status in {"verified", "minor_fix", "formatted_only"}
        valid = valid and (pipeline is None or row.get("pipeline") == pipeline)
        valid = valid and (policy_version is None or row.get("policy_version") == policy_version)
        if pipeline == "verify":
            ranks = {"fast": 0, "balanced": 1, "strict": 2}
            valid = valid and ranks.get(row.get("check_mode"), -1) >= ranks[mode]
            valid = valid and set(channels or []).issubset(row.get("check_channels") or [])
        try:
            age = (datetime.now(timezone.utc) - datetime.fromisoformat(row.get("checked_at", ""))).total_seconds()
            valid = valid and 0 <= age <= 30 * 86400
        except (ValueError, TypeError):
            valid = False
        if not valid:
            skipped += 1
            continue
        if original and status:
            for key in _result_keys(row):
                reusable[key] = row
        else:
            skipped += 1
    if warnings is not None and skipped:
        warnings.append(f"Ignored {skipped} incomplete prior result row(s); those references will be checked again.")
    return reusable


def audit_result_from_dict(row: dict[str, Any]) -> AuditResult:
    data = dict(row)
    for key in ("canonical", "identifier_record"):
        value = data.get(key)
        if isinstance(value, dict):
            data[key] = CanonicalRecord(**{k: v for k, v in value.items() if k in CanonicalRecord.__dataclass_fields__})
        elif value is not None:
            data[key] = None
    allowed = AuditResult.__dataclass_fields__
    return AuditResult(**{k: v for k, v in data.items() if k in allowed})
