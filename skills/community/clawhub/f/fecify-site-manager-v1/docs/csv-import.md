# CSV 批量导入商品

`scripts/csv-import/` 下按平台组织 CSV 导入工具链。命名规范：`detect-<平台>-csv.js` / `import-<平台>-csv.js`。

## 已支持格式

| 平台 | 检测器 | 导入器 | 文档 |
|------|--------|--------|------|
| Shopify | [detect-shopify-csv.js](../scripts/csv-import/detect-shopify-csv.js) | [import-shopify-csv.js](../scripts/csv-import/import-shopify-csv.js) | [shopify-csv-product-import.md](csv-import/shopify-csv-product-import.md) |
| （阿里巴巴） | — | — | 待开发 |
| （Amazon） | — | — | 待开发 |

## 通用流程

所有平台 CSV 导入遵循**两步交互**：

1. **检测** — 运行对应平台的 `detect-<平台>-csv.js`，展示格式/规格/商品数
2. **确认** — 用户选择选项（数量、图片、Tag、并发）后执行导入

具体平台的操作详情、提示模板、列映射见对应文档。

## 扩展

新增 CSV 格式见 [extending.md](extending.md)。
