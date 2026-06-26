"""Apply refine diff operations to a blueprint.

Diff format:
{
  "diffId": "diff-...",
  "baseBlueprintRevisionId": "rev-...",
  "operations": [
    {"op": "modify", "path": "library.knowledge.painPoints[0].name", "old": "...", "new": "..."},
    {"op": "add", "path": "library.knowledge.painPoints[]", "value": {...}},
    {"op": "delete", "path": "library.knowledge.pitfalls[2]"}
  ],
  "rationale": "..."
}

Path syntax:
- Dot-separated keys: library.knowledge.painPoints
- Array index: painPoints[0]
- Array append marker: painPoints[]
"""
from __future__ import annotations

import copy
import re
from typing import Any


_PATH_SEGMENT_RE = re.compile(r"([^.\[\]]+)|\[(\d*)\]")


class DiffPatchError(ValueError):
    """Raised when a diff operation cannot be applied."""


def parse_path(path: str) -> list[str | int]:
    """Parse 'library.knowledge.painPoints[0].name' into ['library','knowledge','painPoints',0,'name'].

    The literal token '[]' (append marker) becomes the integer ``-1``.
    """
    if not path:
        raise DiffPatchError("Empty path")
    parts: list[str | int] = []
    pos = 0
    while pos < len(path):
        match = _PATH_SEGMENT_RE.match(path, pos)
        if not match:
            raise DiffPatchError(f"Invalid path segment at position {pos}: {path!r}")
        name, idx = match.groups()
        if name is not None:
            parts.append(name)
        else:
            parts.append(-1 if idx == "" else int(idx))
        pos = match.end()
        if pos < len(path) and path[pos] == ".":
            pos += 1
    return parts


def _walk(obj: Any, parts: list[str | int]) -> Any:
    """Walk object by path parts. Returns final node."""
    current = obj
    for part in parts:
        if isinstance(part, int):
            if not isinstance(current, list):
                raise DiffPatchError(f"Expected list, got {type(current).__name__}")
            if part == -1:
                raise DiffPatchError("Cannot walk into append marker '[]'")
            if part < 0 or part >= len(current):
                raise DiffPatchError(f"List index {part} out of range")
            current = current[part]
        else:
            if not isinstance(current, dict):
                raise DiffPatchError(f"Expected dict, got {type(current).__name__}")
            if part not in current:
                raise DiffPatchError(f"Key '{part}' not found")
            current = current[part]
    return current


def _apply_modify(blueprint: dict[str, Any], path: str, new_value: Any) -> None:
    parts = parse_path(path)
    if not parts:
        raise DiffPatchError("Modify requires non-empty path")
    parent = _walk(blueprint, parts[:-1])
    last = parts[-1]
    if isinstance(last, int):
        if not isinstance(parent, list):
            raise DiffPatchError("Modify expected list parent")
        if last == -1 or last < 0 or last >= len(parent):
            raise DiffPatchError(f"Modify index out of range: {last}")
        parent[last] = new_value
    else:
        if not isinstance(parent, dict):
            raise DiffPatchError("Modify expected dict parent")
        parent[last] = new_value


def _apply_add(blueprint: dict[str, Any], path: str, value: Any) -> None:
    parts = parse_path(path)
    if not parts:
        raise DiffPatchError("Add requires non-empty path")
    last = parts[-1]
    if last == -1:
        # Append to array — second-to-last must be the array key
        if len(parts) < 2:
            raise DiffPatchError("Append requires at least one parent key")
        array_key = parts[-2]
        parent = _walk(blueprint, parts[:-2])
        if isinstance(array_key, int):
            if not isinstance(parent, list):
                raise DiffPatchError("Append expected list grandparent")
            target = parent[array_key]
        else:
            if not isinstance(parent, dict):
                raise DiffPatchError("Append expected dict parent")
            target = parent.setdefault(array_key, [])
        if not isinstance(target, list):
            raise DiffPatchError(f"Append target is not a list: {array_key}")
        target.append(value)
        return

    parent = _walk(blueprint, parts[:-1])
    if isinstance(last, int):
        if not isinstance(parent, list):
            raise DiffPatchError("Add at index expected list parent")
        if last < 0 or last > len(parent):
            raise DiffPatchError(f"Add index out of range: {last}")
        parent.insert(last, value)
    else:
        if not isinstance(parent, dict):
            raise DiffPatchError("Add expected dict parent")
        parent[last] = value


def _apply_delete(blueprint: dict[str, Any], path: str) -> None:
    parts = parse_path(path)
    if not parts:
        raise DiffPatchError("Delete requires non-empty path")
    parent = _walk(blueprint, parts[:-1])
    last = parts[-1]
    if isinstance(last, int):
        if not isinstance(parent, list):
            raise DiffPatchError("Delete expected list parent")
        if last == -1 or last < 0 or last >= len(parent):
            raise DiffPatchError(f"Delete index out of range: {last}")
        parent.pop(last)
    else:
        if not isinstance(parent, dict):
            raise DiffPatchError("Delete expected dict parent")
        if last not in parent:
            raise DiffPatchError(f"Delete key not found: {last}")
        del parent[last]


def apply_diff(blueprint: dict[str, Any], diff: dict[str, Any]) -> dict[str, Any]:
    """Apply a list of operations to a blueprint, returning a new blueprint.

    The original blueprint is not mutated.
    Operations are applied in order. If any operation fails, raises DiffPatchError
    and the partial result is discarded.
    """
    result = copy.deepcopy(blueprint)
    operations = diff.get("operations", [])
    if not isinstance(operations, list):
        raise DiffPatchError("Diff operations must be a list")

    for idx, op_obj in enumerate(operations):
        if not isinstance(op_obj, dict):
            raise DiffPatchError(f"Operation #{idx} is not a dict")
        op_type = op_obj.get("op")
        path = op_obj.get("path", "")
        if not isinstance(path, str):
            raise DiffPatchError(f"Operation #{idx} path must be string")

        try:
            if op_type == "modify":
                _apply_modify(result, path, op_obj.get("new"))
            elif op_type == "add":
                _apply_add(result, path, op_obj.get("value"))
            elif op_type == "delete":
                _apply_delete(result, path)
            else:
                raise DiffPatchError(f"Unknown op type: {op_type!r}")
        except DiffPatchError as exc:
            raise DiffPatchError(f"Operation #{idx} ({op_type} {path}): {exc}") from exc

    return result


def filter_diff(diff: dict[str, Any], decisions: dict[int, str]) -> dict[str, Any]:
    """Filter a diff by per-operation decisions.

    decisions maps operation index -> "accept" | "reject".
    Operations without a decision default to "accept".
    Returns a new diff containing only accepted operations.
    """
    operations = diff.get("operations", [])
    accepted = [
        op for idx, op in enumerate(operations)
        if decisions.get(idx, "accept") == "accept"
    ]
    new_diff = copy.deepcopy(diff)
    new_diff["operations"] = accepted
    return new_diff
