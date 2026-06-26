#!/usr/bin/env python3
"""Build calendar-style schedule matrix for Feishu Base."""
import json
from collections import defaultdict
from datetime import datetime

with open("config/schedule_registry.json") as f:
    data = json.load(f)
with open("config/accounts.json") as f:
    accounts = json.load(f)

matrix = defaultdict(lambda: defaultdict(list))
for e in data["schedule"]:
    dt = datetime.fromisoformat(e["scheduled_at"])
    ds = dt.strftime("%m/%d")
    d = e.get("direction", "")
    if d and d not in matrix[e["account_id"]][ds]:
        matrix[e["account_id"]][ds].append(d)

all_dates = sorted(set(
    datetime.fromisoformat(e["scheduled_at"]).strftime("%m/%d")
    for e in data["schedule"]
))
future_dates = [d for d in all_dates if d >= "06/03"]

style_map = {
    "velvet": "Velvet 城市", "soft_signal": "Soft Signal 亲子",
    "shadow_cut": "Shadow Cut 路线", "swiss_pulse": "Swiss Pulse 建议",
    "comparison": "Comparison 对比"
}

# Build field names
field_names = ["账号ID", "风格"]
for d in future_dates:
    field_names.append(d)

# Build records
records = []
for aid in sorted(accounts.keys(), key=lambda x: int(x)):
    a = accounts[aid]
    s = style_map.get(a.get("style", ""), a.get("style", ""))
    row = [f'{aid} {a.get("zh_name", "")}', s]
    for d in future_dates:
        dlist = matrix.get(aid, {}).get(d, [])
        row.append(" / ".join(dlist) if dlist else "—")
    records.append(row)

output = {"field_names": field_names, "records": records, "future_dates": future_dates}
with open("/tmp/schedule_matrix.json", "w") as f:
    json.dump(output, f, ensure_ascii=False)
print(json.dumps(output, ensure_ascii=False, indent=2))
