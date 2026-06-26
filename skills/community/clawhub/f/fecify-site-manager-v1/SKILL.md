---
name: fecify-site-manager-v1
version: "1"
description: >
  管理多个 Fecify 独立站。每个会话绑定一个站点（URL + API Token），配置持久化，
  重启不丢失。支持商品、订单及 CSV 批量导入等业务操作。
---

# Fecify 站群管家 v1

> 版本: v1 | 配置数据存储于 `data/fecify-shared/`，发版升级不影响已有配置

## 0. 会话隔离

**所有 exec 调用必须带 `env: { FECIFY_SESSION: "<标识>" }`。**

会话标识：用户指定 → 用指定名称；未指定 → 用 session key 后 8 位。

```
exec({ env: { FECIFY_SESSION: "agent-a" }, command: "node scripts/base/check-config.js" })
```

## 1. 会话启动

```
node scripts/base/check-config.js
```

**未配置** → 提示用户提交 `站点URL` + `AccessToken`（任意格式），然后：

```
node scripts/base/save-config.js "<URL>" "<Token>"
```

该脚本自动保存配置并拉取 init 数据。配置持久化，不受重启影响。

**已配置** → 显示站点 URL 和 init 状态。

## 2. 模块速查

### API 操作

| 模块 | 文档 | API |
|------|------|-----|
| 商品 | [products.md](docs/products.md) | 列表/详情/创建/更新 |
| 图片 | [base-image.md](docs/base-image.md) | 列表/上传（跨模块公用） |
| 订单 | [orders.md](docs/orders.md) | 待补充 |
| 优惠券 | [coupons.md](docs/coupons.md) | 待补充 |

### 业务场景

| 场景 | 文档 | 说明 |
|------|------|------|
| CSV 导入 | [csv-import.md](docs/csv-import.md) | 所有平台 CSV 商品导入入口 |

### 参考

| 文档 | 说明 |
|------|------|
| [architecture.md](docs/architecture.md) | 目录结构 / api-client / site-config |
| [extending.md](docs/extending.md) | 新增模块 / 新增 CSV 格式 |

## 3. API 调用

```
node scripts/proxy/api-call.js <METHOD> <PATH> [BODY_JSON]
```

示例：

```
node scripts/proxy/api-call.js GET /api/skill/product/list '{"pageNum":1,"pageSize":20}'
node scripts/proxy/api-call.js POST /api/skill/product/create '{"product":{...}}'
```

先读 `docs/` 下对应文档获取参数说明，再调用。

### 响应判断

**`code === 200` → 成功；否则 → 失败。**

```json
// 成功
{ "code": 200, "message": "success", "data": { ... } }
// 业务错误
{ "code": 100701001, "message": "product save fail | ..." }
// PHP 异常（HTML 响应）
{ "code": -1, "message": "服务端返回 HTML 异常...", "_raw": "..." }
```

- `code === 200` → 读 `data`
- `code === -1` → 网络/解析层错误
- 其他 `code` → 业务错误，看 `message`

## 4. CSV 导入（两步交互）

用户上传 CSV → **先检测再导入，不可跳过检测**。
检测分两步：① 表格格式识别 ② 数据行校验。有异常 → 提示修复重新上传；无异常 → 展示选项等用户确认。
完整交互模板见 [shopify-csv-product-import.md](docs/csv-import/shopify-csv-product-import.md#用户交互提示agent-参考)。

```
# Step 1 — 检测
node scripts/csv-import/detect-shopify-csv.js <CSV文件>

# Step 2 — 执行（根据用户选择组装参数）
node scripts/csv-import/import-shopify-csv.js <CSV> [--max=N] [--skip=N] [--dry-run] [--use-network-images] [--gen-tags=none|auto|force] [--tag-count=N] [--img-concurrency=N] [--img-retries=N] [--import-concurrency=N] [--skip-validation]
```
