"""Variable pool and Dify template resolution.

Engine file — copy as-is from the skill template; do NOT edit per project.
Resolves Dify's {{#node_id.var#}}, {{#env.NAME#}}, {{#secret.NAME#}} syntax.
"""
from __future__ import annotations

import os
import re
from typing import Any

VAR_RE = re.compile(r"\{\{\s*#([^#]+)#\s*\}\}")


class VariablePool:
    """Holds every node's output variables, keyed by (node_id, var_name)."""

    def __init__(self) -> None:
        self._data: dict[tuple[str, str], Any] = {}

    def set(self, node_id: str, var: str, value: Any) -> None:
        self._data[(node_id, var)] = value

    def get(self, node_id: str, var: str, default: Any = None) -> Any:
        return self._data.get((node_id, var), default)

    def set_many(self, node_id: str, outputs: dict[str, Any]) -> None:
        for k, v in outputs.items():
            self.set(node_id, k, v)

    def resolve_ref(self, ref: str) -> Any:
        """Resolve a single reference body like 'node-1.text' or 'env.KEY'."""
        ref = ref.strip()
        if ref.startswith(("env.", "secret.")):
            return os.environ.get(ref.split(".", 1)[1], "")
        if ref == "context":
            return self.get("__runtime__", "context", "")
        if "." not in ref:
            # bare name: look up under sys first, then any node (last write wins)
            return self.get("sys", ref, "")
        node_id, var = ref.split(".", 1)
        return self.get(node_id, var, "")

    def resolve(self, text: Any) -> Any:
        """Interpolate all {{#...#}} placeholders in a string. Non-strings pass through."""
        if not isinstance(text, str):
            return text

        def _sub(m: re.Match) -> str:
            val = self.resolve_ref(m.group(1))
            return "" if val is None else str(val)

        return VAR_RE.sub(_sub, text)

    def resolve_map(self, obj: Any) -> Any:
        """Recursively resolve placeholders in dict/list/str structures."""
        if isinstance(obj, dict):
            return {k: self.resolve_map(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.resolve_map(v) for v in obj]
        return self.resolve(obj)
