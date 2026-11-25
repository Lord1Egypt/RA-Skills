"""Bounded, explicit local structured-spec intake for the bundled engine."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

MAX_SPEC_BYTES = 2 * 1024 * 1024


class IntakeError(ValueError):
    """A user-safe local source acquisition error."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Object-pairs hook for json.loads that fails closed on duplicate keys."""
    seen: set[str] = set()
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate JSON key: {key!r}")
        seen.add(key)
        result[key] = value
    return result


def _load_yaml_strict(text: str) -> Any:
    """Parse YAML with safe_load while rejecting duplicate mapping keys."""
    try:
        import yaml
    except ModuleNotFoundError as exc:
        raise IntakeError("YAML support requires PyYAML from the bundled skill requirements") from exc

    class _NoDuplicateKeyLoader(yaml.SafeLoader):
        pass

    def _check_duplicate_key(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> dict[str, Any]:
        loader.flatten_mapping(node)
        seen: set[str] = set()
        result: dict[str, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node)
            if not isinstance(key, str):
                raise yaml.YAMLError(f"mapping key must be a string, got {type(key).__name__}")
            if key in seen:
                raise yaml.YAMLError(f"duplicate YAML key: {key!r}")
            seen.add(key)
            result[key] = loader.construct_object(value_node)
        return result

    _NoDuplicateKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        _check_duplicate_key,
    )
    return yaml.load(text, Loader=_NoDuplicateKeyLoader)  # noqa: S506 — custom SafeLoader subclass


def load_local_document(file_name: str) -> tuple[Path, dict[str, Any]]:
    """Read one explicit JSON/YAML file without following a remote descriptor."""
    path = Path(file_name)
    if not path.is_file():
        raise IntakeError("input must be an existing local file")
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise IntakeError("unable to read input file") from exc
    if size > MAX_SPEC_BYTES:
        raise IntakeError(f"input exceeds {MAX_SPEC_BYTES} byte limit")

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise IntakeError("input must be UTF-8 text") from exc

    suffix = path.suffix.lower()
    try:
        if suffix == ".json":
            document = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
        elif suffix in {".yaml", ".yml"}:
            document = _load_yaml_strict(text)
        else:
            raise IntakeError("input must have a .json, .yaml, or .yml extension")
    except IntakeError:
        raise
    except Exception as exc:
        kind = "JSON" if suffix == ".json" else "YAML"
        raise IntakeError(f"invalid {kind} document: {exc}") from exc

    if not isinstance(document, dict):
        raise IntakeError("specification root must be an object")
    return path, document


def _normalized_origin(value: str) -> tuple[str, str, int]:
    """Return a normalized http(s) origin tuple with its effective port."""
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError
    try:
        port = parsed.port
    except ValueError:
        raise ValueError from None
    return (
        parsed.scheme.lower(),
        parsed.hostname.lower(),
        port if port is not None else (443 if parsed.scheme.lower() == "https" else 80),
    )


def load_supplied_source(file_name: str, *, base_url: str | None = None) -> tuple[Path, dict[str, Any], str]:
    """Load one explicit local structured spec or supplied API-reference document.

    Documents never cause network discovery. They require an explicit http(s)
    base URL and are converted to a constrained OpenAPI-shaped in-memory model
    so they pass through the normal digest, receipt, and policy gates.
    """
    path = Path(file_name)
    suffix = path.suffix.lower()
    if suffix in {".json", ".yaml", ".yml"}:
        loaded_path, document = load_local_document(file_name)
        return loaded_path, document, "local-structured-spec"
    if suffix not in {".md", ".html", ".htm"}:
        raise IntakeError("input must be JSON, YAML, Markdown, or HTML")
    if not path.is_file():
        raise IntakeError("input must be an existing local file")
    try:
        if path.stat().st_size > MAX_SPEC_BYTES:
            raise IntakeError(f"input exceeds {MAX_SPEC_BYTES} byte limit")
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise IntakeError("input must be UTF-8 text") from exc
    if not base_url:
        raise IntakeError("document input requires an explicit --base-url")
    try:
        from documents import DocumentError, extract_operations
        source_kind = "markdown" if suffix == ".md" else "html"
        operations = extract_operations(content, source_kind=source_kind)
    except DocumentError as exc:
        raise IntakeError(str(exc)) from exc
    if not operations:
        raise IntakeError("document contains no explicit HTTP method/path evidence")

    try:
        base_origin = _normalized_origin(base_url)
    except ValueError:
        raise IntakeError("document --base-url must be a valid http(s) origin") from None

    paths: dict[str, dict[str, Any]] = {}
    for index, op in enumerate(operations, start=1):
        candidate = op["path"]
        parsed = urlsplit(candidate)
        if parsed.scheme:
            try:
                candidate_origin = _normalized_origin(candidate)
            except ValueError:
                raise IntakeError("absolute operation URL must be a valid http(s) origin") from None
            if candidate_origin != base_origin:
                raise IntakeError("absolute operation URL must match the explicit --base-url origin")
            path = parsed.path or "/"
        else:
            path = candidate
        path_item = paths.setdefault(path, {})
        operation_id = f"document_{op['method'].lower()}_{index}"
        path_parameters = [
            {"name": name, "in": "path", "required": True, "schema": {"type": "string"}}
            for name in re.findall(r"\{([A-Za-z][A-Za-z0-9_.-]{0,127})\}", path)
        ]
        internal_evidence = {
            "line": op["evidence"]["line"],
            "confidence": "explicit",
        }
        path_item[op["method"].lower()] = {
            "operationId": operation_id,
            "parameters": path_parameters,
            "x-api-to-typemcp-evidence": internal_evidence,
            "responses": {"200": {"description": "Document-derived operation"}},
        }
    document = {
        "openapi": "3.0.3",
        "info": {"title": "Document-derived API", "version": "0.0.0"},
        "servers": [{"url": base_url}],
        "paths": paths,
    }
    return path, document, f"local-{source_kind}-document"
