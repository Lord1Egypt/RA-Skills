# 扩展指南

## 新增业务模块

以新增"专辑 (Collections)"为例：

1. 在 `docs/` 下创建 `collections.md`（模块汇总）
2. 创建 `docs/collections/` 子目录，每个 API 一个 `.md`
3. 汇总文件含：API 一览表、各 API 的"何时用"提示、命令示例、详细文档链接
4. 在 [SKILL.md](../SKILL.md) 的模块速查表中新增一行

## 新增 CSV 格式支持

以「阿里巴巴 CSV」为例，参照 Shopify 的完整实现模式。

### 文件清单

新增一个格式需要创建以下文件：

```
docs/csv-import/
  alibaba-csv-product-import.md    ← 平台文档（参照 shopify-csv-product-import.md）
scripts/csv-import/
  detect-alibaba-csv.js            ← 格式检测器
  import-alibaba-csv.js            ← 导入器
```

### 1. 创建检测器 `scripts/csv-import/detect-<平台>-csv.js`

命名规范：`detect-<平台>-csv.js`，`<平台>` 为小写英文名 (`alibaba`、`amazon`、`shopee`)。

#### 1.1 输出 JSON 格式

```json
{
  "format": "alibaba",          // 小写平台名
  "variant": "product",         // "product" | "non-product" | "unknown"
  "subType": "multi-spec",      // "single-spec" | "multi-spec"
  "confidence": 95,             // 0-100
  "totalProducts": 200,
  "singleSpecProducts": 50,
  "multiSpecProducts": 150,
  "maxVariantsPerProduct": 12,
  "extraColumns": ["...", "..."],
  "sample": [{...}, {...}, {...}]   // 前 3 个有效数据行
}
```

#### 1.2 核心函数

| 函数 | 职责 |
|------|------|
| `parseCSV(text)` | 引号感知的 CSV 解析，返回 `string[][]` |
| `headerScore(headers)` | 特征匹配打分，返回 `{ match, confidence, reason, extraColumns }` |
| `isProductTable(headers)` | 排除非商品表（订单/客户表等） |
| `detectVariant(rows, headers)` | 单/多规格判断，返回 `{ multiSpec, singleVariantProducts, multiVariantProducts, totalProducts, maxVariants }` |

#### 1.3 检测规则设计

- **必要条件**（缺一即 `format: "unknown"`）：该平台 CSV 必定存在的列名
- **充分条件**：辅助列，满足一定比例（如 ≥60%）即可判定
- **排除规则**：避免与其他格式冲突（如含 `order`+`lineitem` 判定为订单表）

> 参考 `detect-shopify-csv.js` 的 `SHOPIFY_PRODUCT_SIGNATURES` 和 `NON_PRODUCT_SIGNATURES` 设计。

#### 1.4 单/多规格判断

根据该平台 CSV 判断商品是单规格还是多规格：
- 单规格：对应的 Option 列为"Title"/"Default Title" 模式，变体仅 1 个
- 多规格：有真实规格名和值，或变体数 > 1
- **注意**：标签含多图的行，Option 字段可能为空，不算变体

### 2. 创建导入器 `scripts/csv-import/import-<平台>-csv.js`

命名规范：`import-<平台>-csv.js`。

#### 2.1 必须实现的功能

| 功能 | 函数 | 说明 |
|------|------|------|
| CSV 解析 | `parseCSV(text)` | 引号感知 |
| 列映射 | `buildColumnMap(headers)` | 平台列名 → 内部 key，大小写容错 |
| 按分组拆分 | `groupByHandle(rows, colMap)` | 将行按分组键（如 Handle）聚合成产品 |
| 图片处理 | `uploadImages(images, title, concurrency, retries)` | 下载 + 上传到 Fecify，并发 + 重试 |
| 构建 JSON | `buildFecifyJSON(product, images)` | 平台数据 → Fecify `POST /api/skill/product/create` 请求体 |
| Tag 生成 | `generateTags(title, bodyHtml, count)` | 关键词提取 + 去停用词 |
| 失败存档 | `saveFailure(title, handle, body, response, error)` | 失败商品 → `temp/failed/` |
| Temp 清理 | `cleanupTemp(dir, maxAgeMs)` | 7 天自动清理 |
| 并发工具 | `concurrentMap(items, concurrency, fn)` | 并发池执行器 |

#### 2.2 必须支持的 CLI 参数

```
node scripts/csv-import/import-<平台>-csv.js <CSV文件> [选项]
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--max=N` | int | Infinity | 最大导入数量 |
| `--dry-run` | flag | false | 只生成 JSON，不调 API |
| `--use-network-images` | flag | false | 跳过上传，用原 URL |
| `--gen-tags=none\|auto\|force` | string | none | Tag 生成模式 |
| `--tag-count=N` | int | 3 | Tag 数量 |
| `--img-concurrency=N` | int | 5 | 图片并发数 |
| `--img-retries=N` | int | 3 | 图片重试次数 |
| `--import-concurrency=N` | int | 2 | 商品导入并发数 |

#### 2.3 buildFecifyJSON 构建要点

构建函数将平台数据转为 Fecify 创建 API 的参数，结构：

```js
{
  product: { title, body_html, type, status, handle, vendor, meta_title, ... },
  images: [{ src, position, alt, width, height, ratio }, ...],
  variants: [{ price, qty, weight, weight_unit, sku, image, option1, option2, option3, ... }, ...],
  options: [{ name, position, items: [...] }, ...],   // 多规格时填充
  tags: [{ id: '', title: '...' }, ...],
  collection_ids: [],
  videos: [],
  productattr_info: [],
  mergeimages: []
}
```

关键映射：
- `product.type` — `1` 单规格 / `2` 多规格
- `variants[].sku` — 可选，缺失需自动生成
- `variants[].image` — 取首图 `images[0].src`，可为空
- `images[]` — 需先上传到 Fecify 获取 `path`

> 参考 `import-shopify-csv.js` 的 `buildFecifyJSON` 和 `groupByHandle` 实现。

#### 2.4 主流程结构

```js
async function main() {
  cleanupTemp(TEMP_DIR);           // 清理过期 temp
  解析 CLI 参数;                     // max, dryRun, useNetworkImages, 并发, tag
  解析 CSV 文件;                     // parseCSV + buildColumnMap
  分组产品;                          // groupByHandle
  
  打印并发配置;
  
  await concurrentMap(products, importConcurrency, async (product) => {
    判断单/多规格;
    处理图片（上传 或 直接用 URL）;
    buildFecifyJSON();
    处理 Tag（none/auto/force）;
    POST 创建商品;
    记录结果（成功/失败存档）;
  });

  打印汇总报告;
  保存汇总 JSON;
}
```

### 3. 创建平台文档 `docs/csv-import/<平台>-csv-product-import.md`

参照 [shopify-csv-product-import.md](csv-import/shopify-csv-product-import.md)，需包含：

| 节 | 内容 |
|----|------|
| 涉及文件 / 涉及 API | 该平台的检测器、导入器、调用的 API |
| 何时用 | 触发场景 |
| 导入流程 | Step 1 检测 → Step 2 执行，含 CLI 命令 |
| 用户交互提示 | 检测通过后向用户展示的选项模板 |
| 识别逻辑 | 必要条件、充分条件、排除规则 |
| 列映射 | 平台列 → Fecify 字段对照表 |
| 注意事项 | 该平台的坑和特殊处理 |
| 并发配置 | 服务器规格推荐表 |
| 大数据量说明 | 容量和分批次建议 |

### 4. 接入系统

完成后更新以下文件：

| 文件 | 操作 |
|------|------|
| [csv-import.md](csv-import.md) | 表格新增一行：平台 / 检测器 / 导入器 / 文档 |
| [SKILL.md](../SKILL.md) | 两步交互命令中加入新格式的 detect 命令参考 |

### 5. 开发检查清单

- [ ] 检测器 CLI 可运行，输出 `{ format, confidence, totalProducts, subType, sample }`
- [ ] 检测器能区分商品表 / 非商品表
- [ ] 检测器能正确判断单/多规格数量
- [ ] 检测器跳过图片行，不误判为变体
- [ ] 导入器支持 `--max`、`--dry-run` 等所有标准 CLI 参数
- [ ] `--dry-run` 生成正确的 Fecify JSON
- [ ] 单规格商品 `product.type = 1`，`options = []`
- [ ] 多规格商品 `product.type = 2`，`options` 正确填充
- [ ] `product.handle` 不为空
- [ ] 图片处理支持上传和网络图两种模式
- [ ] 失败商品自动存档到 `temp/failed/`
- [ ] 导入结束输出汇总（成功/失败数）
- [ ] 平台文档覆盖所有章节
- [ ] 所有引用文件已更新

## 已有格式

| 格式 | 检测器 | 导入器 | 文档 |
|------|--------|--------|------|
| Shopify | `detect-shopify-csv.js` | `import-shopify-csv.js` | [shopify-csv-product-import.md](csv-import/shopify-csv-product-import.md) |
| 阿里巴巴 | 待开发 | 待开发 | 待开发 |
| Amazon | 待开发 | 待开发 | 待开发 |
