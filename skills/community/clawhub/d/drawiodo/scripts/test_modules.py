"""Test module system"""
import sys, os
sys.path.insert(0, r"C:\Users\sm001\.workbuddy\skills\drawiodo\scripts")

from drawio_modules import registry, list_modules

print("=== 可用模块 ===")
for m in list_modules():
    print(f"  {m['name']}: {m['desc']}")

print("\n=== 1. Graph: 电商系统(tech主题) ===")
data = {
    "title": "E-Commerce (Tech)",
    "nodes": [
        {"id": "User", "label": "User", "shape": "uml",
         "fields": ["- id: Long", "- username: String"], "methods": ["+ login(): void"]},
        {"id": "Product", "label": "Product", "shape": "uml",
         "fields": ["- id: Long", "- name: String"], "methods": ["+ getStock(): int"]},
        {"id": "Order", "label": "Order", "shape": "uml",
         "fields": ["- orderId: Long"], "methods": ["+ pay(): void"]},
        {"id": "DB", "label": "PostgreSQL", "shape": "cylinder"},
        {"id": "Cache", "label": "Redis", "shape": "cylinder"},
    ],
    "edges": [
        {"from": "User", "to": "Order", "label": "1"},
        {"from": "Product", "to": "Order", "label": "2"},
        {"from": "User", "to": "DB", "label": "CRUD"},
        {"from": "Order", "to": "DB", "label": "CRUD"},
        {"from": "Product", "to": "Cache", "label": "cache"},
    ],
}
OUTPUT = r"C:\Users\sm001\WorkBuddy\2026-06-19-11-30-56"
builder = registry["graph"].build(data, theme="tech")
path = os.path.join(OUTPUT, "module_graph.drawio")
builder.save(path)
print(f"✅ {path}")

print("\n=== 2. Gantt: 项目甘特图(default主题) ===")
gantt_data = {
    "title": "Project Gantt",
    "tasks": [
        {"id": "req", "name": "需求分析", "start": 0, "end": 4},
        {"id": "design", "name": "系统设计", "start": 3, "end": 7},
        {"id": "dev", "name": "开发", "start": 6, "end": 12},
        {"id": "test", "name": "测试", "start": 11, "end": 15},
        {"id": "deploy", "name": "部署上线", "start": 14, "end": 17},
    ],
    "deps": [
        {"from": "req", "to": "design"},
        {"from": "design", "to": "dev"},
        {"from": "dev", "to": "test"},
        {"from": "test", "to": "deploy"},
    ],
}
builder2 = registry["gantt"].build(gantt_data, theme="default")
path2 = os.path.join(OUTPUT, "module_gantt.drawio")
builder2.save(path2)
print(f"✅ {path2}")

import subprocess
dp = r"C:\Program Files\draw.io\draw.io.exe"
if os.path.exists(dp):
    subprocess.Popen([dp, path])
    subprocess.Popen([dp, path2])
    print("\n📂 已在 draw.io 中打开")
