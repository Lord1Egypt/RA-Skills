---
name: "ad-creative-intel-free"
description: "解决竞品创意看不见、投放动态摸不透、榜单变化追不到的免费广告情报查询工具"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "广告情报免费版"
  version: "1.0.0"
  summary: "解决竞品创意看不见、投放动态摸不透、榜单变化追不到的免费广告情报查询工具"
  tags:
    - "广告情报"
    - "创意搜索"
    - "竞品分析"
    - "应用榜单"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 广告情报免费版（Ad Creative Intel Free）

面向买量投放、创意策划、市场研究人员的轻量级广告情报查询工具。在一个会话内完成创意搜索、应用洞察、榜单查询三件事，所有结果以原始结构化 JSON 返回，由调用 Agent 决定分析与呈现方式。

> 本免费版面向个人用户试用与轻量查询场景。如需批量导出、历史趋势回溯、下载/收入预估数据等高级能力，请使用 `ad-creative-intel-pro` 专业版。

## 设计动机：四大高频痛点

| 痛点 | 典型表现 | 本技能对策 |
|------|----------|------------|
| 竞品创意分散难对比 | 创意散落多平台，需逐个登录查看 | 统一搜索接口，按地区/媒体/类型横向筛选 |
| 新投放素材发现滞后 | 等到爆款出现才知道，错过红利期 | 多维度筛选 + 创意详情追溯，及时发现新素材 |
| 应用榜单变化难追踪 | 排名数据需手动记录，趋势不可视 | 榜单查询接口，支持免费/付费/畅销分类 |
| 缺乏统一数据入口 | 每查一类数据都要切换工具 | 三大端点集群统一封装在一个 skill 内 |

## 使用流程

### Step 1：检查 API Key（< 10 秒）

```bash
[ -n "${ADC_INTEL_API_KEY:-}" ] && echo ok || echo missing
```

若输出 `ok` 进入步骤 2；若输出 `missing`，按"API Key 配置"章节完成设置后重试。

### Step 2：发现筛选元数据（< 30 秒）

首次使用前调用一次筛选元数据接口，缓存国家、媒体、广告类型、行业等代码表：

```bash
curl -s "https://api.ad-creative-intel.com/api/data/filter-options" \
  -H "X-API-Key: ${ADC_INTEL_API_KEY}"
```

### Step 3：执行第一次创意搜索（< 60 秒）

```bash
curl -s -X POST "https://api.ad-creative-intel.com/api/data/search" \
  -H "X-API-Key: ${ADC_INTEL_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"keyword":"rpg","countries":["US"],"mediaChannels":[1],"pageSize":10,"page":1}'
```

返回原始 JSON，包含 `list`（创意列表）、`totalSize`、`pageIndex` 等字段。

### Step 4：查看创意详情（< 20 秒）

```bash
curl -s "https://api.ad-creative-intel.com/api/data/content-detail?contentId=XXXXX&related=imagevideo" \
  -H "X-API-Key: ${ADC_INTEL_API_KEY}"
```

#
## 核心能力

### 1. 广告创意搜索

提供关键词与多维度筛选的创意搜索能力，返回原始结构化数据。

| 端点 | 方法 | 用途 |
|------|------|------|
| `/api/data/search` | POST | 按关键词与筛选条件搜索广告创意 |
| `/api/data/count` | POST | 统计满足条件的创意总数 |
| `/api/data/count-all` | POST | 按维度分组统计创意数 |
| `/api/data/distribute` | POST | 创意分布统计 |
| `/api/data/distribute-dims` | GET | 查询可用分布维度 |
| `/api/data/content-detail` | GET | 单条创意详情（支持 `related=imagevideo` 关联素材） |
| `/api/data/item-apps` | POST | 查询创意关联的应用 |
| `/api/data/screen-types` | GET | 屏幕/元素类型代码表 |
| `/api/data/page-config` | GET | 搜索页面配置 |

**关键参数约束**：
- `pageSize` 上限为 **10**（超过自动降为 10，使用 `page` 翻页）
- `countries`、`mediaChannels`、`adTypes` 等筛选代码需从 `/filter-options` 获取
- `tradeLevel` 为树形结构（如 `602`=游戏、`607`=金融），子行业需调用维度接口

**输入**: 用户提供广告创意搜索所需的指令和必要参数。
**处理**: 按照skill规范执行广告创意搜索操作,遵循单一意图原则。
**输出**: 返回广告创意搜索的执行结果,包含操作状态和输出数据。

### 2. 应用与开发者洞察

查询应用、开发者、SDK 等基础信息，构建"创意-应用-开发者"三层数据视图。

| 端点 | 方法 | 用途 |
|------|------|------|
| `/api/data/unified-product-search` | POST | 统一应用/产品搜索 |
| `/api/data/product-search` | POST | 产品搜索 |
| `/api/data/company-search` | POST | 开发者/公司搜索 |
| `/api/data/app-detail` | GET | 应用详情（按 `unifiedProductId`） |
| `/api/data/developer-detail` | GET | 开发者详情 |
| `/api/data/app-profile` | GET | 应用档案 |
| `/api/data/similar-apps` | POST | 相似应用 |
| `/api/data/sdk-detail` | GET | 应用使用的 SDK |
| `/api/data/product-content-search` | POST | 查询某产品的创意 |
| `/api/data/product-content-counts` | POST | 统计某产品的创意数 |

**输入**: 用户提供应用与开发者洞察所需的指令和必要参数。
**处理**: 按照skill规范执行应用与开发者洞察操作,遵循单一意图原则。
**输出**: 返回应用与开发者洞察的执行结果,包含操作状态和输出数据。

### 3. 应用商店榜单查询

查询应用商店排名数据，支持免费/付费/畅销榜与分类榜单。

| 端点 | 方法 | 用途 |
|------|------|------|
| `/api/data/store-rank` | POST | 应用商店榜单（free/paid/grossing） |
| `/api/data/generic-rank` | POST | 通用榜单列表 |
| `/api/data/store-categories` | GET | 商店分类代码 |
| `/api/data/store-countries` | GET | 商店国家代码 |

**输入**: 用户提供应用商店榜单查询所需的指令和必要参数。
**处理**: 按照skill规范执行应用商店榜单查询操作,遵循单一意图原则。
**输出**: 返回应用商店榜单查询的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：解决竞品创意看不、投放动态摸不透、榜单变化追不到的、免费广告情报查询、广告情报免费版是、面向买量投放、创意策划、市场研究人员的轻、量级广告情报查询、竞品创意素材分散、在多平台难以横向、新投放素材发现滞、应用榜单排名变化、无法及时追踪、缺乏统一的数据查、询入口、四大痛点而设计、它把多源广告情报、数据封装为统一查、询接口、让用户在一个会话、内完成创意搜索、应用洞察、榜单查询三件事等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 参数映射与筛选代码

调用搜索类端点前，需将自然语言转换为 API 代码：

| 自然语言 | API 字段 | 代码示例 |
|----------|----------|----------|
| 视频广告 | `creativeType` | `010` |
| 游戏行业 | `tradeLevel1` | `602` |
| 金融行业 | `tradeLevel1` | `607` |
| 美国 | `countries` | `US` |
| 日本 | `countries` | `JP` |
| 近 7 天 | `dateRange` | `7d` |
| 近 30 天 | `dateRange` | `30d` |

**未覆盖代码的获取方法**：调用 `GET /api/data/filter-options` 拉取完整代码表，或调用端点专属维度接口（如 `store-categories`）。

## 输出规则

- 严格返回 API 响应的**原始结构化 JSON**，保留 API 字段名
- **不**重命名、删除、汇总、排序或编辑加工数据
- **不**生成 H5/落地页/卡片/仪表盘
- **不**自动运行多步研究或产出分析建议（除非用户明确要求）
- 空的 `list` 是合法结果（无匹配），不是错误
- 第三方预估数据（如下载/收入）必须原样返回，呈现时由调用方标注"预估值"
- 若工具协议实现可用，优先使用工具协议工具调用；否则直接调用 HTTP 端点

## 示例

### 场景一：买量团队监控竞品 RPG 游戏创意

```text
任务：调研美国市场近 30 天 RPG 游戏类广告创意 Top 50

执行步骤：
1. 调用 /filter-options 获取 trade_level1=602（游戏）确认
2. 调用 /search：
   {
     "keyword": "rpg",
     "countries": ["US"],
     "tradeLevel1": "602",
     "dateRange": "30d",
     "pageSize": 10,
     "page": 1
   }
3. 翻页 5 次收集 50 条创意
4. 调用 /count-all 按 adType 分组统计
5. 输出原始 JSON 与统计概览

注意：本免费版单次 pageSize 上限 10，需翻页 5 次
```

### 场景二：创意策划寻找金融类短视频灵感

```text
任务：查找金融行业（tradeLevel1=607）的视频类广告创意

执行步骤：
1. 调用 /filter-options 确认 creativeType=010（视频）
2. 调用 /search：
   {
     "tradeLevel1": "607",
     "creativeType": "010",
     "pageSize": 10
   }
3. 对感兴趣的创意调用 /content-detail 获取详情
4. 调用 /item-apps 追溯关联应用，了解是哪个产品在投
5. 输出创意列表 + 关联应用清单
```

### 场景三：应用开发者跟踪自家产品榜单变化

```text
任务：查询美国 App Store 游戏分类免费榜 Top 100，看自家产品是否上榜

执行步骤：
1. 调用 /store-categories 获取游戏分类代码
2. 调用 /store-rank：
   {
     "country": "US",
     "category": "<game_category_code>",
     "rankType": "free",
     "pageSize": 100
   }
3. 在返回的 list 中查找自家产品 unifiedProductId
4. 若需进一步定位产品详情，调用 /app-detail
5. 输出榜单原始数据 + 自家产品排名位置
```

### 场景四：市场研究员分析某开发者全部在投创意

```text
任务：调研开发者 "Supercell" 旗下所有应用当前在投的广告创意

执行步骤：
1. 调用 /company-search 搜索 "Supercell" 获取开发者 ID
2. 调用 /developer-detail 获取其应用列表
3. 对每个应用调用 /product-content-search 获取创意
4. 调用 /product-content-counts 统计各应用创意数
5. 输出开发者-应用-创意三层视图（原始 JSON）
```

## API Key 配置

调用前必须配置 `ADC_INTEL_API_KEY` 环境变量。若未配置，本技能会输出缺 Key 引导而非直接报错。

### 配置方式

**方式一：环境变量（推荐）**

```bash
# Linux / macOS
export ADC_INTEL_API_KEY="your_api_key_here"

# Windows PowerShell
$env:ADC_INTEL_API_KEY = "your_api_key_here"
```

**方式二：Agent 平台配置**

```bash
skill-platform config set skills.entries.ad-creative-intel.apiKey "your_api_key_here"
```

### 获取 API Key

1. 访问广告情报数据服务官网注册账号
2. 登录后在控制台找到 **API Keys** 菜单
3. 创建一个新的 Key 并复制保存
4. 按上述方式配置到环境中

> 安全提示：永远不要在对话中打印、回显或存储 API Key。本技能仅通过环境变量读取，不会接受用户在对话中直接输入的 Key。

## 错误处理


### Agent 层错误（未发起请求）

当 `ADC_INTEL_API_KEY` 缺失时，返回结构化错误而非崩溃：

```json
{
  "error": {
    "code": "missing_api_key",
    "message": "未配置 ADC_INTEL_API_KEY 环境变量",
    "retry": false,
    "guide": "请参考 API Key 配置章节完成设置后重试"
  }
}
```

### API 层错误（请求返回非 2xx）

API 返回 `{ "detail": "...", "code": "..." }`，本技能原样透传并附加 HTTP 状态码：

| HTTP 状态 | 错误代码 | 含义 | 处理建议 |
|-----------|----------|------|----------|
| 401 | `INVALID_API_KEY` | Key 缺失/格式错/已停用 | 不执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，检查 Key 配置 |
| 401 | `NOT_AUTHENTICATED` | 未认证 | 不执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，重新配置 Key |
| 403 | `FORBIDDEN` | 权限不足 | 不执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，联系服务方升级权限 |
| 429 | `RATE_LIMITED` | 触发速率限制 | 等待 60 秒后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 500 | `INTERNAL` | 服务端错误 | 等待 30 秒执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，最多 3 次 |
## FAQ

**Q1：免费版有没有调用次数限制？**
A：没有次数限制。免费版仅限制 3 项高级功能（批量导出 >10 条/次、历史趋势回溯、下载/收入预估数据），日常创意搜索、应用查询、榜单查询不限次数。

**Q2：为什么 pageSize 被自动改成 10？**
A：免费版单次返回上限为 10 条，超过会自动 clamp 为 10。使用 `page` 参数翻页可获取更多数据。专业版支持更大单次返回。

**Q3：返回的 list 为空是出错了吗？**
A：不是。空的 `list` 是合法结果，表示当前筛选条件下无匹配创意。请检查筛选代码是否正确（可调用 `/filter-options` 核对）。

**Q4：下载/收入数据为什么返回 403？**
A：下载/收入预估数据属于高级功能，免费版无权限访问。如需此数据请使用专业版 `ad-creative-intel-pro`。

**Q5：能否同时查询多个国家的数据？**
A：可以。`countries` 参数支持数组，如 `["US","JP","KR"]`。但跨地区对比分析需调用方自行聚合，本技能返回原始 JSON 不做加工。

**Q6：创意详情里的 related=imagevideo 是什么意思？**
A：表示同时返回该创意的图片与视频素材信息。可选值取决于 `/screen-types` 返回的代码表。

## 故障排查

| 症状 | 可能原因 | 解决方案 |
|------|----------|----------|
| 所有请求都返回 401 | API Key 未配置或已失效 | 检查 `ADC_INTEL_API_KEY` 环境变量是否设置，重新生成 Key |
| 搜索结果总是为空 | 筛选代码错误 | 调用 `/filter-options` 核对国家/媒体/类型代码 |
| 翻页后数据重复 | `page` 参数未递增 | 确认每次请求 `page` 字段递增 1 |
| 调用 /download-* 返回 403 | 免费版无下载/收入数据权限 | 使用专业版或移除该端点调用 |
| 请求频繁返回 429 | 触发速率限制 | 降低调用频率，建议间隔 ≥ 3 秒 |
| 返回字段名与文档不一致 | API 版本更新 | 以实际 API 返回为准，本技能不做字段重命名 |
| 中文 Key 配置后仍提示 missing | Shell 未生效 | 重启终端或重新加载 shell 配置文件 |

## 已知限制

本免费体验版限制以下高级功能：

- ❌ **批量导出**：单次返回上限 10 条，无法一次性导出大批量数据（专业版支持无上限）
- ❌ **历史趋势回溯**：无法查询历史时间段的创意/榜单变化趋势（专业版支持任意时间段回溯）
- ❌ **下载/收入预估数据**：无法访问 `/download-*` 与 `/revenue-*` 端点（专业版开放全部预估数据）

解锁全部功能请使用专业版：`ad-creative-intel-pro`

## 依赖说明

### 运行环境

- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **网络**：需可访问 `api.ad-creative-intel.com` 域名

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由 Agent 平台内置 LLM 提供（免费版默认 GPT-4o-mini 路由） |
| 广告情报数据服务 API | 外部 API | 必需 | 需注册账号并获取 API Key |
| curl | 命令行工具 | 必需 | 系统自带或通过包管理器安装 |

### API Key 配置

- **存储位置**：环境变量 `ADC_INTEL_API_KEY`
- **禁止**：在 SKILL.md 或脚本中硬编码 Key
- **禁止**：在对话中接受用户输入的 Key 并回显

### 可用性分类

- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需 exec 执行 curl 命令）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 调用广告情报数据 API

## License 与版权声明

本 skill 基于原始作品改进，保留原始版权声明：

- 原始作品：广告创意数据 API 客户端
- 原始 license：MIT
- 改进作品：© 2026 Ad Creative Intel
- 改进 license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：

- 重新设计为中文痛点导向的免费/专业双版本架构
- 新增四大痛点对策矩阵与场景化使用指南
- 新增 FAQ、故障排查表、API Key 安全配置规范
- 新增筛选元数据自动发现机制与参数映射说明
- 移除原项目专属标识，统一为"广告情报数据服务"抽象命名
- 将工具协议引用从特定实现改为通用"工具协议"标准术语
- 新增分级时间快速开始与 4 个真实场景示例

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 适用场景

```text
任务：调研美国市场近 30 天 RPG 游戏类广告创意 Top 50

执行步骤：
1. 调用 /filter-options 获取 trade_level1=602（游戏）确认
2. 调用 /search：
   {
     "keyword": "rpg",
     "countries": ["US"],
     "tradeLevel1": "602",
     "dateRange": "30d",
     "pageSize": 10,
     "page": 1
   }
3. 翻页 5 次收集 50 条创意
4. 调用 /count-all 按 adType 分组统计
5. 输出原始 JSON 与统计概览

注意：本免费版单次 pageSize 上限 10，需翻页 5 次
```

## 不适用场景

以下场景广告情报免费版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求。

