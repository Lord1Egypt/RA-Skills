"""Org chart using module system"""
import sys, os
sys.path.insert(0, r"C:\Users\sm001\.workbuddy\skills\drawiodo\scripts")
from drawio_modules import registry

OUTPUT = r"C:\Users\sm001\WorkBuddy\2026-06-19-11-30-56"

data = {
    "title": "Company Organization",
    "nodes": [
        {"id": "CEO", "label": "CEO\n王大明"},
        {"id": "CTO", "label": "CTO\n李小明"},
        {"id": "CFO", "label": "CFO\n陈大伟"},
        {"id": "COO", "label": "COO\n赵小红"},
        {"id": "Eng", "label": "Engineering\n张强"},
        {"id": "PM", "label": "Product\n刘丽"},
        {"id": "Fin", "label": "Finance\n吴娟"},
        {"id": "Ops", "label": "Operations\n周杰"},
        {"id": "Frontend", "label": "Frontend Team"},
        {"id": "Backend", "label": "Backend Team"},
        {"id": "DevOps", "label": "DevOps Team"},
        {"id": "QA", "label": "QA Team"},
        {"id": "Design", "label": "Design Team"},
        {"id": "HR", "label": "HR Team"},
        {"id": "Marketing", "label": "Marketing Team"},
    ],
    "edges": [
        {"from": "CEO", "to": "CTO", "label": ""},
        {"from": "CEO", "to": "CFO", "label": ""},
        {"from": "CEO", "to": "COO", "label": ""},
        {"from": "CTO", "to": "Eng", "label": ""},
        {"from": "CTO", "to": "PM", "label": ""},
        {"from": "CFO", "to": "Fin", "label": ""},
        {"from": "COO", "to": "Ops", "label": ""},
        {"from": "Eng", "to": "Frontend", "label": ""},
        {"from": "Eng", "to": "Backend", "label": ""},
        {"from": "Eng", "to": "DevOps", "label": ""},
        {"from": "Eng", "to": "QA", "label": ""},
        {"from": "PM", "to": "Design", "label": ""},
        {"from": "Ops", "to": "Marketing", "label": ""},
        {"from": "Ops", "to": "HR", "label": ""},
    ],
}

builder = registry["graph"].build(data, theme="nature")
path = os.path.join(OUTPUT, "org_chart.drawio")
builder.save(path)
print(f"✅ {path}")

import subprocess
dp = r"C:\Program Files\draw.io\draw.io.exe"
if os.path.exists(dp):
    subprocess.Popen([dp, path])
    print("📂 已打开")
