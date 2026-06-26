---
name: bond-information
description: |
  债券资讯与信用风险监测技能。基于 FEEDAX API 查询债券市场相关新闻资讯，支持按债券类型（城投债/公司债/企业债/金融债等）、情感倾向、时间范围筛选，提供债券违约风险监测、信用评级追踪、发行人舆情分析等专业功能。
  
  使用场景：用户监测债券违约风险、追踪城投债舆情、分析公司债信用状况、查询特定债券新闻、评估债券发行人风险、了解债券市场动态、进行债券投资风险预警等。
  
  触发示例："查询城投债最新舆情"、"某公司债券违约风险"、"20 万科 01 债券新闻"、"近期债券违约事件"、"城投债负面消息"、"公司债信用评级变化"、"债券发行人舆情"等。
  
  支持按债券类型筛选，按情感倾向过滤，返回债券名称、发行人、情感得分、相关性分析等多维度数据。
---

# 债券资讯 (Bond Information)

基于 FEEDAX API 的债券资讯与信用风险监测技能，提供全面的债券舆情查询能力。

## ⚠️ 前置条件：配置 API Key

**使用本技能前，必须先配置 API Key。**

### 检查配置

查看 `.env` 文件是否存在且包含有效的 API Key：

```bash
cat .env
```

### 如果未配置

返回以下错误提示：

> **GE1003**: 未配置 API Key，请前往 https://www.feedax.cn 免费申请，完成后请告诉我 API Key 以便我记住

在 `.env` 文件中添加：

```env
FEEDAX_API_KEY=your_api_key_here
```

> **注意**: 如果 `.env` 文件不存在，请创建该文件并添加上述内容。API Key 请联系管理员获取。

### API Key 错误码说明

|错误码|说明|解决方案|
|-|-|-|
|GE1003|未配置 API Key|前往 https://www.feedax.cn 申请|
|GE1004|API Key 已失效|检查 API Key 有效性，或重新申请|
|GE1005|API Key 已过期|前往 https://www.feedax.cn 重新申请|
|GE1006|API Key 无效|前往 https://www.feedax.cn 重新申请|
|GE1007|账户余额不足|前往 https://www.feedax.cn 充值|

### 服务错误处理

当 API 服务暂时不可用时，系统会返回友好的错误提示：

|HTTP 状态码|错误提示|
|-|-|
|400|请求参数错误，请检查输入|
|401/403|API Key 可能无效或已过期|
|429|请求过于频繁，请稍后再试|
|500|服务器内部错误|
|502|服务暂时不可用，请稍后再试|
|503|服务维护中，请稍后再试|
|504|网关超时，请稍后再试|
|连接超时|请求超时，请稍后再试|
|连接错误|无法连接到服务器，请检查网络或稍后再试|

---

## 一、接口信息

* **接口地址**: `221.6.15.90:18011`
* **接口 URI**: `/data-service/v1/news/bond/external/query`
* **请求方式**: `POST`
* **Content-Type**: `application/json; charset=UTF-8`

---

## 二、参数说明

### 2.1 必传参数

|参数名|类型|说明|
|-|-|-|
|`apiKey`|String|平台分配的密钥，身份校验必传|
|`keyWordQuery`|Object|关键词查询对象|

**keyWordQuery 结构**:

```json
{
    "keyword": "搜索关键词",
    "queryFields": ["1", "2"]
}
```

* `queryFields`: `["1", "2"]` - 1=正文，2=标题

### 2.2 分页与排序

|参数名|类型|默认值|说明|
|-|-|-|-|
|`pageNum`|Integer|0|页码（从 0 开始）|
|`pageSize`|Integer|20|每页数量，1 ≤ size ≤ 100|
|`sortBy`|String|`publish_date`|**默认按发布时间排序**。仅当用户明确要求按热度排序时才修改|
|`sortType`|String|`DESC`|排序方式：ASC/DESC|

**sortBy 可选值**:

* `publish_date` - **默认**。按发布时间排序，获取最新内容
* `heat_scores` - 按热度排序

**排序规则**：

* **默认行为**：按 `publish_date`（发布时间）排序，获取最新发布的舆情
* **用户明确要求时**：当用户说"按热度排序"、"最热门的"等，才使用 `heat_scores`

### 2.3 内容筛选

|参数名|类型|默认值|说明|
|-|-|-|-|
|`bondTypes`|Array|`[]`|债券类型列表|
|`sentiments`|Array|`[]`|情感倾向列表：正面/负面/中性，空数组表示全部|
|`sseNewsTags`|Array|`[]`|债券标签列表，空数组表示全部|
|`csrcIndustries`|Array|`[]`|证监会行业列表|
|`industrySwResults`|Array|`[]`|申万行业列表|
|`mediaTypes`|Array|`[]`|信源类型列表，空数组表示全部|
|`newsImportanceLevels`|Array|`[]`|重要程度列表，空数组表示全部|
|`themeRresults`|Array|`[]`|主题列表，空数组表示全部|

### 2.4 时间筛选

|参数名|类型|默认值|说明|
|-|-|-|-|
|`startTime`|Long|自动计算|查询开始时间（13 位毫秒时间戳）|
|`endTime`|Long|当前时间|查询结束时间（13 位毫秒时间戳）|

### 2.5 互动数据筛选

|参数名|类型|说明|
|-|-|-|
|`heatScores`|Integer|热度得分|
|`viewNum`|Integer|浏览数|
|`forwardedNum`|Integer|转发数|

---

## 三、债券类型分类 (bondTypes)

### 主要债券类型

| 债券类型 | 说明 |
|---------|------|
| **国债** | 中央政府发行的债券 |
| **地方政府债** | 地方政府发行的债券 |
| **政策性金融债** | 政策性银行发行的金融债券 |
| **企业债** | 企业发行的债券 |
| **公司债** | 上市公司发行的债券 |
| **中期票据** | 银行间市场发行的中期债务工具 |
| **短期融资券** | 短期债务融资工具 |
| **ABS** | 资产支持证券 |
| **可转债** | 可转换公司债券 |
| **REIT** | 不动产投资信托基金 |
| **城投债** | 城投公司发行的债券 |

---

## 四、情感倾向分类 (sentiments)

|情感|值|说明|
|-|-|-|
|正面|`正面`|积极、利好的债券新闻|
|负面|`负面`|消极、风险警示的债券新闻|
|中性|`中性`|客观陈述的债券新闻|

---

## 五、债券标签 (sseNewsTags)

### 常见债券标签

* **风险类**: 违约风险、信用评级下调、负面舆情
* **评级类**: 信用评级、评级调整、评级展望
* **发行类**: 债券发行、申购、配售
* **交易类**: 债券交易、收益率、利差
* **政策类**: 监管政策、货币政策、财政政策
* **行业类**: 城投、房地产、金融、产业债

---

## 六、输出 JSON 格式

### 6.1 请求示例

```json
{
    "apiKey": "YOUR_API_KEY",
    "keyWordQuery": {
        "keyword": "城投债",
        "queryFields": ["1", "2"]
    },
    "bondTypes": ["城投债"],
    "sentiments": [],
    "sseNewsTags": [],
    "csrcIndustries": [],
    "industrySwResults": [],
    "mediaTypes": [],
    "newsImportanceLevels": [],
    "themeRresults": [],
    "pageNum": 0,
    "pageSize": 20,
    "sortBy": "publish_date",
    "sortType": "DESC",
    "startTime": 1774211938071,
    "endTime": 1774838338071
}
```

### 6.2 响应示例

```json
{
    "code": 200,
    "message": "success",
    "total": 156,
    "data": [
        {
            "title": "城投债信用利差走阔，关注区域分化风险",
            "content": "...",
            "summary": "近期城投债信用利差有所走阔，不同区域间分化加剧...",
            "source": "新浪财经",
            "url": "https://...",
            "publishDate": 1774838338071,
            "sentiment": "负面",
            "newsImportanceLevel": "高",
            "heatScores": 85,
            "viewNum": 12500,
            "forwardedNum": 320,
            "sseBondResults": [
                {
                    "bondName": "20 万科 01",
                    "bondType": "公司债",
                    "bondIssuer": "万科企业股份有限公司",
                    "companySentimentScore": -0.3,
                    "relevance": 0.85,
                    "importantArea": "产业债"
                }
            ]
        }
    ]
}
```

### 6.3 必须展示字段

**每条资讯必须包含以下 10 个核心字段**：

| 序号 | 字段 | API 字段名 | 说明 |
|------|------|-----------|------|
| 1 | **新闻标题** | `title` | 资讯标题 |
| 2 | **新闻摘要** | `summary` | 资讯内容摘要 |
| 3 | **新闻内容** | `content` | 资讯完整正文 |
| 4 | **新闻来源** | `source` | 发布媒体/来源 |
| 5 | **发布时间** | `publishDate` | 13 位毫秒时间戳 |
| 6 | **债券名称** | `sseBondResults[].bondName` | 相关债券名称 |
| 7 | **债券类型** | `sseBondResults[].bondType` | 债券类型 |
| 8 | **发行人** | `sseBondResults[].bondIssuer` | 发行人名称 |
| 9 | **重要程度** | `newsImportanceLevel` | 高/中/低 |
| 10 | **热度数据** | `heatScores`/`viewNum`/`forwardedNum` | 热度得分、浏览数、转发数 |

---

## 七、解析规则

### 7.1 关键词解析

从用户输入中提取核心检索关键词。

#### 关键词提取规则

1. **提取核心词**：从用户输入中提取 1-3 个核心关键词（债券名称/类型/发行人）
2. **同义词扩充**：为债券类型添加同义词
3. **情感词处理**：情感词（负面、正面）不放入关键词，通过 `sentiments` 参数控制

#### 关键词解析示例

|用户输入|关键词|
|-|-|
|城投债违约|`城投债 违约`|
|20 万科 01|`20 万科 01`|
|公司债负面|`公司债`|
|债券评级下调|`债券 评级`|

### 7.2 债券类型映射

|用户表述|bondTypes|
|-|-|
|城投债/城投|`["城投债"]`|
|公司债/公司信用债|`["公司债"]`|
|企业债|`["企业债"]`|
|金融债|`["政策性金融债"]`|
|国债/国库券|`["国债"]`|
|地方债|`["地方政府债"]`|
|中票|`["中期票据"]`|
|短融|`["短期融资券"]`|
|全部/不指定|`[]`|

### 7.3 情感倾向映射

|用户表述|sentiments|
|-|-|
|负面/负面信息/风险/担忧/违约|`["负面"]`|
|正面/正面信息/利好/好消息|`["正面"]`|
|中性|`["中性"]`|
|全部情感/不指定|`[]`|

### 7.4 时间范围计算

|用户表述|计算方式|
|-|-|
|6 小时|当前时间 - 6 小时|
|24 小时/一天|当前时间 - 24 小时|
|3 天|当前时间 - 3 天|
|7 天/一周|当前时间 - 7 天|
|30 天/一个月|当前时间 - 30 天|

### 7.5 排序方式映射

**默认规则**：除非用户明确要求，否则一律使用 `publish_date`（发布时间）排序

|用户表述|sortBy|说明|
|-|-|-|
|**无明确要求**|`publish_date`|**默认**，获取最新发布的内容|
|按热度/热门/最火的|`heat_scores`|按热度排序|
|最新/最近/新发布的|`publish_date`|按发布时间排序（默认）|

**关键规则**：

1. **默认行为**：用户只说"搜索 XX 新闻"，没有提到排序方式 → 使用 `publish_date`
2. **明确要求时**：用户说"搜索最热门的 XX"、"按热度排序" → 使用 `heat_scores`
3. **时间优先**：用户关注时效性 → 使用 `publish_date`
4. **热度优先**：用户关注传播度 → 使用 `heat_scores`

### 7.6 重要程度映射

|用户表述|newsImportanceLevels|
|-|-|
|重要/重大|`["高"]`|
|一般/普通|`["中"]`|
|全部|`[]`|

---

## 八、通用规则

1. **必传参数**: `apiKey` 和 `keyWordQuery` 必须传入
2. **逻辑关系**: List 类型参数多值之间为**或关系**，不同参数之间为**且关系**
3. **时间规则**: 时间戳为 13 位毫秒级
4. **数值范围**: Min ≤ Max，否则筛选无效

---

## 九、数据返回方式

### 9.1 返回格式

搜索结果以 **双通道** 方式返回：

#### 通道 1：对话展示（摘要）

* 在对话中展示 **前 5 条** 数据的摘要信息
* **必须展示 10 个核心字段**：
  1. 新闻标题
  2. 新闻摘要
  3. 新闻内容
  4. 新闻来源
  5. 发布时间
  6. 债券名称
  7. 债券类型
  8. 发行人
  9. 重要程度
  10. 热度数据（热度得分、浏览数、转发数）

#### 通道 2：文件输出（完整数据）

* 自动保存 **所有返回数据** 到 CSV 和 MD 文件
* 文件位置：`./bond_information_<时间戳>.csv` 和 `./bond_information_<时间戳>.md`
* CSV 包含完整字段，MD 包含统计分析和数据说明

### 9.2 文件格式示例

**CSV 文件字段**:

```
发布时间，标题，摘要，内容，来源，债券名称，债券类型，发行人，重要程度，热度得分，浏览数，转发数，URL
```

**MD 说明文件内容**:

```markdown
# 债券资讯查询结果说明

**查询关键词**: 城投债
**债券类型**: 城投债
**查询时间范围**: 近 7 天
**数据日期**: 2026-04-02 18:45:00
**结果总数**: 156 条
**接口状态**: code=200, message=success

## 债券类型分布
- 城投债：98 条
- 公司债：35 条
- 企业债：23 条

## 情感分布
- 中性：98 条
- 正面：35 条
- 负面：23 条

## 重要程度分布
- 高：45 条
- 中：67 条
- 低：44 条
...
```

### 9.3 使用建议

* **快速浏览**：查看对话中的前 5 条摘要
* **深度分析**：打开 CSV/MD 文件获取完整数据进行进一步处理
* **数据导出**：CSV 文件可直接导入 Excel 或其他分析工具

---

## 十、搜索执行方式

### 10.1 CLI 命令行工具（推荐）

**文件**: `scripts/query_bond_information.py`

通过命令行调用债券资讯 API，支持所有筛选参数。

#### 基础用法

```bash
# 基础搜索
python3 scripts/query_bond_information.py --keyword "城投债"

# 搜索指定债券类型（最近 7 天）
python3 scripts/query_bond_information.py --keyword "公司债" --days 7

# 搜索指定情感倾向
python3 scripts/query_bond_information.py --keyword "违约" --sentiments 负面 --days 30

# 搜索特定债券
python3 scripts/query_bond_information.py --keyword "20 万科 01" --days 14
```

#### 参数说明

**必填参数**

|参数|简写|说明|
|-|-|-|
|`--keyword`|`-k`|搜索关键词|

**情感筛选**

|参数|简写|说明|
|-|-|-|
|`--sentiments`|`-s`|情感倾向：正面/负面/中性（可多选）|

**分页与排序**

|参数|简写|默认值|说明|
|-|-|-|-|
|`--days`|`-d`|7|查询天数|
|`--page`|`-p`|0|页码（从 0 开始）|
|`--size`|`-n`|20|每页数量|
|`--sort-by`||`publish_date`|排序字段|
|`--sort-type`||`DESC`|排序方式：ASC/DESC|

**输出控制**

|参数|简写|说明|
|-|-|-|
|`--verbose`|`-v`|显示详细内容（摘要）|
|`--output-dir`||输出目录（默认当前目录）|
|`--no-output`||不生成输出文件，仅显示结果|
|`--api-key`||FEEDAX API Key（也可通过环境变量提供）|

#### 完整示例

```bash
# 搜索城投债负面舆情，最近 14 天
python3 scripts/query_bond_information.py \
    --keyword "城投债" \
    --sentiments 负面 \
    --days 14 \
    --size 20 \
    --verbose
```

#### 输出结果

1. **对话显示**：自动在终端显示结果摘要（序号、时间、情感、标题、来源、债券信息、热度）
2. **CSV 文件**：完整数据保存至 `./bond_information_<时间戳>.csv`
3. **MD 文件**：统计分析保存至 `./bond_information_<时间戳>.md`

---

### 10.2 API Key 配置方式

API Key 需要通过以下方式之一提供（优先级从高到低）：

1. **命令行参数**: `--api-key "your-api-key"`
2. **环境变量**: `export FEEDAX_API_KEY="your-api-key"`
3. **配置文件**: 在 `scripts/` 目录创建 `config.json`，内容为 `{"api_key": "your-api-key"}`

---

## 十一、示例对话

**用户**: 搜索最近 7 天城投债的负面新闻，按热度排序

**解析结果**:

```json
{
    "apiKey": "YOUR_API_KEY",
    "keyWordQuery": {
        "keyword": "城投债",
        "queryFields": ["1", "2"]
    },
    "bondTypes": ["城投债"],
    "sentiments": ["负面"],
    "sseNewsTags": [],
    "csrcIndustries": [],
    "industrySwResults": [],
    "mediaTypes": [],
    "newsImportanceLevels": [],
    "themeRresults": [],
    "pageNum": 0,
    "pageSize": 20,
    "sortBy": "heat_scores",
    "sortType": "DESC",
    "startTime": 1774211938071,
    "endTime": 1774838338071
}
```

**执行命令**:

```bash
python3 scripts/query_bond_information.py \
    --keyword "城投债" \
    --sentiments 负面 \
    --days 7 \
    --sort-by heat_scores
```

---

## 十二、执行流程

收到用户搜索请求后，必须按以下步骤顺序执行：

### Step 1: 检查 API Key 配置

```bash
cat .env | grep FEEDAX_API_KEY
```

* 如果返回空或文件不存在，提示用户："未配置 API Key，请前往 https://www.feedax.cn 申请，完成后请告诉我 API Key 以便我记住"
* 如果存在有效的 API Key，继续下一步

### Step 2: 解析用户输入

从用户自然语言中提取以下参数：

|提取项|对应 CLI 参数|示例|
|-|-|-|
|关键词|`--keyword`|"城投债违约" → `--keyword "城投债"`|
|情感倾向|`--sentiments`|"负面" → `--sentiments 负面`|
|时间范围|`--days`|"最近 3 天" → `--days 3`|
|排序方式|`--sort-by`|"按热度" → `--sort-by heat_scores`|

### Step 3: 构建并执行 CLI 命令

根据解析结果构建命令并执行：

```bash
python3 scripts/query_bond_information.py --keyword "关键词" --sentiments 负面 --days 7
```

### Step 4: 返回结果

* 在对话中显示结果摘要（10 个必须展示字段）
* 完整数据自动保存至 CSV 和 MD 文件

### 执行示例

**用户输入**: "搜索最近 7 天城投债的负面新闻"

**执行命令**:

```bash
python3 scripts/query_bond_information.py --keyword "城投债" --sentiments 负面 --days 7
```

---

## 十三、注意事项

1. **时间参数**: 使用 Unix 时间戳（毫秒），脚本会自动计算
2. **页码**: 从 0 开始计数
3. **情感倾向**: 正面、负面、中性，不传表示全部
4. **债券类型**: 支持 11 种债券类型筛选
5. **API Key**: 必须提供，支持三种配置方式
6. **输出文件**: 默认生成 CSV 和 MD 文件，可使用 `--no-output` 禁用

---

## 十四、参考文件

* `scripts/query_bond_information.py` - 主查询脚本
* `scripts/config.json` - API Key 配置文件（可选）
* `.env` - 环境变量配置文件

---

*数据来自 FEEDAX 债券资讯监测平台，涵盖新闻、社交媒体、论坛、金融平台等多种信源。*
