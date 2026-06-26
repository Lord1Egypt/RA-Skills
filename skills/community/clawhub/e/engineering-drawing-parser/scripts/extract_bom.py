"""Extract BOM rows from a tabular text dump."""
from __future__ import annotations
import re
from typing import Any, Dict, List

# Heuristic: rows formatted as `<序号> <代号> <名称> <数量> <材料> [备注]`
ROW = re.compile(
    r"^(?P<no>\d{1,3})\s+(?P<part_no>[A-Za-z0-9./\-]+)\s+(?P<name>[\u4e00-\u9fa5A-Za-z0-9 \-]+?)\s+(?P<qty>\d+)\s+(?P<material>[^\s]+)(?:\s+(?P<remark>.+))?$"
)

def extract_bom(text: str) -> List[Dict[str, Any]]:
    bom = []
    for line in text.splitlines():
        m = ROW.match(line.strip())
        if m:
            d = m.groupdict()
            d["no"] = int(d["no"])
            d["qty"] = int(d["qty"])
            bom.append(d)
    return bom
