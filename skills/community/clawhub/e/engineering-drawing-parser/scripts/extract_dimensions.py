"""Extract dimensions and simple tolerances."""
from __future__ import annotations
import re
from typing import Any, Dict, List

DIM_PATTERNS = [
    re.compile(r"φ\s*(?P<value>\d+(?:\.\d+)?)(?:\s*(?P<tol>[+\-±]\s*\d+(?:\.\d+)?))?"),
    re.compile(r"R\s*(?P<value>\d+(?:\.\d+)?)"),
    re.compile(r"\b(?P<value>\d+(?:\.\d+)?)\s*(?P<tol>[+\-±]\s*\d+(?:\.\d+)?)"),
]
FIT = re.compile(r"\b[A-Z]\d+\s*/\s*[a-z]\d+\b")

def extract_dimensions(text: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for pat in DIM_PATTERNS:
        for m in pat.finditer(text):
            d: Dict[str, Any] = {"value": m.group("value")}
            tol = m.groupdict().get("tol") if "tol" in m.groupdict() else None
            if tol:
                d["tolerance"] = tol.replace(" ", "")
            d["span"] = [m.start(), m.end()]
            out.append(d)
    for m in FIT.finditer(text):
        out.append({"fit": m.group(0), "span": [m.start(), m.end()]})
    return out
