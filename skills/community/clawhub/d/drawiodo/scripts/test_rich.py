"""
test_rich.py — 复杂图：全栈电商系统
展示 UML 类图、ER实体、圆柱体数据库、菱形决策、各种形状
"""
import sys, os
sys.path.insert(0, r"C:\Users\sm001\.workbuddy\skills\drawiodo\scripts")
from drawio_unified import generate_diagram

OUTPUT = r"C:\Users\sm001\WorkBuddy\2026-06-19-11-30-56"

nodes = [
    # ===== 用户层 =====
    {"id": "User", "label": "User", "shape": "uml",
     "fields": ["- id: Long", "- username: String", "- email: String", "- createdAt: Date"],
     "methods": ["+ login(): void", "+ logout(): void"]},

    {"id": "Session", "label": "Session", "shape": "note",
     "value": "Session\nToken Manager"},

    # ===== 商品服务 =====
    {"id": "Product", "label": "Product", "shape": "uml",
     "fields": ["- id: Long", "- name: String", "- price: BigDecimal", "- stock: Integer"],
     "methods": ["+ getStockStatus(): String"]},

    {"id": "Category", "label": "Category", "shape": "uml",
     "fields": ["- id: Long", "- name: String", "- parentId: Long"],
     "methods": ["+ getChildren(): List"]},

    {"id": "Cart", "label": "Cart", "shape": "uml",
     "fields": ["- cartId: Long", "- userId: Long", "- items: List"],
     "methods": ["+ addItem(p, qty): void", "+ checkout(): Order"]},

    # ===== 订单 =====
    {"id": "Order", "label": "Order", "shape": "uml",
     "fields": ["- orderId: Long", "- userId: Long", "- total: BigDecimal", "- status: String"],
     "methods": ["+ pay(): void", "+ cancel(): void", "+ getItems(): List"]},

    {"id": "Payment", "label": "Payment", "shape": "hexagon",
     "value": "Payment\nGateway"},
    
    {"id": "Refund", "label": "Refund", "shape": "diamond",
     "value": "Refund\nDecision"},

    # ===== 数据库 =====
    {"id": "DB-Main", "label": "Main DB\n(PostgreSQL)", "shape": "cylinder"},
    {"id": "DB-Cache", "label": "Redis\nCache", "shape": "cylinder"},

    # ===== 订单实体 =====
    {"id": "OrderItem", "label": "OrderItem", "shape": "uml",
     "fields": ["- itemId: Long", "- orderId: Long", "- productId: Long", "- qty: Integer"],
     "methods": ["+ subtotal(): BigDecimal"]},

    # ===== 基础设施 =====
    {"id": "MQ", "label": "Message\nQueue", "shape": "document"},
    {"id": "CDN", "label": "CDN", "shape": "cloud"},
    {"id": "Search", "label": "Elastic\nSearch", "shape": "folder"},
]

edges = [
    # 用户 → 购物车/订单
    {"from": "User", "to": "Session", "label": "manage"},
    {"from": "User", "to": "Cart", "label": "owns 1"},
    {"from": "User", "to": "Order", "label": "places 1"},
    
    # 购物车 → 订单
    {"from": "Cart", "to": "Order", "label": "checkout"},
    {"from": "Order", "to": "OrderItem", "label": "contains"},
    {"from": "Order", "to": "Payment", "label": "pay"},
    {"from": "Payment", "to": "Refund", "label": "fail →"},
    {"from": "Order", "to": "MQ", "label": "publish"},

    # 商品
    {"from": "Product", "to": "Category", "label": "belongs to"},
    {"from": "Product", "to": "OrderItem", "label": "referenced in"},
    {"from": "Product", "to": "Cart", "label": "added to"},

    # 数据库
    {"from": "User", "to": "DB-Main", "label": "CRUD"},
    {"from": "Order", "to": "DB-Main", "label": "CRUD"},
    {"from": "Product", "to": "DB-Main", "label": "CRUD"},
    {"from": "Product", "to": "DB-Cache", "label": "cache"},
    
    # 基础设施
    {"from": "CDN", "to": "Product", "label": "static"},
    {"from": "Search", "to": "Product", "label": "index"},
]

print("=" * 60)
print("生成复杂图：全栈电商系统（UML + 数据库 + 多种形状）")
print("=" * 60)

builder = generate_diagram(nodes, edges, "Full-Stack E-Commerce System")

path = os.path.join(OUTPUT, "complex_ecommerce.drawio")
builder.save(path)
print(f"\n✅ {path}")

# 打开 draw.io
import subprocess
drawio_path = r"C:\Program Files\draw.io\draw.io.exe"
if os.path.exists(drawio_path):
    subprocess.Popen([drawio_path, path])
    print("📂 已打开")
