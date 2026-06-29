"""Test all themes with the complex e-commerce diagram"""
import sys, os
sys.path.insert(0, r"C:\Users\sm001\.workbuddy\skills\drawiodo\scripts")
from drawio_unified import generate_diagram
import subprocess

OUTPUT = r"C:\Users\sm001\WorkBuddy\2026-06-19-11-30-56"

nodes = [
    {"id": "User", "label": "User", "shape": "uml",
     "fields": ["- id: Long", "- username: String", "- email: String"],
     "methods": ["+ login(): void", "+ logout(): void"]},
    {"id": "Product", "label": "Product", "shape": "uml",
     "fields": ["- id: Long", "- name: String", "- price: BigDecimal"],
     "methods": ["+ getStockStatus(): String"]},
    {"id": "Order", "label": "Order", "shape": "uml",
     "fields": ["- orderId: Long", "- userId: Long", "- total: BigDecimal"],
     "methods": ["+ pay(): void", "+ cancel(): void"]},
    {"id": "Cart", "label": "Cart", "shape": "uml",
     "fields": ["- cartId: Long", "- userId: Long"],
     "methods": ["+ checkout(): Order"]},
    {"id": "DB-Main", "label": "PostgreSQL", "shape": "cylinder"},
    {"id": "DB-Cache", "label": "Redis", "shape": "cylinder"},
    {"id": "MQ", "label": "Message Queue", "shape": "document"},
    {"id": "Payment", "label": "Payment", "shape": "hexagon"},
    {"id": "Refund", "label": "Refund", "shape": "diamond"},
]

edges = [
    {"from": "User", "to": "Cart", "label": "1"},
    {"from": "User", "to": "Order", "label": "2"},
    {"from": "Cart", "to": "Order", "label": "3"},
    {"from": "Order", "to": "Payment", "label": "pay"},
    {"from": "Payment", "to": "Refund", "label": "fail"},
    {"from": "Order", "to": "MQ", "label": "publish"},
    {"from": "Product", "to": "Cart", "label": "4"},
    {"from": "User", "to": "DB-Main", "label": "CRUD"},
    {"from": "Order", "to": "DB-Main", "label": "CRUD"},
    {"from": "Product", "to": "DB-Main", "label": "CRUD"},
    {"from": "Product", "to": "DB-Cache", "label": "cache"},
]

themes = ["default", "tech", "business", "bw", "nature"]

for theme in themes:
    builder = generate_diagram(nodes, edges, f"E-Commerce ({theme})", theme=theme)
    path = os.path.join(OUTPUT, f"theme_{theme}.drawio")
    builder.save(path)
    print(f"✅ theme_{theme}.drawio")

drawio_path = r"C:\Program Files\draw.io\draw.io.exe"
if os.path.exists(drawio_path):
    for theme in themes:
        subprocess.Popen([drawio_path, os.path.join(OUTPUT, f"theme_{theme}.drawio")])
    print("📂 全部已打开")
