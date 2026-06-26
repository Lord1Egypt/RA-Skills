# Shopify CSV 商品导入

`scripts/csv-import/` 下 Shopify CSV 导入工具链。

## 涉及文件

| 文件 | 说明 |
|------|------|
| [detect-shopify-csv.js](../../scripts/csv-import/detect-shopify-csv.js) | 格式检测器 |
| [import-shopify-csv.js](../../scripts/csv-import/import-shopify-csv.js) | 主导入脚本 |

### 涉及 API

| API | 说明 |
|-----|------|
| `POST /api/skill/base-image/upload` | 上传图片 → 得 `path` |
| `POST /api/skill/product/create` | 创建商品 |

### 何时用

- 用户从 Shopify 导出商品 CSV，想迁移到 Fecify
- CSV 含多余列（Google Shopping、SEO 等）——检测器容忍

## 导入流程（两步）

> Agent 执行：用户上传 CSV 后，先检测再展示选项，用户确认后再导入。

### Step 1 — 检测

检测分两个步骤：

**① 格式识别** — 判断是否为 Shopify 商品表
**② 数据校验** — 逐行检查每个商品的数据完整性

```
node scripts/csv-import/detect-shopify-csv.js <CSV文件路径>
```

展示检测结果：
- 格式是否正确（不正确则显示错误原因）
- 表格类型、商品总数、单/多规格数量、额外列
- **数据异常**：逐商品列出 CSV 行号、异常字段和问题描述

> 如有数据异常（`dataIssues.totalIssues > 0`），提示用户修复 CSV 后重新上传，**不可直接导入**。
> 仅当无异常时才进入 Step 2。

### Step 2 — 执行导入

先 dry-run 快速验证 JSON 格式：

```
node scripts/csv-import/import-shopify-csv.js <CSV> --max=5 --dry-run
```

`--max=5` 只生成前 5 个商品的 JSON，快速验证格式是否正确。

正式导入（根据用户选择组装参数）：

```
# 默认值（全量 + 上传图片 + 不生成 tag）
node scripts/csv-import/import-shopify-csv.js <CSV>

# 带选项示例
node scripts/csv-import/import-shopify-csv.js <CSV> --max=100 --use-network-images --gen-tags=force --tag-count=5

# 跳过前 N 个 + 截取范围
node scripts/csv-import/import-shopify-csv.js <CSV> --skip=100 --max=50

# 自定义并发（示例：高配服务器）
node scripts/csv-import/import-shopify-csv.js <CSV> --img-concurrency=10 --import-concurrency=5

# 跳过执行层校验（仅调试用，不推荐）
node scripts/csv-import/import-shopify-csv.js <CSV> --skip-validation
```

（必须带 `FECIFY_SESSION` env）

导入完成后输出汇总：共 X 个 | 成功 Y | 失败 Z。**失败商品自动存档**到 `temp/failed/`，每文件含：
- 商品标题、Handle
- 完整的 API 请求体（requestBody）
- API 响应（code + message + _raw）
- 错误堆栈（如有）

成功商品不存档，只记录到汇总。`temp/` 下超过 7 天的文件每次运行自动清理。

## 用户交互提示（Agent 参考）

### 有数据异常时

检测到 `dataIssues.totalIssues > 0` 时，展示异常清单，不展示选项，不提示「继续」：

```
📊 Shopify 商品表 · [N] 个商品 · 单规格 [X] / 多规格 [Y]

---

⚠️ 数据异常：[M] 个问题 / [K] 个商品

Row [行号] · `[handle]`
　　　　❌ [字段] — [问题描述]

---

请修复以上问题后重新上传 CSV，再次导入。
```

### 无数据异常时

```
✅ 表格格式正确 — Shopify 商品表

📊 共 [N] 个商品 | 单规格 [X] 个 | 多规格 [Y] 个
⚠️ 发现 [M] 个额外列（不影响导入）

---

您可以指定以下导入选项（不指定则使用默认值）：

1. 导入哪些商品？
   → 导入前 N 个 / 全部商品（默认）

2. 商品图片怎么处理？
   → 上传到站点（默认） / 直接使用网络图

3. 需要自动生成 Tag 吗？
   → 不生成（默认）
   → 智能补全：CSV 有 tag 就用，没有则自动生成
   → 强制覆盖：全部自动生成，忽略 CSV 中的 tag

4. 生成几个 Tag？（仅开启 tag 生成时有效）
   → 默认 3-5 个，您也可以指定区间

5. 并发设置（默认：图片 5 并发 / 重试 3 次 / 商品 2 并发，适用于 2核4G 服务器）
   → 您可以根据服务器配置自定义，参考：
     · 2核4G → 图片 5，商品 2（默认）
     · 4核8G → 图片 10，商品 5
     · 8核16G → 图片 20，商品 10
     · 16核32G → 图片 30，商品 20

请回复「继续」使用默认值，或直接告诉我您的选择。

💡 参考示例：
导入50个商品，用网络图，强制生成4个tag，服务器4核8G
→ 等效 CLI：--max=50 --use-network-images --gen-tags=force --tag-count=4 --img-concurrency=10 --import-concurrency=5
```

用户回复「继续」→ 默认参数 `--img-concurrency=5 --import-concurrency=2`。

用户指定选项 → 解析自然语言，映射为 CLI 参数执行。

## 识别逻辑

**必要条件（缺一不可）：** `Handle` 列 + `Title` 列

**充分条件（满足 3/5）：** `Variant Price`、`Image Src`、`Option1 Name`、`Option1 Value`、`Body`（或 `Body (HTML)`）

**排除规则：** 含 `order`+`lineitem` → 订单表；含 `customer`+`email`+`phone` → 客户表

## 列映射（Shopify → Fecify）

| Shopify 列 | Fecify 字段 | 位置 | 备注 |
|------------|------------|------|------|
| Handle | `product.handle` | product | 分组关键字段 |
| Title | `product.title` | product | |
| Body (HTML) | `product.body_html` | product | |
| Vendor | `product.vendor` | product | 选填 |
| Option1/2/3 Name | `options[].name` | options | 自动推断 |
| Option1/2/3 Value | `variants[].option1/2/3` | variants | |
| Variant Price | `variants[].price` | variants | |
| Variant Compare At Price | `variants[].compare_at_price` | variants | 选填 |
| Variant SKU | `variants[].sku` | variants | 缺失自动生成 |
| Variant Grams | `variants[].weight` | variants | 默认 `"0"` |
| Variant Weight Unit | `variants[].weight_unit` | variants | 默认 `"g"` |
| Variant Barcode | `variants[].barcode` | variants | 选填 |
| Image Src | 先上传 → `images[].src` | images | 下载后上传 Fecify |
| Image Position | `images[].position` | images | |
| Image Alt Text | `images[].alt` | images | 选填 |
| Variant Image | `variants[].image` | variants | 取首图 |
| Status | `product.status` | product | active→1, 其他→2 |

## 注意事项

1. `variants[].sku` — 可以为空；导入脚本会为无 SKU 的变体自动生成
2. `variants[].image` — 可以为空；如果填写则须指向 `images[]` 中的 `src`，否则服务端报错
3. `variant_need_image` — `1` 或 `2` 均可

## 并发配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--img-concurrency=N` | 5 | 图片下载上传同时 N 张 |
| `--img-retries=N` | 3 | 单张图片下载失败重试 N 次（间隔 1s→2s→4s 递增） |
| `--import-concurrency=N` | 2 | 同时创建 N 个商品 |

### 服务器规格推荐

| 服务器 | 图片并发 | 商品并发 | 说明 |
|--------|---------|---------|------|
| 2核4G | 5 | 2 | **默认配置**，低配服务器 |
| 4核8G | 10 | 5 | 适合多数批量导入场景 |
| 8核16G | 20 | 10 | 中高配，大批量导入 |
| 16核32G | 30 | 20 | 高配，最大化吞吐 |

> 图片下载为网络 I/O 密集型，商品创建为 API 调用。建议根据实际网络带宽和 Fecify 服务端负载调整。

## 响应判断

两个 API 均遵循 `code === 200` 成功规则：

- 图片上传成功 `code: 200` → `data.path` 为路径
- 商品创建成功 `code: 200` → `data.product_id` 为新 ID
- `code !== 200` → 业务错误，看 `message`
- `code === -1` → 网络/解析错误或 PHP 异常，看 `_raw`

## 大数据量说明

**当前容量**：单次几千个商品、几万行 CSV 可正常处理。

**并发加速**：
- 图片下载上传默认 5 并发，可根据服务器规格调整到 10-15
- 商品创建默认 2 并发，推荐 2-5
- 使用 `--use-network-images` 跳过图片上传可大幅提速

**建议**：
- 超大批量用 `--max` 分批次导入（如每次 200-500 个）
- 查看 [服务器规格推荐](#服务器规格推荐) 选择合适的并发值
- 超大表格（10 万+行）后续可改造为流式解析

## 示例

```
# 检测
node scripts/csv-import/detect-shopify-csv.js ./products_export.csv

# 导入
node scripts/csv-import/import-shopify-csv.js ./products_export.csv
```
