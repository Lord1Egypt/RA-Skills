#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Run offline installation and integrity checks for the installed skill."""

from __future__ import annotations

import hashlib
import json
import sys
from argparse import Namespace
from pathlib import Path
from typing import Any

import init_packet
import query_sources
import validate_packet


SKILL_ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"name": name, "passed": passed, "detail": detail}


def main() -> int:
    checks: list[dict[str, Any]] = []
    checks.append(
        result(
            "python-version",
            sys.version_info >= (3, 11),
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        )
    )

    skill_files = sorted(SKILL_ROOT.rglob("SKILL.md"))
    checks.append(
        result(
            "single-skill-entrypoint",
            skill_files == [SKILL_ROOT / "SKILL.md"],
            ", ".join(str(path.relative_to(SKILL_ROOT)) for path in skill_files),
        )
    )

    required = [
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "LICENSE.txt",
        SKILL_ROOT / "NOTICE.txt",
        SKILL_ROOT / "references" / "papers.jsonl",
        SKILL_ROOT / "references" / "repositories.json",
        SKILL_ROOT / "references" / "source-state.json",
        SKILL_ROOT / "references" / "catalog-snapshot.json",
        SKILL_ROOT / "references" / "routing-rules.json",
        SKILL_ROOT / "references" / "archive-records.json",
        SKILL_ROOT / "references" / "legacy-routing-review.json",
        SKILL_ROOT / "references" / "paper-selection-metadata.json",
        SKILL_ROOT / "references" / "paper-repository-relations.json",
        SKILL_ROOT / "assets" / "intervention-packet.schema.json",
        SKILL_ROOT / "assets" / "intervention-packet.example.json",
    ]
    missing = [str(path.relative_to(SKILL_ROOT)) for path in required if not path.is_file()]
    checks.append(result("required-files", not missing, ", ".join(missing) or "complete"))

    try:
        papers = [
            json.loads(line)
            for line in (SKILL_ROOT / "references" / "papers.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        canonical = [
            record
            for record in papers
            if record.get("record_type") == "canonical_paper"
        ]
        archive_only = [
            record
            for record in papers
            if record.get("record_type") == "archive_only_provenance"
        ]
        paper_ok = (
            len(papers) == 231
            and len(canonical) == 227
            and len(archive_only) == 4
            and len({record.get("doi") for record in canonical}) == 227
        )
        checks.append(
            result(
                "paper-index",
                paper_ok,
                f"canonical={len(canonical)}, archive_only={len(archive_only)}",
            )
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        checks.append(result("paper-index", False, type(exc).__name__))

    try:
        repositories = load_json(
            SKILL_ROOT / "references" / "repositories.json"
        )["repositories"]
        repo_ok = (
            len(repositories) == 53
            and len({record.get("name") for record in repositories}) == 53
            and all(
                isinstance(record.get("head_sha"), str)
                and len(record["head_sha"]) == 40
                for record in repositories
            )
        )
        checks.append(result("repository-index", repo_ok, f"records={len(repositories)}"))
    except (OSError, TypeError, KeyError, ValueError, json.JSONDecodeError) as exc:
        checks.append(result("repository-index", False, type(exc).__name__))

    try:
        state = load_json(SKILL_ROOT / "references" / "source-state.json")
        expected = state["hashes"]
        hash_targets = {
            "derived_papers_jsonl_sha256": "references/papers.jsonl",
            "repositories_json_sha256": "references/repositories.json",
            "catalog_snapshot_sha256": "references/catalog-snapshot.json",
            "routing_rules_sha256": "references/routing-rules.json",
            "legacy_routing_review_sha256": "references/legacy-routing-review.json",
            "archive_records_sha256": "references/archive-records.json",
            "paper_selection_metadata_sha256": "references/paper-selection-metadata.json",
            "paper_repository_relations_sha256": "references/paper-repository-relations.json",
        }
        actual_hashes = {
            key: sha256(SKILL_ROOT / relative)
            for key, relative in hash_targets.items()
        }
        hashes_ok = all(expected.get(key) == value for key, value in actual_hashes.items())
        checks.append(
            result(
                "internal-hashes",
                hashes_ok,
                "; ".join(f"{key}={value}" for key, value in actual_hashes.items()),
            )
        )
        checks.append(
            result(
                "offline-rebuild-index-integrity",
                (
                    expected.get("derived_papers_jsonl_sha256")
                    == actual_hashes["derived_papers_jsonl_sha256"]
                ),
                (
                    "bundled index matches its pinned derivation hash; "
                    "run rebuild_indexes.py --check for full semantic reconstruction"
                ),
            )
        )
    except (OSError, TypeError, KeyError, ValueError, json.JSONDecodeError) as exc:
        checks.append(result("internal-hashes", False, type(exc).__name__))
        checks.append(
            result("offline-rebuild-index-integrity", False, type(exc).__name__)
        )

    repository_license = SKILL_ROOT.parent / "LICENSE"
    if repository_license.is_file():
        license_ok = repository_license.read_bytes() == (
            SKILL_ROOT / "LICENSE.txt"
        ).read_bytes()
        license_detail = "root and bundle licenses match"
    else:
        license_ok = (SKILL_ROOT / "LICENSE.txt").is_file()
        license_detail = "installed skill license is present"
    checks.append(result("license", license_ok, license_detail))

    # Call the bundled pure-Python APIs in-process. This checks the same offline
    # paths as their CLIs without paying five interpreter-startup costs.
    try:
        schema = load_json(
            SKILL_ROOT / "assets" / "intervention-packet.schema.json"
        )
        example = load_json(
            SKILL_ROOT / "assets" / "intervention-packet.example.json"
        )
        example_errors = validate_packet.SchemaValidator(schema).validate(example)
        checks.append(
            result(
                "packet-example",
                not example_errors,
                "schema-valid" if not example_errors else f"errors={len(example_errors)}",
            )
        )
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        checks.append(result("packet-example", False, type(exc).__name__))

    try:
        search_records = [
            *[("paper", record) for record in query_sources.load_papers()],
            *[("repo", record) for record in query_sources.load_repositories()],
        ]
        search_results = query_sources.execute_search(
            search_records,
            "verification provenance",
            "all",
            False,
        )
        checks.append(
            result(
                "offline-search",
                bool(search_results),
                f"examined={len(search_records)}, matched={len(search_results)}",
            )
        )
    except (OSError, TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        checks.append(result("offline-search", False, type(exc).__name__))

    try:
        initialized = init_packet.packet(
            Namespace(
                objective="Doctor fail-closed packet check.",
                workspace=".",
                evaluation_horizon="Not yet declared.",
            )
        )
        initialization_errors = validate_packet.SchemaValidator(schema).validate(
            initialized
        )
        checks.append(
            result(
                "fail-closed-packet-initialization",
                not initialization_errors,
                (
                    "initialized and validated"
                    if not initialization_errors
                    else f"errors={len(initialization_errors)}"
                ),
            )
        )
    except (NameError, OSError, TypeError, ValueError, KeyError) as exc:
        checks.append(
            result("fail-closed-packet-initialization", False, type(exc).__name__)
        )

    ok = all(check["passed"] for check in checks)
    json.dump(
        {
            "ok": ok,
            "skill_root": ".",
            "python_version": (
                f"{sys.version_info.major}.{sys.version_info.minor}."
                f"{sys.version_info.micro}"
            ),
            "checks": checks,
        },
        sys.stdout,
        ensure_ascii=True,
        sort_keys=True,
    )
    sys.stdout.write("\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
