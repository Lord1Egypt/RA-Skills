---
id: 1688商品诊断
name: 1688-product-analysis
description: 1688 商品全方位分析诊断工具，整合多个数据源对指定商品进行深度分析。当用户需要分析某个指定商品表现、诊断流量问题、优化商品策略时使用。适用于指定商品的：商品数据分析、销售表现诊断、搜索排名问题分析、广告效果评估、市场竞争分析、商品优化建议。触发关键词包括"分析这个商品"、"商品诊断"、"商品表现分析"、"为什么商品没流量"、"商品优化建议"、"商品数据分析"等。
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      bins: ["python3"]
    primaryEnv: "ALI_1688_AK"
  interactions:
    - name: select_abnormal_offer
      type: table
      selectionType: product
      description: "从异常商品列表中选择要诊断的商品。在执行 get_abnormal_offers 获取异常商品后展示，用户可多选需要诊断的商品。"
      required_data:
        title: "表格标题"
        columns: "列定义数组"
        rows: "异常商品数据行数组，每项包含 id, title, reason, payAmount, changeRate"
    - name: input_offer_id
      type: input
      selectionType: product
      description: "当异常商品列表为空时，引导用户手动输入商品 ID 进行诊断。"
      required_data:
        questions: "问题列表，包含一个输入框让用户填写商品 ID"
    - name: select_action
      type: card
      selectionType: requirement
      description: "诊断报告输出后，根据商品诊断结果生成可执行的行动选项（商品主图优化、商品标题优化），让用户选择要立即执行的优化操作"
      required_data:
        questions: "问题列表数组，每项包含 question（问题文本）和 options（选项字符串数组，1-2 项，对应主图/标题优化）"
---

# 1688 商品诊断

## ⚠️ 强制约束

1. **禁止编造数据**：所有数据必须来自 CLI 真实返回结果
2. **先执行 CLI 再分析**：必须先通过 `python3 cli.py` 调用获取数据，不得跳过
3. **如实标注失败或空数据**：返回 `success=false` 或空数据时标注"数据暂不可用"，不必反复重试

## 数据查询命令

统一入口：`python3 {baseDir}/cli.py <command> [options]`

`__userId__` 由 `cli.py` 通过解析 `ALI_1688_AK` 自动注入，命令本身无需感知卖家身份。

| 命令                    | 用法                                                                                                          | 说明                                                                                          |
| ----------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `get_abnormal_offers`   | `python3 {baseDir}/cli.py get_abnormal_offers [--date_type <日期类型>] [--device <设备>]`                       | 查询商家需重点关注的异常商品列表（支付下跌、访客下跌等，多个异常榜单取交集）                    |
| `get_offer_data`        | `python3 {baseDir}/cli.py get_offer_data --offer_id <商品ID> [--modules <模块列表>]`                           | 获取商品综合数据（基础资料、表现、货盘、搜推问题、购买因素、异常检测、广告分析、热搜词、热品）  |

### get_abnormal_offers 参数说明

- `--date_type`：日期类型（可选，默认 `RECENT_7`）
  - 可选值：`RECENT_7`（近 7 天）、`RECENT_30`（近 30 天）
- `--device`：设备筛选（可选，默认 `ALL`）
  - 可选值：`ALL`（全部）、`PC`、`APP`

返回值示例：

```json
{
  "success": true,
  "data": {
    "count": 20,
    "items": [
      {"itemId": "668758083302", "offerTitle": "...", "reason": "支付下跌", "valueMap": {...}},
      {"itemId": "779218424674", "offerTitle": "...", "reason": "访客下跌", "valueMap": {...}}
    ]
  }
}
```

### get_offer_data 参数说明

- `--offer_id`：商品 ID，字符串（**必填**）
- `--modules`：要获取的数据模块，逗号分隔（可选，默认 `all`）
  - 可选值：`profile`（基础资料）、`performance`（表现）、`huopan`（货盘）、`search_issues`（搜推问题）、`purchase_factors`（购买因素）、`sycm_anomaly`（异常检测）、`ad_analysis`（广告分析）、`hotwords`（热搜词）、`hot_items`（热品）、`all`

输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

示例：

```bash
# 获取全量数据
python3 {baseDir}/cli.py get_offer_data --offer_id 1048050628164

# 仅获取表现 + 广告 + 搜推问题
python3 {baseDir}/cli.py get_offer_data --offer_id 1048050628164 --modules performance,ad_analysis,search_issues
```

## 参考文档

通过 `read_file` 读取：

| 文档     | 路径                                       |
| -------- | ------------------------------------------ |
| 分析维度 | `references/analysis-dimensions.md`        |
| 报告模板 | `references/report-template-simple.md`     |
| 交互规范 | `references/interaction-specs.md`          |

## 安全声明

| 风险级别 | 命令                   | Agent 行为             |
| -------- | ---------------------- | ---------------------- |
| **只读** | `get_abnormal_offers`  | 可直接执行，无需确认   |
| **只读** | `get_offer_data`       | 可直接执行，无需确认   |

## 诊断执行步骤

### Step 1: 查询异常商品列表 + 交互选择（前置步骤）

执行异常商品查询，获取商家需要重点关注的商品：

```bash
python3 {baseDir}/cli.py get_abnormal_offers
```

根据返回结果分两种情况处理：

**情况 A：异常商品列表不为空**

调用 `show_interaction` 以 Table 组件展示异常商品供用户选择：

- 设置 `name='select_abnormal_offer'`
- 将 `get_abnormal_offers` 返回的 `data.items` 数组按照 `references/interaction-specs.md` 中定义的字段映射规则，转换后赋值给 `rows` 槽位
- **具体的列定义、字段映射和数据结构请查阅 `references/interaction-specs.md` 中 `select_abnormal_offer` 章节**

用户选择商品后，从交互结果中提取 `id`（即 `itemId`）作为后续诊断的 `offer_id`。

**情况 B：异常商品列表为空**

调用 `show_interaction` 以 Input 组件引导用户手动输入商品 ID：

- 设置 `name='input_offer_id'`
- **具体的数据结构请查阅 `references/interaction-specs.md` 中 `input_offer_id` 章节**

用户输入商品 ID 后，将其作为后续诊断的 `offer_id`。

> 如果用户已明确提供了商品 ID，可跳过此步骤直接进入 Step 2。

### Step 2: 读取分析标准 + 收集商品数据（并发执行）

用户选择商品（或输入 offer_id）后，同时执行：

- `read_file("references/analysis-dimensions.md")`
- `bash("python3 {baseDir}/cli.py get_offer_data --offer_id <商品ID>")`

### Step 3: 输出精简报告

按照 `references/report-template-simple.md` 模板输出诊断报告。

**输出格式**：

```
1. [商品名称] (ID: [商品ID]) —— 【货盘定位】
   ● 选择原因：[为什么优化，用数据说话]
   ● 优化：
      - [优化项1]
      - [优化项2]
      - [优化项3]
```

**要求**：

1. **货盘定位** - 标注【引流款】【利润款】【爆款】【定制款】【新品】
2. **选择原因** - 1-2 句话说明核心问题，必须引用具体数据
3. **优化项** - 每个商品 1-4 条，要具体可执行（不要泛泛而谈）
4. **优先级** - 违规问题 > 流量问题 > 转化问题 > 优化建议

### Step 4: 行动选择（必须执行，禁止省略）

诊断报告输出完成后，Agent **必须立即**调用 `show_interaction` 触发 `select_action` 交互：

1. **先读取** `references/interaction-specs.md` 中 `select_action` 章节，获取完整的数据槽位、构造规则、关键词映射表、完整 JSON 示例
2. **再触发** metadata.interactions 中声明的 `select_action`，严格按 specs 中的字段映射构造 `questions` 数据
3. **数据来源**：`options` 数组的内容必须从本次诊断报告"优化项"原文提取，禁止硬编码或编造
4. **用户选中后**：根据 specs 中"用户选择后的处理"表，直接调用对应下游技能（`1688-item-image-optimizer` / `1688-item-title-optimizer`），并把当前诊断的 `offer_id` 与对应优化项原文作为上下文传入，无需用户再次输入

> ⚠️ 即使报告输出完整、用户没有进一步发言，也**必须**触发此交互，否则视为流程未完成。

## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词                              | Agent 额外动作                                                               |
| -------------------------------------------- | ---------------------------------------------------------------------------- |
| "AK 未配置"                                  | 提示用户在 OpenClaw 配置 `ALI_1688_AK`，或检查 `~/.openclaw/openclaw.json`  |
| "offer_id 不能为空" / "modules 取值非法"     | 提示用户使用合法的参数值                                                     |
| "dateType 取值非法" / "device 取值非法"      | 提示用户使用合法的参数值                                                     |
| "异常商品数据为空" / "商品数据为空"          | 提示用户确认账号是否已沉淀有效数据                                           |
| "网络异常，已重试" / "限流" / "429"          | 建议用户等待 1-2 分钟后重试                                                  |
| 其他                                         | 仅输出 markdown 即可                                                         |

## 环境变量（.env）

项目根目录的 `.env` 文件存储 skill 基础信息，供埋点上报等模块读取。发布到不同环境时可直接替换该文件中的变量值。

| 变量                  | 默认值                  | 说明                                                                |
| --------------------- | ----------------------- | ------------------------------------------------------------------- |
| `SKILL_NAME`          | `1688-product-analysis` | skill 名称                                                          |
| `SKILL_VERSION`       | `1.0.0`                 | skill 版本号                                                        |
| `SKILL_CHANNEL`       | `clawhub`               | 发布渠道                                                            |
| `ALI_1688_AK`         | 由平台 OpenClaw 注入    | 1688 开放平台 AK，CLI 自动解析卖家身份并注入 `__userId__`           |
| `OPENCLAW_CONFIG_DIR` | `~/.openclaw`           | OpenClaw 配置文件目录（AK 兜底读取来源）                            |

> 已存在的系统环境变量优先级高于 `.env`，CI/CD 注入的变量不会被覆盖。

## 注意事项

- 商品 ID 为字符串格式，通过 `--offer_id` 参数传入
- 报告中每一项数据都必须能追溯到 CLI 的真实输出
- 建议要具体可执行，结合 1688 平台特点和商家实际需求
