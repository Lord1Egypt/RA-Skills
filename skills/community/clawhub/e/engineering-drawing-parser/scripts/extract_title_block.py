"""Extract drawing title block fields from layout text."""
from __future__ import annotations
import re
from typing import Dict

GB_KEYS = {
    "drawing_no": [r"图\s*号[:：]\s*([A-Za-z0-9\-\.]+)"],
    "drawing_name": [r"图\s*名[:：]\s*([^\n]+)"],
    "scale": [r"比\s*例[:：]\s*([0-9:：./]+)"],
    "material": [r"材\s*料[:：]\s*([^\n]+)"],
    "designer": [r"设\s*计[:：]\s*([^\n]+)"],
    "checker":  [r"校\s*对[:：]\s*([^\n]+)"],
    "approver": [r"审\s*核[:：]\s*([^\n]+)|批\s*准[:：]\s*([^\n]+)"],
    "date":     [r"日\s*期[:：]\s*([0-9\.\-/年月日]+)"],
}

def extract_title_block(text: str, standard: str = "GB") -> Dict[str, str]:
    out: Dict[str, str] = {}
    for key, patterns in GB_KEYS.items():
        for p in patterns:
            m = re.search(p, text)
            if m:
                # pick first non-None group
                for g in m.groups():
                    if g:
                        out[key] = g.strip()
                        break
                break
    return out
