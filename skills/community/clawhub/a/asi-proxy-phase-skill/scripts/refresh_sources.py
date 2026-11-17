#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Check public source drift and optionally refresh factual metadata."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES_DIR = SKILL_ROOT / "references"
REPOSITORIES_PATH = REFERENCES_DIR / "repositories.json"
PAPERS_PATH = REFERENCES_DIR / "papers.jsonl"
SOURCE_STATE_PATH = REFERENCES_DIR / "source-state.json"
GITHUB_REPOS_URL = (
    "https://api.github.com/users/kadubon/repos"
    "?type=public&sort=full_name&direction=asc&per_page=100&page={page}"
)
HF_CATALOG_URL = (
    "https://huggingface.co/datasets/kadubon/paper-tex-corpus/"
    "resolve/v1.0.0/metadata/research-catalog.json"
)
USER_AGENT = "kadubon-asi-proxy-phase-skill-refresh/1.1"
DERIVATIVE_EXCLUSIONS = {
    "asi-proxy-phase-skill": (
        "This repository is the derived skill itself, not an upstream research source."
    )
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare the bundled source snapshot with kadubon's public GitHub repository "
            "listing and the public v1.0.0 Hugging Face paper catalog."
        ),
        epilog=(
            "--check is the default and never writes files. It exits 1 when drift is found. "
            "--write updates factual metadata only, preserves semantic annotations, and marks "
            "affected records needs_review. GITHUB_TOKEN or GH_TOKEN may raise the rate limit; "
            "the command still calls only the type=public user endpoint and never prints a token."
        ),
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="Read-only drift check (default).",
    )
    mode.add_argument(
        "--write",
        action="store_true",
        help="Write factual public metadata and needs_review markers.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-request timeout in seconds (default: 30).",
    )
    parser.add_argument("--pretty", action="store_true", help="Indent JSON output.")
    return parser.parse_args()


def emit(payload: Any, *, pretty: bool = False) -> None:
    json.dump(
        payload,
        sys.stdout,
        ensure_ascii=True,
        indent=2 if pretty else None,
        sort_keys=True,
    )
    sys.stdout.write("\n")


def diagnostic(message: str) -> None:
    print(f"refresh_sources: {message}", file=sys.stderr)


def fetch_json(url: str, timeout: float) -> Any:
    headers = {
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if url.startswith("https://api.github.com/"):
        headers["X-GitHub-Api-Version"] = "2022-11-28"
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        url,
        headers=headers,
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        final_url = response.geturl()
        if url.startswith("https://api.github.com/"):
            if not final_url.startswith(
                (
                    "https://api.github.com/users/kadubon/repos",
                    "https://api.github.com/repos/kadubon/",
                )
            ):
                raise ValueError(f"unexpected GitHub redirect target: {final_url}")
        elif not final_url.startswith(
            (
                "https://huggingface.co/datasets/kadubon/paper-tex-corpus/",
                "https://huggingface.co/api/resolve-cache/datasets/"
                "kadubon/paper-tex-corpus/",
            )
        ):
            raise ValueError(f"unexpected catalog redirect target: {final_url}")
        return json.loads(response.read().decode("utf-8"))


def fetch_public_repositories(timeout: float) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for page in range(1, 101):
        payload = fetch_json(GITHUB_REPOS_URL.format(page=page), timeout)
        if not isinstance(payload, list):
            raise ValueError("GitHub public user endpoint did not return an array")
        if not payload:
            break
        for record in payload:
            if not isinstance(record, dict):
                raise ValueError("GitHub repository entry is not an object")
            if record.get("private") is not False:
                raise ValueError("GitHub response contains a non-public repository entry")
            if record.get("owner", {}).get("login", "").casefold() != "kadubon":
                raise ValueError("GitHub response contains a repository owned by another user")
            records.append(record)
        if len(payload) < 100:
            break
    else:
        raise ValueError("GitHub repository pagination exceeded the safety limit")
    names = [str(record.get("name", "")) for record in records]
    if any(not name for name in names) or len(names) != len(set(name.casefold() for name in names)):
        raise ValueError("GitHub public repository names are missing or duplicated")
    return records


def fetch_repository_head(record: dict[str, Any], timeout: float) -> str:
    name = urllib.parse.quote(str(record["name"]), safe="")
    branch = urllib.parse.quote(str(record["default_branch"]), safe="")
    payload = fetch_json(
        f"https://api.github.com/repos/kadubon/{name}/commits/{branch}",
        timeout,
    )
    sha = payload.get("sha") if isinstance(payload, dict) else None
    if not isinstance(sha, str) or re.fullmatch(r"[0-9a-f]{40}", sha) is None:
        raise ValueError(f"GitHub did not return a valid HEAD SHA for {record['name']}")
    return sha


def upstream_repositories(
    records: list[dict[str, Any]], timeout: float
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    upstream: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []
    for record in records:
        name = str(record["name"])
        reason = DERIVATIVE_EXCLUSIONS.get(name.casefold())
        if reason:
            excluded.append({"name": name, "reason": reason})
            continue
        observed = dict(record)
        observed["_observed_head_sha"] = fetch_repository_head(record, timeout)
        upstream.append(observed)
    return upstream, excluded


def fetch_public_catalog(timeout: float) -> dict[str, Any]:
    payload = fetch_json(HF_CATALOG_URL, timeout)
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise ValueError("Hugging Face catalog has no records array")
    if payload.get("record_count") != len(payload["records"]):
        raise ValueError("Hugging Face catalog record_count does not match its records")
    return payload


def read_repositories() -> tuple[Any, list[dict[str, Any]]]:
    payload = json.loads(REPOSITORIES_PATH.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        records = payload.get("repositories", payload.get("records"))
    else:
        records = payload
    if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
        raise ValueError(
            "repositories.json must be an array or contain a repositories array"
        )
    return payload, records


def read_papers() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(
        PAPERS_PATH.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"papers.jsonl:{line_number}: expected object")
        records.append(value)
    return records


def read_source_state() -> dict[str, Any]:
    if not SOURCE_STATE_PATH.is_file():
        return {}
    payload = json.loads(SOURCE_STATE_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("source-state.json must contain an object")
    return payload


def excluded_catalog_dois(source_state: dict[str, Any]) -> set[str]:
    selection = source_state.get("paper_selection", {})
    if not isinstance(selection, dict):
        return set()
    values = selection.get("catalog_records_not_in_papers_config", [])
    if not isinstance(values, list):
        return set()
    return {
        str(item["doi"]).casefold()
        for item in values
        if isinstance(item, dict) and isinstance(item.get("doi"), str)
    }


def repo_name(record: dict[str, Any]) -> str:
    value = record.get("name") or record.get("full_name") or record.get("repository_id")
    text = str(value or "")
    return text.split("/", 1)[-1]


def canonical_digest(value: Any) -> str:
    data = json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    )
    data = (data + "\n").encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def public_repo_metadata(record: dict[str, Any]) -> dict[str, Any]:
    license_value = record.get("license")
    if isinstance(license_value, dict):
        license_spdx = license_value.get("spdx_id")
    else:
        license_spdx = None
    if isinstance(license_spdx, str) and license_spdx.casefold() in {
        "none",
        "noassertion",
    }:
        license_spdx = None
    return {
        "name": record.get("name"),
        "full_name": record.get("full_name"),
        "url": record.get("html_url"),
        "default_branch": record.get("default_branch"),
        "description": record.get("description"),
        "language": record.get("language"),
        "license_spdx": license_spdx,
        "fork": record.get("fork"),
        "archived": record.get("archived"),
        "disabled": record.get("disabled"),
        "created_at": record.get("created_at"),
        "updated_at": record.get("updated_at"),
        "pushed_at": record.get("pushed_at"),
        "visibility": record.get("visibility", "public"),
    }


def repo_field(record: dict[str, Any], field: str) -> Any:
    aliases = {
        "url": ("url", "html_url"),
        "license_spdx": (
            "license_spdx",
            "license",
            "license_spdx_id",
            "license_observation",
        ),
    }
    for key in aliases.get(field, (field,)):
        if key in record:
            value = record[key]
            if field == "license_spdx" and isinstance(value, dict):
                return value.get("api_spdx") or value.get("spdx_id")
            if field == "license_spdx" and isinstance(value, str):
                if value.casefold() in {
                    "no license file detected",
                    "none",
                    "noassertion",
                }:
                    return None
            return value
    return None


def compare_repositories(
    local: list[dict[str, Any]], remote: list[dict[str, Any]]
) -> dict[str, Any]:
    local_by_name = {repo_name(record).casefold(): record for record in local}
    remote_by_name = {str(record["name"]).casefold(): record for record in remote}
    added = sorted(set(remote_by_name) - set(local_by_name))
    not_listed = sorted(set(local_by_name) - set(remote_by_name))
    changed: list[dict[str, Any]] = []
    for key in sorted(set(local_by_name) & set(remote_by_name)):
        local_record = local_by_name[key]
        public = public_repo_metadata(remote_by_name[key])
        fields: dict[str, dict[str, Any]] = {}
        observed_head = remote_by_name[key].get("_observed_head_sha")
        if (
            isinstance(observed_head, str)
            and local_record.get("head_sha") != observed_head
        ):
            fields["head_sha"] = {
                "local": local_record.get("head_sha"),
                "public": observed_head,
            }
        for field, remote_value in public.items():
            aliases = {
                "url": ("url", "html_url"),
                "license_spdx": (
                    "license_spdx",
                    "license",
                    "license_spdx_id",
                    "license_observation",
                ),
            }
            if not any(
                candidate in local_record
                for candidate in aliases.get(field, (field,))
            ):
                continue
            local_value = repo_field(local_record, field)
            if local_value != remote_value:
                fields[field] = {"local": local_value, "public": remote_value}
        if fields:
            changed.append(
                {
                    "name": str(remote_by_name[key]["name"]),
                    "fields": fields,
                    "pinned_head_sha": local_record.get("head_sha"),
                    "head_refresh_required": "head_sha" in fields,
                }
            )
    return {
        "added": [remote_by_name[name]["name"] for name in added],
        "not_listed": [repo_name(local_by_name[name]) for name in not_listed],
        "changed": changed,
    }


def compare_papers(
    local: list[dict[str, Any]],
    catalog: dict[str, Any],
    digest: str,
    excluded_dois: set[str],
) -> dict[str, Any]:
    local_by_doi = {
        str(record["doi"]).casefold(): record
        for record in local
        if isinstance(record.get("doi"), str) and record["doi"]
    }
    catalog_by_doi = {
        str(record["doi"]).casefold(): record
        for record in catalog["records"]
        if isinstance(record, dict) and isinstance(record.get("doi"), str)
    }
    added = sorted(set(catalog_by_doi) - set(local_by_doi) - excluded_dois)
    not_listed = sorted(set(local_by_doi) - set(catalog_by_doi))
    changed: list[dict[str, Any]] = []
    fields_to_compare = (
        "title",
        "date_published",
        "canonical_url",
        "authors",
        "abstract",
        "keywords",
    )
    for doi in sorted(set(local_by_doi) & set(catalog_by_doi)):
        fields = {
            field: {
                "local": local_by_doi[doi].get(field),
                "public": catalog_by_doi[doi].get(field),
            }
            for field in fields_to_compare
            if field in local_by_doi[doi]
            and local_by_doi[doi].get(field) != catalog_by_doi[doi].get(field)
        }
        local_hash = local_by_doi[doi].get("catalog_sha256")
        if local_hash not in {None, digest}:
            fields["catalog_sha256"] = {"local": local_hash, "public": digest}
        if fields:
            changed.append({"doi": catalog_by_doi[doi]["doi"], "fields": fields})
    return {
        "added": [catalog_by_doi[doi]["doi"] for doi in added],
        "not_listed": [local_by_doi[doi]["doi"] for doi in not_listed],
        "changed": changed,
    }


def apply_repository_refresh(
    payload: Any,
    local: list[dict[str, Any]],
    remote: list[dict[str, Any]],
) -> Any:
    local_by_name = {repo_name(record).casefold(): record for record in local}
    remote_by_name = {str(record["name"]).casefold(): record for record in remote}
    output: list[dict[str, Any]] = []
    for key in sorted(set(local_by_name) | set(remote_by_name)):
        if key not in remote_by_name:
            preserved = dict(local_by_name[key])
            if preserved.get("public_listing_status") != "not_listed":
                preserved["public_listing_status"] = "not_listed"
                preserved["needs_review"] = True
            output.append(preserved)
            continue
        public = public_repo_metadata(remote_by_name[key])
        if key not in local_by_name:
            output.append(
                {
                    **public,
                    "head_sha": None,
                    "summary": None,
                    "role": None,
                    "interfaces": [],
                    "dimensions": [],
                    "related_papers": [],
                    "dependencies": [],
                    "maturity": "unreviewed",
                    "evidence_state": "unreviewed",
                    "limits": [],
                    "needs_review": True,
                    "head_refresh_required": True,
                    "public_listing_status": "listed",
                }
            )
            continue
        prior = local_by_name[key]
        updated = dict(prior)
        changed = False
        prior_pushed = repo_field(prior, "pushed_at")
        for field, value in public.items():
            if repo_field(prior, field) != value:
                if field == "license_spdx" and isinstance(updated.get("license"), dict):
                    updated["license"] = dict(updated["license"])
                    updated["license"]["api_spdx"] = value
                else:
                    updated[field] = value
                changed = True
        updated["public_listing_status"] = "listed"
        observed_head = remote_by_name[key].get("_observed_head_sha")
        if (
            prior_pushed != public["pushed_at"]
            or (
                isinstance(observed_head, str)
                and observed_head != prior.get("head_sha")
            )
        ):
            updated["head_refresh_required"] = True
        if changed:
            updated["needs_review"] = True
        output.append(updated)
    if isinstance(payload, dict):
        result = dict(payload)
        key = "repositories" if "repositories" in payload else "records"
        result[key] = output
        return result
    return output


def apply_paper_refresh(
    local: list[dict[str, Any]],
    catalog: dict[str, Any],
    digest: str,
    excluded_dois: set[str],
) -> list[dict[str, Any]]:
    catalog_by_doi = {
        str(record["doi"]).casefold(): record
        for record in catalog["records"]
        if isinstance(record, dict) and isinstance(record.get("doi"), str)
    }
    seen: set[str] = set()
    output: list[dict[str, Any]] = []
    factual_fields = (
        "title",
        "date_published",
        "canonical_url",
        "authors",
        "abstract",
        "keywords",
    )
    for prior in local:
        doi_value = prior.get("doi")
        if not isinstance(doi_value, str) or not doi_value:
            output.append(prior)
            continue
        key = doi_value.casefold()
        seen.add(key)
        if key not in catalog_by_doi:
            updated = dict(prior)
            updated["catalog_status"] = "not_listed"
            updated["needs_review"] = True
            output.append(updated)
            continue
        source = catalog_by_doi[key]
        updated = dict(prior)
        changed = False
        for field in factual_fields:
            if updated.get(field) != source.get(field):
                updated[field] = source.get(field)
                changed = True
        if updated.get("catalog_sha256") not in {None, digest}:
            changed = True
        updated["catalog_sha256"] = digest
        updated["catalog_status"] = "listed"
        if changed:
            updated["needs_review"] = True
        output.append(updated)
    for key in sorted(set(catalog_by_doi) - seen - excluded_dois):
        source = catalog_by_doi[key]
        output.append(
            {
                "record_type": "paper",
                "doi": source["doi"],
                **{field: source.get(field) for field in factual_fields},
                "subject": [],
                "central_contribution": None,
                "methods": [],
                "phase_dimensions": [],
                "related_repositories": [],
                "catalog_sha256": digest,
                "catalog_status": "listed",
                "needs_review": True,
            }
        )
    return output


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_write_many(contents: dict[Path, str]) -> None:
    originals = {
        path: path.read_text(encoding="utf-8") if path.exists() else None
        for path in contents
    }
    temporary_paths: dict[Path, Path] = {}
    try:
        for path, content in contents.items():
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
            )
            temporary = Path(temporary_name)
            temporary_paths[path] = temporary
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
        for path, temporary in temporary_paths.items():
            os.replace(temporary, path)
    except OSError:
        for path, original in originals.items():
            if original is not None:
                atomic_write(path, original)
            elif path.exists():
                path.unlink()
        raise
    finally:
        for temporary in temporary_paths.values():
            if temporary.exists():
                temporary.unlink()


def main() -> int:
    args = parse_args()
    if args.timeout <= 0 or args.timeout > 120:
        diagnostic("--timeout must be greater than 0 and no more than 120 seconds")
        emit({"ok": False, "error": "invalid timeout"}, pretty=args.pretty)
        return 2
    mode = "write" if args.write else "check"
    try:
        repositories_payload, local_repositories = read_repositories()
        local_papers = read_papers()
        source_state = read_source_state()
        excluded_dois = excluded_catalog_dois(source_state)
        observed_repositories = fetch_public_repositories(args.timeout)
        public_repositories, derivative_exclusions = upstream_repositories(
            observed_repositories, args.timeout
        )
        catalog = fetch_public_catalog(args.timeout)
        catalog_digest = canonical_digest(catalog)
        repository_drift = compare_repositories(local_repositories, public_repositories)
        paper_drift = compare_papers(
            local_papers, catalog, catalog_digest, excluded_dois
        )
    except (
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        urllib.error.URLError,
    ) as exc:
        diagnostic(str(exc))
        emit({"ok": False, "mode": mode, "error": str(exc)}, pretty=args.pretty)
        return 2

    drift = any(repository_drift[key] for key in repository_drift) or any(
        paper_drift[key] for key in paper_drift
    )
    written: list[str] = []
    if args.write and drift:
        refreshed_repositories = apply_repository_refresh(
            repositories_payload, local_repositories, public_repositories
        )
        refreshed_papers = apply_paper_refresh(
            local_papers, catalog, catalog_digest, excluded_dois
        )
        source_state["refresh"] = {
            "checked_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
            "github_endpoint": GITHUB_REPOS_URL.format(page="{page}"),
            "github_observed_public_repository_count": len(observed_repositories),
            "github_upstream_source_count": len(public_repositories),
            "derivative_exclusions": derivative_exclusions,
            "catalog_url": HF_CATALOG_URL,
            "catalog_record_count": len(catalog["records"]),
            "catalog_sha256": catalog_digest,
            "needs_review": True,
        }
        repositories_text = (
            json.dumps(
                refreshed_repositories,
                ensure_ascii=True,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
        papers_text = "".join(
            json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n"
            for record in refreshed_papers
        )
        source_state.setdefault("hashes", {})[
            "repositories_json_sha256"
        ] = hashlib.sha256(repositories_text.encode("utf-8")).hexdigest()
        source_state["hashes"]["derived_papers_jsonl_sha256"] = hashlib.sha256(
            papers_text.encode("utf-8")
        ).hexdigest()
        state_text = (
            json.dumps(source_state, ensure_ascii=True, indent=2, sort_keys=True)
            + "\n"
        )
        atomic_write_many(
            {
                REPOSITORIES_PATH: repositories_text,
                PAPERS_PATH: papers_text,
                SOURCE_STATE_PATH: state_text,
            }
        )
        written = [
            "references/repositories.json",
            "references/papers.jsonl",
            "references/source-state.json",
        ]

    payload = {
        "ok": True,
        "mode": mode,
        "drift": drift,
        "public_state": {
            "github_endpoint": GITHUB_REPOS_URL.format(page="{page}"),
            "observed_public_repository_count": len(observed_repositories),
            "upstream_source_count": len(public_repositories),
            "derivative_exclusions": derivative_exclusions,
            "catalog_url": HF_CATALOG_URL,
            "catalog_record_count": len(catalog["records"]),
            "catalog_sha256": catalog_digest,
        },
        "repository_drift": repository_drift,
        "paper_drift": paper_drift,
        "written": written,
        "notice": (
            "HEAD SHAs are checked from each upstream default branch. --write marks "
            "changed records for review and never silently replaces a pinned head_sha."
        ),
    }
    emit(payload, pretty=args.pretty)
    if mode == "check" and drift:
        diagnostic("public source drift detected")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
