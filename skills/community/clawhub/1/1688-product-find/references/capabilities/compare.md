# Capability: compare (商品比价)

## 功能说明
基于用户选中商品的图片或商品链接，通过以图搜图找到同款商品，自动按销量、价格、服务三个维度各选出 1 款代表性商品，生成纵向对比表。

## 触发方式
**Skill 级触发词**: 比价、对比、哪家便宜、找更便宜的、同款低价、进行比较

**Capability 识别特征**:
- 用户上传图片/链接并**明确要求比价**（如“找同款并比价”、“找到同款进行比较”）
- 用户在搜索结果中选定某款商品后要求比价/对比
- 用户使用“比一比”、“哪家便宜”、“低价同款”等关键词

**❗ 商品链接直接比价**：
- 用户给到商品链接且意图包含比价 → 直接使用 `compare --url`，一步到位
- **禁止**先执行 `link_search` 再执行 `compare`，`compare --url` 内部已包含链接解析+主图提取+比价逻辑

**⚠️ 意图判断核心原则**:
- **上传图片/链接时，默认是找同款，使用 `image_search` 或 `link_search`**
- **仅在用户明确提到“比价/比较/对比”时，才使用 `compare`**
- `compare` 命令内部已包含以图搜图/链接解析逻辑，一步到位完成搜索+比价

## 前置条件
- 已配置 AK。**Agent 判断 AK 是否已配置时，必须通过执行 `cli.py configure`（无参数）确认，禁止仅凭环境变量或对话历史判断**。
- 需要商品图片或商品链接（支持以下四种输入方式，二选一）：
  - **URL 图片**：在线图片链接，如 `https://img.alicdn.com/xxx.jpg`
  - **本地图片**：本地文件路径，如 `/path/to/image.jpg`（自动预处理：缩放 + 格式转换）
  - **搜索结果中的图片**：从前序搜索结果的 `image_url` 字段提取
  - **商品链接/ID**：1688/淘宝/天猫商品链接或纯商品 ID（自动解析链接并提取主图）

## CLI 调用（Agent 执行时必须使用）
```bash
python3 {baseDir}/cli.py compare [--image "商品图片URL"] [--url "商品链接"] [--query "附加关键词"] [--limit 3] [--sort price_asc] [--score-level high] [--purchase-amount 1] [--tags 4306497] [--ic-tags ""]
```

> `--image` 和 `--url` 二选一，必须提供其中一个。两者都提供时优先使用 `--image`。

### 命令行参数
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--image` | `-i` | 商品图片 URL 或本地路径（与 `--url` 二选一） | 可选 |
| `--url` | `-u` | 商品链接或商品 ID（自动提取主图，与 `--image` 二选一） | 可选 |
| `--query` | `-q` | 附加关键词（规格、品类等） | 可选 |
| `--platform` | `-p` | 目标平台 | 1688 |
| `--limit` | `-l` | 对比商品数量 | 3 |
| `--sort` | `-s` | 排序方式：`price_asc`(价格低→高)、`price_desc`(价格高→低)、`sold_desc`(销量高→低)、`yx_desc`(严选指数高→低) | 无（默认排序） |
| `--score-level` | - | 相关性档位：`high`(高)、`medium`(中)、`low`(低) | `high` |
| `--purchase-amount` | - | 采购件数（正整数，不支持范围） | `1` |
| `--tags` | - | TC标（品池标签），英文逗号分隔 | `4306497` |
| `--ic-tags` | - | IC标（品池标签），英文逗号分隔 | 无 |

**支持的图片输入格式**：
- URL：`https://xxx.jpg`、`https://xxx.png` 等
- 本地路径：`/path/to/image.jpg`、`C:\Users\image.png` 等（支持 JPG、PNG、GIF、BMP、WEBP 等格式）
- 本地图片会自动预处理：超尺寸自动缩放、非 JPEG 格式自动转换

### 使用示例
```bash
# 场景1：基本比价（一步到位，无需先执行 image_search）
python3 {baseDir}/cli.py compare -i "/path/to/image.jpg" -q "蒙奇奇 15CM 毛绒"

# 场景2：通过商品链接直接比价（一步到位，无需先执行 link_search）
python3 {baseDir}/cli.py compare -u "https://detail.1688.com/offer/895657286458.html"

# 场景3：通过纯商品 ID 比价
python3 {baseDir}/cli.py compare -u "895657286458" -q "不锈钢漏勺"

# 场景4：按价格从低到高排序
python3 {baseDir}/cli.py compare -i "/path/to/image.jpg" -s price_asc

# 场景5：按销量从高到低排序
python3 {baseDir}/cli.py compare -i "/path/to/image.jpg" -s sold_desc

# 场景6：降低相关性要求，召回更多商品
python3 {baseDir}/cli.py compare -i "/path/to/image.jpg" --score-level medium

# 场景7：组合使用 - 按价格排序 + 中等相关性
python3 {baseDir}/cli.py compare -i "/path/to/image.jpg" -s price_asc --score-level medium

# 场景8：使用默认 TOP 3 对比（推荐，不要随意修改 limit）
python3 {baseDir}/cli.py compare -i "https://img.alicdn.com/imgextra/xxx.jpg"

# 场景9：指定采购件数
python3 {baseDir}/cli.py compare -i "/path/to/image.jpg" -q "蒸汽拖把" --purchase-amount 200

# 场景10：完整参数
python3 {baseDir}/cli.py compare -i "/path/to/image.jpg" -q "蒸汽拖把" -l 3 -s yx_desc --score-level high --purchase-amount 100 --tags "4306497"

# 场景11：链接比价 + 关键词
python3 {baseDir}/cli.py compare -u "https://detail.1688.com/offer/895657286458.html" -q "不锈钢漏勺"
```

## 处理流程

### 1. 获取商品图片
- **图片输入**（`--image`）：直接使用图片 URL 或本地路径
- **链接输入**（`--url`）：自动解析商品链接，提取商品主图（复用 link_search 的 LinkParser + ProductImageExtractor）
  - 支持 1688/淘宝/天猫链接及纯商品 ID
  - 提取失败时返回错误提示，建议用户改用 `--image` 参数

### 2. 以图搜图获取同款候选
- 使用商品图片 URL 调用 `/api/find_product/1.0.0` 接口
- 固定搜索 20 条候选商品，确保三维度选品有足够样本
- 若用户提供了 `--query` 关键词，同时传入 API 请求体提升相关性
- 支持通过 `--sort` 参数控制排序方式
- 支持通过 `--score-level` 参数控制相关性档位

### 2. 三维度自动选品
独立评估每个维度的最佳商品（不互斥），同一商品赢得多个维度时合并标签：

| 维度 | 选品策略 | 标签 |
|------|---------|------|
| 销量最高 | 按 `sold_count` 降序取第 1 | "销量最高" |
| 价格最低 | 按 `price` 升序取第 1（排除无价格） | "价格最低" |
| 综合最优 | 按 `yx_index` 倒序取第 1 | "综合最优" |

> **标签合并规则**：当同一商品同时满足多个维度最优时，合并标签展示（如 "销量最高 且 价格最低 且 综合最优"），最终输出的商品数量由去重结果决定（1~3 款），不会用额外商品填充。

### 3. 自适应输出格式
- **3 款不同商品**：标准纵向对比表格（3 列）
- **2 款不同商品**：精简对比表格（2 列），合并标签展示
- **1 款商品**（三维度均为同一商品）：卡片式展示，标签合并为 "销量最高 且 价格最低 且 综合最优"

## 输出格式

### 场景 A：多款商品对比表（2~3 列）
```markdown
| 维度 | 推荐 1 (销量最高) | 推荐 2 (价格最低) | 推荐 3 (综合最优) |
|:-----|:----------------|:----------------|:----------------|
| 商品 | 铂佳无磁不锈钢漏勺... | 加大不锈钢花椒漏勺... | 新款不锈钢汤勺饭店... |
| 💰 单价 | ￥1.19 | ￥3.80 | ￥3.89 |
| 📦 规格 | 20cm 细网 | 25cm 粗网 | 30cm 加密 |
| ⭐ 严选指数 | 85.23 | 72.50 | 90.16 |
| 📊 起批量 | 100件 | 50件 | 200件 |
| 销量 | 1.2万 | 856 | 2340 |
| 库存 | 有货 | 有货 | 有货 |
| 服务 | 7天无理由、48h发货 | 包邮、7天无理由 | 7天无理由 |
| 卖点 | 爆款热销 | 工厂直供 | 品质保障 |
| 供应商 | 义乌XX日用.. | 揭阳XX不锈钢.. | 潮安XX厨具.. |
| 链接 | [查看](url1) | [查看](url2) | [查看](url3) |
```

### 场景 B：标签合并对比表（2 列）
当两个维度指向同一商品时，合并标签展示：
```markdown
| 维度 | 推荐 1 (销量最高 且 综合最优) | 推荐 2 (价格最低) |
|:-----|:---------------------------|:-----------------|
| 商品 | XX商品... | YY商品... |
| ... | ... | ... |
```

### 场景 C：单款商品卡片（1 列）
当三个维度均指向同一商品时，使用卡片式展示：
```markdown
**🏆 销量最高 且 价格最低 且 综合最优**

| 维度 | 详情 |
|:-----|:-----|
| 商品 | XX不锈钢漏勺... |
| 💰 单价 | ￥1.19 |
| 📦 规格 | 20cm 细网 |
| ⭐ 严选指数 | 85.23 |
| 📊 起批量 | 100件 |
| 销量 | 1.2万 |
| 库存 | 有货 |
| 服务 | 7天无理由、48h发货 |
| 卖点 | 爆款热销 |
| 供应商 | 义乌XX日用.. |
| 链接 | [查看](url) |
```

### JSON 输出结构
```json
{
  "success": true,
  "markdown": "纵向比价表 Markdown",
  "data": {
    "data": {
      "success": true,
      "source_image": "图片URL",
      "compare_products": [...],
      "search_type": "compare",
      "total_candidates": 9,
      "total_compared": 3
    }
  }
}
```

## 输出字段说明

### 展示的字段

| 字段名 | API 字段 | 说明 | 示例 |
|--------|---------|------|------|
| 商品 | `title` | 商品标题 | "铂佳无磁不锈钢漏勺..." |
| 💰 单价 | `price` | 商品单价（元） | ￥1.19 |
| 📦 规格 | `sku_title` | 规格详情/SKU 信息 | "20cm 细网" |
| ⭐ 严选指数 | `yx_index` | 严选指数评分（两位小数，截断） | 85.23 |
| 📊 起批量 | `quantity_begin` + `unit` | 起批量（拼接展示） | 100件 |
| 销量 | `sold_count` | 销量数据 | 1.2万 |
| 库存 | `stock_amount` | 库存状态 | 有货/无货 |
| 服务 | `service_infos` | 服务标签列表 | 7天无理由、48h发货 |
| 卖点 | `selling_points` | 卖点标签列表 | 爆款热销 |
| 供应商 | `supplier` | 供应商名称 | 义乌XX日用.. |
| 链接 | `detail_url` | 商品详情页链接 | [查看](url) |

## 代码结构
```
scripts/capabilities/compare/
├── __init__.py      # 模块初始化
├── cmd.py           # CLI 入口
└── service.py       # 核心比价逻辑
    ├── ImagePreprocessor        # 图片预处理器（复用 image_search）
    ├── _count_service_tags()    # 服务标签计数
    ├── _select_top()            # 三维度选品策略
    ├── CompareExecutor          # 比价执行器
    └── compare_products()       # 主入口函数
```

## 错误处理
- **AK 未配置**: 提示用户运行 `cli.py configure YOUR_AK`
- **链接无法提取主图**: 提示用户改用 `--image` 参数直接提供图片 URL
- **链接格式无效**: 抛出 `ValueError("无法识别的商品 ID 格式")`
- **两个参数都未提供**: 抛出 `ValueError("必须提供 --image 或 --url 参数")`
- **图片路径无效**: 提示用户检查图片路径是否存在
- **API 格式异常**: 抛出 `ServiceError("格式异常，请稍后重试")`
- **无匹配商品**: 返回 `success: true`，markdown 显示"未找到可比价的同款商品"

## 依赖关系
- `_http.search_products`: 商品搜索公共接口
- `_auth.get_ak_from_env`: AK 认证（cmd.py 层调用）
- `_errors.ServiceError`: 错误处理
- `_output.print_output/print_error/format_compare_table`: 输出格式化
- `ImagePreprocessor`: 图片预处理（复用 image_search 逻辑）
- `LinkParser` / `ProductImageExtractor`: 链接解析和主图提取（复用 link_search 逻辑）

## 注意事项
1. **意图判断**：
   - ✅ 用户上传图片 + “找同款” → 使用 `image_search`
   - ✅ 用户上传图片 + “找同款并比价” → 使用 `compare --image`
   - ✅ 用户给链接 + “找同款并比价” → 使用 `compare --url`
   - ✅ 搜索结果展示后，用户选中某款说“比价” → 使用 `compare --image`（从结果提取 image_url）
2. `--image` 参数来源：
   - 用户直接上传的本地图片路径（用户说“找这款并比价”）
   - 前序搜索结果的 `image_url` 字段（用户已选中某款商品后要求比价）
   - 商家指定的图片 URL
3. `--url` 参数来源：
   - 用户提供的商品链接（如 `https://detail.1688.com/offer/xxx.html`）
   - 纯商品 ID（如 `895657286458`）
4. `--query` 参数用于传入用户提到的规格、品类等附加条件，提升搜索相关性
5. **默认返回 TOP 3**，Agent 不应擅自修改 `--limit`，除非用户明确要求
6. **排序参数**：`--sort` 可选，不传则使用 API 默认排序（相关性）
7. **相关性档位**：`--score-level` 默认 `high`，如果高相关性结果不足，可提示用户是否降低为 `medium` 或 `low`
8. **不存在浏览器降级方案**，AK 缺失或 API 失败时只能返回错误提示
9. **🚫 常见错误**：
   - ❌ 错误：用户上传图片说“找同款” → 执行 `compare`（应该用 `image_search`）
   - ✅ 正确：用户上传图片说“找同款” → 执行 `image_search`
   - ❌ 错误：用户上传图片说“找同款并比价” → 先 `image_search` 再 `compare`
   - ✅ 正确：用户上传图片说“找同款并比价” → 直接 `compare --image <path>`
   - ❌ 错误：用户给链接说“比价” → 先 `link_search` 再 `compare`
   - ✅ 正确：用户给链接说“比价” → 直接 `compare --url <link>`
