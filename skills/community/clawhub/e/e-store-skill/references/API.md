# e-store Access API — 完整接口参考

> 由 [`../SKILL.md`](../SKILL.md) 按需引用。常规搜索 / 详情 / 下载流程不需要读本文 —— 它存在的目的是覆盖那些主 skill 没说清楚的边界情况。

---

## 基础约定

- **Base URL**：默认 `https://store-api.liganma.com`，可由 `E_STORE_BASE_URL` 覆盖。
- **认证**：通过 URL 查询参数 `ak=<your-ak>`（每个请求都要带）。
- **响应包装**：`{"code": 200, "msg": "success", "data": <payload>}`；非 200 即逻辑错误，向上展示 `msg`。
- **方法**：全部为 `GET`。
- **Long 字段**（任何 `id`、`productId`、`versionId`、`solutionId` 等）**以字符串形式返回**，避免 JavaScript 精度丢失。
- **日期格式**：`yyyy/MM/dd HH:mm:ss`。
- **分页响应**：`SimplePage` 形态 —— `{ pageNum, pageSize, total, pages, list }`。
- **自描述**：所有响应自带 `_dataInfo`（每个字段的中文说明）；入口接口 `/access` 自带 `_usage`（接口清单）。**可以现场调 `/access` 自我发现**，无需翻外部文档。

---

## 接口清单（共 12 个，全部 GET）

根路径：`{baseURL}/access`。

### 资源（Product）

| # | 端点 | 必填参数 | 可选参数 |
|---|------|----------|----------|
| 1 | `/product/search` | — | `keyword`、`notInLib`（默认 `true`：全部 / `false`：仅库中）、`pageNum`（默认 1）、`pageSize`（默认 10，5~200） |
| 2 | `/product/detail` | `id` | — |
| 3 | `/product/versions` | `productId` | `pageNum`（默认 1）、`pageSize`（默认 20） |
| 4 | `/product/download` | `id` | — |
| 5 | `/product/version/download` | `versionId` | — |
| 6 | `/product/config` | `id` | — |
| 7 | `/product/version/config` | `versionId` | — |

### 方案（Solution）

| # | 端点 | 必填参数 | 可选参数 |
|---|------|----------|----------|
| 8 | `/solution/search` | — | `keyword`、`notInLib`、`pageNum`、`pageSize` |
| 9 | `/solution/detail` | `id` | — |
| 10 | `/solution/versions` | `solutionId` | `pageNum`、`pageSize` |
| 11 | `/solution/download` | `id` | — |
| 12 | `/solution/version/download` | `versionId` | — |

> 资源 / 方案路径完全对称：把 `product` 换成 `solution` 即可。

---

## 典型调用

### 搜索资源

```
GET {baseURL}/access/product/search?ak={ak}&keyword=Spring&notInLib=true&pageNum=1&pageSize=10
```

`notInLib=true` 返回所有已发布资源；`notInLib=false` 只返回当前用户库里的。

### 资源详情

```
GET {baseURL}/access/product/detail?ak={ak}&id=1001
```

嵌套字段含 `category`（分类）、`creator`（作者）、`version`（当前版本）。

### 版本列表

```
GET {baseURL}/access/product/versions?ak={ak}&productId=1001&pageNum=1&pageSize=20
```

只返回 `publish` 状态的版本。

### 下载（`hasFile=true` 的版本）

```
GET {baseURL}/access/product/download?ak={ak}&id=1001
```

`data.downloadLink` 是**临时签名链接**，立即用，不要缓存。

### 配置获取（`hasFile=false` 的版本）

```
GET {baseURL}/access/product/config?ak={ak}&id=1001
GET {baseURL}/access/product/version/config?ak={ak}&versionId=3001
```

`data.config` 是配置文本（如 MCP server JSON）。**调用前先看版本的 `hasFile` 字段**判断走 download 还是 config。

### 入口（自描述）

```
GET {baseURL}/access?ak={ak}
```

返回接口清单和字段说明。在你忘记某个端点名 / 参数时直接调一次比翻文档更快。

---

## 注意事项

1. 搜索接口仅返回 `published` 状态的内容。
2. `notInLib=false` 只对绑定到有效用户的 ak 生效。
3. 下载链接有时效，必须立即使用。
4. 方案 `detail` 的 `products` 字段是**该方案发布时的资源快照**，不是实时引用。
5. 路径上资源 / 方案完全对称：`product` ↔ `solution`。
6. 纯配置版本（`hasFile=false`）必须走 `/product/config` 或 `/product/version/config`，不能调 download。
7. 所有 `id` 类字段以字符串形式返回，**永远当字符串拼参数**，不要在 JS 里 `parseInt`。
8. 鉴权失败、参数缺失、模型不存在等业务错误**仍会返回 HTTP 200**，需用 `code` 字段判断成功与否。

---

## 错误处理速查

| 现象 | 可能原因 |
|------|----------|
| HTTP 401 / `code` 表示未鉴权 | `ak` 缺失 / 失效 / 错误 |
| `code` 非 200，`msg=参数错误` | 缺必填参数；`pageSize` 越界（5~200） |
| `code=…`，`msg=资源不存在` | id 错误或资源未发布 |
| download 接口报错 `非可下载版本` | 版本 `hasFile=false`，改用 config 接口 |
| 下载链接 403 / 404 | 链接已过期，重新调 download 生成新链接 |

---

## 客户端脚本对照

仓库内 `scripts/client.py` / `scripts/client.js` 已封装上述全部端点。函数命名一一对应：

| HTTP 端点 | Python 函数 | Node 函数 | CLI 命令 |
|-----------|-------------|------------|----------|
| `/access` | `usage()` | `usage()` | `usage` |
| `/product/search` | `product_search()` | `productSearch()` | `product-search` |
| `/product/detail` | `product_detail()` | `productDetail()` | `product-detail` |
| `/product/versions` | `product_versions()` | `productVersions()` | `product-versions` |
| `/product/download` | `product_download()` | `productDownload()` | `product-download` |
| `/product/version/download` | `product_version_download()` | `productVersionDownload()` | `product-ver-download` |
| `/product/config` | `product_config()` | `productConfig()` | `product-config` |
| `/product/version/config` | `product_version_config()` | `productVersionConfig()` | `product-ver-config` |
| `/solution/search` | `solution_search()` | `solutionSearch()` | `solution-search` |
| `/solution/detail` | `solution_detail()` | `solutionDetail()` | `solution-detail` |
| `/solution/versions` | `solution_versions()` | `solutionVersions()` | `solution-versions` |
| `/solution/download` | `solution_download()` | `solutionDownload()` | `solution-download` |
| `/solution/version/download` | `solution_version_download()` | `solutionVersionDownload()` | `solution-ver-download` |
| — | `search_all()`（资源+方案合搜） | `searchAll()` | `search` |

脚本零依赖（仅用 Python stdlib / Node 内置 `https`），可直接 import 进任意工作流。
