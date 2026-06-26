# CMS Executor - 多平台 CMS 连接器

## 概述

本模块提供多平台（WordPress / Shopify / Amazon）CMS 直连执行能力，支持通过平台原生 API 创建/更新/删除内容，配合审批引擎和回滚机制实现安全的内容管理。

## 目录结构

```
cms-executor/
├── connectors/
│   ├── __init__.py              # 统一导出
│   ├── base_connector.py        # 抽象基类（所有 CMS 平台通用接口）
│   ├── wordpress_connector.py   # WordPress REST API 实现
│   ├── shopify_connector.py     # Shopify GraphQL Admin API 实现
│   └── amazon_connector.py      # Amazon SP-API 实现
├── engine/
│   ├── __init__.py
│   ├── approval.py              # 多级审批引擎
│   └── rollback.py              # 变更追踪与回滚
└── tests/
    ├── test_cms_executor.py     # WordPress & 审批引擎测试
    └── test_connectors.py       # Shopify & Amazon 连接器测试
```

---

## 平台支持

| 平台 | API | 认证方式 |
|------|-----|---------|
| WordPress | REST API v2 | Application Passwords |
| Shopify | GraphQL Admin API 2024-01 | OAuth / API Key |
| Amazon | SP-API | LWA OAuth |

---

## 1. Shopify 连接器

### 认证配置

1. 在 Shopify 后台创建私有应用或自定义应用
2. 配置 API 权限（Products, Variants, Images）
3. 获取访问令牌（Access Token）

### 基本使用

```python
from connectors import ShopifyConnector, CMSCredential, ContentPayload

# 初始化连接器
cred = CMSCredential(
    url="https://your-shop.myshopify.com",
    api_key="<YOUR_SHOPIFY_ACCESS_TOKEN>",   # 访问令牌
)
shopify = ShopifyConnector(cred)

# 验证连接
if shopify.authenticate():
    print("✅ Shopify 连接成功")

# ── 商品 CRUD ────────────────────────────────────────
from connectors.shopify_connector import ProductPayload, VariantPayload

# 方式一：使用 ContentPayload（兼容基类）
payload = ContentPayload(title="My Product", content="<p>Description</p>", status="draft")
result = shopify.create_content(payload)
print(f"✅ 商品已创建，ID={result['id']}, handle={result['handle']}")

# 方式二：使用 ProductPayload（Shopify 原生字段）
from connectors.shopify_connector import ProductPayload, VariantPayload, ImagePayload, SEOPayload
product = ProductPayload(
    title="Premium Widget",
    body_html="<p>High quality widget</p>",
    vendor="Acme Corp",
    product_type="Electronics",
    status="active",
    tags=["widget", "premium"],
    variants=[
        VariantPayload(
            title="Blue / Large",
            price="29.99",
            sku="WGT-BL-L",
            inventory_quantity=100,
            option1="Blue", option2="Large",
        ),
        VariantPayload(
            title="Red / Large",
            price="29.99",
            sku="WGT-RE-L",
            inventory_quantity=50,
            option1="Red", option2="Large",
        ),
    ],
    images=[
        ImagePayload(src="https://cdn.example.com/widget.jpg", alt_text="Widget front view"),
    ],
    seo=SEOPayload(title="Premium Widget - Acme Corp", description="Shop premium widgets"),
)
# 通过内部 GraphQL API 直接创建
resp = shopify._graphql(shopify._build_product_create_mutation(product))

# ── 变体操作 ──────────────────────────────────────────
variant = VariantPayload(
    title="Green / Medium",
    price="24.99",
    sku="WGT-GN-M",
    inventory_quantity=30,
)
shopify.create_variant(product_id=123, variant=variant)
shopify.update_variant(variant_id=555, variant=VariantPayload(price="22.99", inventory_quantity=10))
shopify.delete_variant(variant_id=555)

# ── 图片操作 ─────────────────────────────────────────
from connectors.shopify_connector import ImagePayload
shopify.add_product_image(123, ImagePayload(src="https://cdn.example.com/extra.jpg"))
shopify.delete_product_image(image_id="111")

# ── 商品列表 ─────────────────────────────────────────
products = shopify.list_content({"first": 50, "query": "status:active"})
for p in products:
    print(f"  {p['id']} | {p['title']} | {p['handle']}")

# ── 删除商品（归档） ──────────────────────────────────
shopify.delete_content(product_id=123)       # 归档（soft delete）
shopify.delete_content(product_id=123, force=True)  # 永久删除

# ── 历史 ─────────────────────────────────────────────
history = shopify.get_history()
for h in history:
    print(f"  [{h['timestamp']}] {h['operation']} - {h['status']}")

# ── 回滚 ─────────────────────────────────────────────
# 回滚最近一次创建操作
for rec in reversed(history):
    if rec["operation"] == "create" and rec["status"] == "executed":
        shopify.rollback_operation(rec["id"])
        print("✅ 回滚成功")
        break

shopify.close()
```

---

## 2. Amazon SP-API 连接器

### 认证配置

1. 在 Seller Central 注册 SP-API 应用，获取 Client ID 和 Client Secret
2. 完成 LWA OAuth 流程，获取 Refresh Token
3. Refresh Token 可长期有效，用于自动刷新 Access Token

### 基本使用

```python
from connectors import AmazonConnector, CMSCredential, ContentPayload

# 初始化连接器
cred = CMSCredential(
    url="https://sellercentral.amazon.com",
    username="amzn1.application-xxx.client_id",
    app_password="amzn1.application-xxx.client_secret",
    api_key="Atza|xxx-access-token",  # 可选，已有 access token
)
amazon = AmazonConnector(
    cred,
    region="na",                    # na | eu | fe
    marketplace_id="A1AM79NJPZON8",  # 美国市场
)

# 设置 Refresh Token（用于自动续期 access token）
amazon.set_refresh_token("Atzr|...")

# 验证连接
if amazon.authenticate():
    print("✅ Amazon SP-API 连接成功")

# ── 商品列表操作 ─────────────────────────────────────
from connectors.amazon_connector import AmazonListingPayload

# 方式一：使用 ContentPayload
payload = ContentPayload(title="USB-C Cable", content="High-speed USB-C cable 2m")
result = amazon.create_content(payload)

# 方式二：使用 AmazonListingPayload（完整字段）
listing = AmazonListingPayload(
    sku="USB-C-2M-BLK",
    product_type="ELECTRONIC_ACCESSORY",
    title="USB-C to USB-C Cable 2m Fast Charging",
    description="Braided nylon, 100W PD fast charge",
    brand="CableMax",
    manufacturer="CableMax Inc",
    price_amount=12.99,
    price_currency="USD",
    quantity=500,
    condition_type="New",
    fulfillment_channel="MFN",
    bullet_points=[
        "100W Power Delivery",
        "USB 3.1 Gen 2, 10Gbps",
        "Durable braided nylon",
    ],
)
resp = amazon._spapi_request(
    "PUT",
    f"/listings/2021-08-01/items/{SELLER_ID}/{listing.sku}?marketplaceId={marketplace}",
    token=access_token,
    data={"attributes": {...}},
)

# 更新商品
result = amazon.update_content(sku_int, payload)

# 删除商品
result = amazon.delete_content(sku_int)

# ── 库存管理 ──────────────────────────────────────────
# 更新库存
amazon.update_inventory(sku="USB-C-2M-BLK", quantity=300, fulfillment_channel="MFN")
# 查询库存
inv = amazon.get_inventory("USB-C-2M-BLK")
# 批量查询
inventories = amazon.list_inventory({"next_token": ""})

# ── 价格管理 ──────────────────────────────────────────
# 更新价格
amazon.update_pricing(sku="USB-C-2M-BLK", amount=14.99, currency="USD")
# 查询价格
price = amazon.get_pricing("USB-C-2M-BLK")

# ── 报告 ─────────────────────────────────────────────
from connectors.amazon_connector import PricePayload, InventoryPayload

# 请求商品报告
report = amazon.request_report(
    report_type="GET_MERCHANT_LISTINGS_DATA",
    marketplace_ids=["A1AM79NJPZON8"],
)
print(f"Report ID: {report['report_id']}, Status: {report['status']}")

# 查询报告状态
status = amazon.get_report(report["report_id"])
# 获取报告下载链接
document = amazon.get_report_document(status["payload"]["reportDocumentId"])
download_url = document["url"]  # 预签名 S3 URL

# ── Feed 提交（批量 XML） ─────────────────────────────
xml_content = '<?xml version="1.0"?><AmazonEnvelope><Header>...</Header></AmazonEnvelope>'
feed = amazon.submit_feed(
    feed_type="POST_PRODUCT_DATA",
    content=xml_content,
    content_type="text/xml",
)
print(f"Feed ID: {feed['feed_id']}, Status: {feed['status']}")

# ── 历史与回滚 ────────────────────────────────────────
history = amazon.get_history()
for h in history:
    print(f"  [{h['timestamp']}] {h['operation']} {h['entity_type']} - {h['status']}")

amazon.close()
```

---

## 3. 审批流程（通用）

```python
from engine import ApprovalEngine, ApprovalRule, ApprovalLevel, OperationType

engine = ApprovalEngine()

# 创建审批请求（草稿 → 自动通过）
req = engine.create_request(
    submitter="auto-bot",
    operation=OperationType.CREATE,
    payload={"title": "新商品", "content": "...", "status": "draft"},
)

if engine.can_auto_approve(req):
    engine.auto_approve(req)
    print("✅ 自动审批通过")
else:
    print(f"⏳ 等待审批，级别: {req.level.value}")
    engine.vote(req.id, approver="admin", decision="approve")
```

---

## 4. 回滚操作

```python
from engine import RollbackEngine

rollback = RollbackEngine(shopify)  # 或 AmazonConnector 实例

# 查看最近变更
changes = rollback.list_recent_changes(hours=24)
for c in changes:
    print(f"  {c['id']} | {c['operation']} | {c['status']}")

# 生成回滚计划（不执行）
plan = rollback.plan_rollback(record_id="abc12345")
print(f"回滚计划: {plan.strategy.value}, 步骤数: {len(plan.steps)}")

# 执行回滚
result = rollback.execute_rollback(plan.plan_id, force=True)
print(f"回滚结果: {'成功' if result['success'] else '失败'}")
```

---

## 风险分级

| 操作 | 触发条件 | 审批级别 |
|------|---------|---------|
| 创建商品 | 草稿状态 + 内容安全 | **AUTO_PASS** |
| 更新商品 | 任意状态 | **SINGLE** |
| 删除商品 | 任意状态 | **MULTI_SIGN** |
| 价格变更 | 价格修改 | **MULTI_SIGN** |
| 包含危险关键词 | `<script>`/`<?php` 等 | **MULTI_SIGN** |

**AUTO_PASS**：无需审批，系统自动通过
**SINGLE**：单人审批（任意一位审批人同意即可）
**MULTI_SIGN**：多人会签（所有审批人全部同意）
**ANY_SIGN**：任意一人同意即可

---

## 测试运行

```bash
cd agent-cluster/cms-executor

# 运行 Shopify & Amazon 连接器测试（推荐）
python -m pytest tests/test_connectors.py -v

# 运行 WordPress & 审批引擎测试
python -m pytest tests/test_cms_executor.py -v

# 运行全部测试
python -m pytest tests/ -v

# 或直接运行
python tests/test_connectors.py
python tests/test_cms_executor.py
```

---

## 扩展其他 CMS

继承 `BaseCMSConnector` 抽象类，实现以下方法即可：

```python
from connectors.base_connector import BaseCMSConnector, CMSCredential, ContentPayload

class MyCMSConnector(BaseCMSConnector):
    def authenticate(self) -> bool: ...
    def create_content(self, payload: ContentPayload) -> Dict[str, Any]: ...
    def update_content(self, content_id: int, payload: ContentPayload) -> Dict[str, Any]: ...
    def delete_content(self, content_id: int, force: bool = False) -> Dict[str, Any]: ...
    def get_content(self, content_id: int) -> Dict[str, Any]: ...
    def list_content(self, params: Dict[str, Any] = None) -> List[Dict[str, Any]]: ...
    def _do_rollback(self, record: OperationRecord) -> bool: ...
```
