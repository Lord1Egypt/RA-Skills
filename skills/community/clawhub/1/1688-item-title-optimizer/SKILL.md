---
name: 1688-item-title-optimizer
description: |
  1688 商品标题智能优化助手 —— 自动并发执行两种优化算法生成结果。
  工具能力：添加热词优化（快速、基于规则）和 LLM 深度重写（高质量、自然流畅），支持用户偏好参数。
  触发词：优化标题、标题优化、改标题、重写标题、商品标题、标题改写。
metadata:
  openclaw:
    emoji: "✏️"
    requires:
      bins:
        - python
  interactions:
    - name: open_tab_select_product
      type: open_tab
      selectionType: shop_backend
      description: "当用户未提供商品ID时，直接输出该JSON唤起商品选择页面，流程结束，禁止反问用户"
      required_data:
        url: "商品选择页面URL"
        pageTitle: "选择商品"
        pageDescription: "选择商品优化标题"
        icon: "图标URL"
    - name: confirm_apply_title
      type: card
      selectionType: requirement
      description: "用户选定标题后，确认是否应用到商品"
      required_data:
        questions: "展示选定标题并询问是否应用"
    - name: select_items_to_optimize
      type: table
      selectionType: product
      description: "当用户传入≥3个商品ID时，在左侧弹出表格让用户筛选要优化的商品"
      required_data:
        title: "表格标题"
        columns: "列定义数组：商品ID、当前标题"
        rows: "商品列表，每项包含 itemId、title"
    - name: title_comparison_card
      type: table
      selectionType: title_plan
      description: "两种优化方案生成后，在左侧弹出表格供用户选择新标题。3列（方案+属性+内容），每个成功方案4个维度各占一行（两个都成功=8行，一个成功一个失败=仅展示成功方案的4行，两个都失败=不弹表格直接提示重试）。利用端侧 show_interaction.table v2 协议的 mergedColumns + groupBy + selectionGranularity:group + selectionMode:single 实现方案列相邻同值合并 + 组级互斥单选，用户勾选整组后点击「采用此方案」按钮"
      required_data:
        title: "表格标题：请选择新标题 + 商品名称（商品ID）"
        columns: "固定3列：plan（方案标识，宽80，不传 editable）、field（属性标签，宽140，必须显式声明 editable:false 否则会被端侧误渲染为可编辑，用户实测确认）、value（内容，宽620，不传 editable，由行级 rows[i].editable 控制）。配合行级 editable：仅新标题行 rows[i] 加 editable:true 时该 cell 可编辑，其他 cell 全部只读"
        mergedColumns: "[\"plan\"]。协议硬约束：列必须存在；不能含列级 editable:true 的列。本场景 value 已不开列级 editable，但仍只合并 plan，因为 value 每行内容都不同没有相邻同值"
        groupBy: "\"plan\"。selectionGranularity=group 时必填，按plan相邻同值切分组"
        selectionGranularity: "\"group\"。勾选粒度按组（每组组首行渲染一个checkbox，rowSpan=组大小）"
        selectionMode: "\"single\"。互斥单选：选新组自动取消旧组；点已选项=清空；空选=跳过。与 selectionGranularity 正交"
        actions: "[{key:adopt, label:采用此方案, variant:primary, description:...}]，覆盖默认「确认选择」"
        rows: "4行或8行（rows.length≤10，超过会触发分页关闭合并）。仅填入成功方案的行，失败方案不展示。两个都成功=8行，一个成功一个失败=4行，两个都失败=不弹表格。同方案的4行 plan 必须填相同值且连续排列：方案名称、新标题（仅这行 rows[i].editable:true，可cell内编辑）、生成逻辑及优化说明、预估曝光变化"
        respond_contract: "selectedRows 始终回传展开后的N行（与 multiple+row 同构），Agent 按 plan 分组、按 field=新标题 取最终value（含编辑），空选视为跳过。无论端侧是否识别行级 editable，Agent 必须软兜底：只采用「新标题」行的编辑值，其他 3 行编辑显式忽略"
---

# 1688-item-title-optimizer — 商品标题智能优化

## 技能概述

1688 商品标题智能优化助手。自动并发执行两种优化算法生成结果：1) 添加热词优化（快速、基于规则）2) LLM 深度重写（高质量、自然流畅）。只需提供商品 ID，即可同时获得两种优化方案供对比选择。支持用户偏好参数（如"加入'防潮'单词"）。

## 使用场景

- 商品标题修改、改写、优化
- 新品发布，需要高质量标题
- 批量优化商品标题
- 用户有特定优化偏好（如指定关键词、风格）

## CLI 命令

### configure — 配置 AK

```bash
# 查看 AK 状态
python3 {baseDir}/cli.py configure
# 设置 AK
python3 {baseDir}/cli.py configure YOUR_AK
```

配置网关鉴权所需的 AK。所有操作命令都依赖 AK，首次使用前需先配置。

### optimize_title — 添加热词优化（方式A）

```bash
python3 {baseDir}/cli.py optimize_title --item_id <商品ID>
```

基于规则和统计的标题优化，保留原标题结构，快速添加高价值热搜词。

### optimize_title_llm — LLM 深度重写（方式B）

```bash
# 基础调用
python3 {baseDir}/cli.py optimize_title_llm --item_id <商品ID>

# 带用户偏好
python3 {baseDir}/cli.py optimize_title_llm --item_id <商品ID> --preference "加入防潮单词"
```

基于大语言模型的智能标题重写，全面改写标题，支持用户偏好定制。

### get_keyword_info — 获取关键词信息

```bash
# 基础调用
python3 {baseDir}/cli.py get_keyword_info --item_id <商品ID>

# 添加自定义关键词
python3 {baseDir}/cli.py get_keyword_info --item_id <商品ID> --custom_keywords "保温杯;不锈钢;便携"
```

获取标题优化所需的全部关键词数据（热搜词、曝光词、类目信息）。

### get_tokenizers — 获取分词器列表

```bash
python3 {baseDir}/cli.py get_tokenizers
```

获取所有可用的分词器列表及说明。

## ⚠️ 重要：技能skill 使用规范

### 规则2：获取到商品ID后，自动并发执行两种优化

当用户请求标题优化时，**必须按以下步骤执行，关键节点需等待用户确认后再继续**：

1. **⏸️ 参数要求（硬性阻断点）**：如果用户未提供商品 ID，**严禁**弹 card 询问，必须按规则1输出JSON

2. **⏸️ 多商品澄清（≥3 个商品时必须触发）**：
   - 如果用户一次传入 **3 个及以上商品 ID**，**必须先触发** `select_items_to_optimize` 交互，让用户筛选需要优化的商品
   - 展示所有商品 ID 及其当前标题（如能获取），让用户选择要优化的商品
   - **必须等待用户选择后再继续**，禁止自动对所有商品执行优化
   - 如果用户传入 1-2 个商品，可直接跳过此步骤进入下一步

3. **自动执行**：收到用户的优化请求后（或用户在澄清点选定商品后），**必须自动并发调用**两种优化命令

4. **并发调用**：在同一个消息中同时发起两个工具调用：
   - `optimize_title`（方式A：添加热词优化）
   - `optimize_title_llm`（方式B：AI深度重写）

5. **提取偏好**：如果用户在请求中提到特殊要求（如"加入'防潮'单词"），提取偏好并传入 `optimize_title_llm` 的 `--preference` 参数

6. **展示结果：触发 `title_comparison_card`**（`type: table`，在左侧弹出表格）
   - 3 列（方案 + 属性 + 内容），每个方案 4 行（方案名称、新标题、生成逻辑及优化说明、预估曝光变化）
   - 利用 `mergedColumns: ["plan"]` + `selectionGranularity: "group"` + `groupBy: "plan"` + `selectionMode: "single"` 实现方案列合并单元格 + 组级单选勾选
   - 通过 `actions` 配置一个 `key: "adopt"` / `label: "采用此方案"` / `variant: "primary"` 的按钮替代默认"确认选择"
   - **rows 的 `plan` 字段：同组所有 4 行都填相同方案名**（如全部填"方案A"或全部填"方案B"），端侧依靠相同值进行合并和分组

7. **⏸️ 应用确认**
   - 向用户展示选定的新标题，与原标题对比
   - 触发 `confirm_apply_title` 交互，让用户选择：
     - ✅ 确认，应用到商品标题
     - ✏️ 我想手动微调后再应用（用户可输入修改后的标题）
     - 💾 仅记录，暂不应用
   - **必须等待用户确认后再继续**，禁止自动跳过

8. **应用到商品**：
   - 如果用户确认应用，且存在技能 `1688-item-one-click`，则调用技能更新商品标题
   - 如果用户手动微调了标题，使用微调后的版本应用

**具体的交互组件数据结构请查阅 [`references/interaction-specs.md`](./references/interaction-specs.md) 中对应交互的章节。**

### 规则3：结果展示规范（左侧 Table 表格）

展示时必须使用 `title_comparison_card`（**`type: table`**）交互组件，在左侧弹出表格，3 列（方案 + 属性 + 内容），每个方案 4 行，方案列合并为大单元格，组级互斥单选勾选。

> ⚠️ **端侧版本依赖（v2 协议）**：本交互依赖 `mergedColumns` / `selectionGranularity` / `selectionMode` / `groupBy` 4 个 v2 字段，**仅在已升级到 v2 的客户端**才会生效。当前 1688 工作台 / 找工厂客户端尚未升级，会**忽略**这 4 个字段，退化为默认的 `row + multiple`（每行一个 checkbox、可任意多勾、无方案列合并）。
>
> **Agent 必须知道**：
> - **payload 不要为兼容降级而修改**——协议字段写法是正确的，等客户端升级即可自动生效
> - **看到「每行一个 checkbox」不是 payload 错了**，是端侧降级渲染
> - 处理 `selectedRows` 时**必须用下方"用户回传后处理"统一兼容算法**，不能假设回传一定是同一方案的 4 行
> - 完整端侧能力对比与降级表见 `references/interaction-specs.md` 中"端侧版本依赖"小节

**展示规范**（`title_comparison_card`）：

1. **`title`**：格式为"请选择新标题 — 商品名称（商品ID）"
2. **`columns` 固定 3 列**：
   - `plan`（方案标识列，宽 80px，**不传** `editable`）
   - `field`（属性标签列，宽 140px，**必须显式声明** `editable: false`）—— ⚠️ 用户实测：省略 `editable` 字段会让端侧把该列误渲染为可编辑，**显式写 `false`** 才能保证只读
   - `value`（内容列，宽 620px，**列级不传** `editable`，由行级 `rows[i].editable: true` 仅在"新标题"行开启）

   ⚠️ **行级 editable 协议（2026-05 用户实测有效）**：1688 端侧官方曾答复"列级 editable 不支持行级控制"，但**用户实测确认**端侧已支持 `rows[i].editable: true` 行级控制。本场景配合"`field` 列显式 `editable: false` + `value` 列不传 + 仅新标题行 `rows[i].editable: true`"的组合写法，达到"仅新标题行可编辑、其他所有 cell 都只读"的预期效果。
   
   **双层保护（防御性设计）**：即使端侧某天回退、行级 editable 失效，Agent 在读取回传时**仍必须**软兜底：只采用「新标题」行的编辑值，其他 3 行编辑显式忽略（详见下方"用户回传后处理"第 6 步），保证业务正确性不依赖于端侧能力
3. **v2 协议合并/勾选字段（4 个，缺一不可）**：
   - `mergedColumns: ["plan"]`：方案列按**相邻同值**合并为大 rowSpan 单元格
   - `groupBy: "plan"`：按方案字段切分相邻分组（`selectionGranularity:"group"` 时必填）
   - `selectionGranularity: "group"`：勾选**单位**为组（每组组首行渲染一个 checkbox，整组共用）
   - `selectionMode: "single"`：勾选**数量**为单选（方案 A / B 互斥；选新组自动取消旧组；点已选项 = 清空；空选 = 跳过）
4. **协议硬约束**（违反会被主进程 validator 拒绝 / 端侧渲染异常）：
   - `mergedColumns` 中的列**不能是列级 `editable: true`** —— 本场景 `value` 列已改为不开启列级 editable（用行级 `rows[i].editable` 替代），所以约束自动满足；仍只合并 `plan`，因为 `value` 每行内容不同没有相邻同值可合并
   - **`field` 列必须显式 `editable: false`**（不可省略）—— 用户实测：省略时端侧会把该列误渲染为可编辑
   - `rows.length ≤ 10` —— 超过会触发端侧分页并自动关闭合并；本场景最多 8 行（仅成功方案入表），安全
   - 同方案的所有行 `plan` 字段必须**填相同值且连续排列**（不能"方案A、方案B、方案A"这样交错），否则相邻同值合并失效
5. **`actions` 自定义按钮**：配置 `[{ key: "adopt", label: "采用此方案", variant: "primary", description: "..." }]` 替代默认"确认选择"
6. **`rows` 仅填入成功方案的行（4 行或 8 行，严禁填入失败方案的行）**：两个都成功 = 方案 A 4 行 + 方案 B 4 行共 8 行；一个成功一个失败 = 仅成功方案的 4 行（**禁止**为失败方案填占位行）；两个都失败 = 不弹表格。每方案 4 个属性维度，**行级 editable 配置**（仅"新标题"行设 `editable: true`，端侧识别后这 3 行渲染只读）：
   - 方案名称（**不设** `editable`，端侧默认只读；即使端侧不识别行级 editable，Agent 也忽略此行编辑值）
   - **新标题**（**设** `"editable": true`，可 cell 内编辑；**用户编辑会被采用**为最终标题）
   - 生成逻辑及优化说明（**不设** `editable`，端侧默认只读；Agent 完全不读此行编辑值）
   - 预估曝光变化（**不设** `editable`，端侧默认只读；Agent 完全不读此行编辑值）
7. **生成逻辑维度构造**（写入"生成逻辑及优化说明"行的 `value`，按热度 `weight` 标注）：
   - 🔥 热词（tag=`热词`）：词名(热度:weight值)
   - 📈 流量获取（tag=`时间词`/`修饰词`）
   - ✨ 吸引力（tag=`场景词`/`风格词`）
   - 👀 买家关注（tag=`属性词`/`材质词`/`品类词`/`功能词`）
8. **📈 曝光量变化预测（必须）**：基于热词数据给出"+X% ~ +Y%"区间，写入"预估曝光变化"行的 `value`，必须附带"实际效果受类目竞争、商品权重、市场环境等多因素影响，仅供参考"免责说明（具体规则见 `references/interaction-specs.md` 中"曝光量变化预测规则"小节）
9. **部分失败处理（严禁展示失败方案）**：若任一方案 CLI 返回 `success: false` 或异常，**直接跳过该方案**，rows 中**仅填入成功方案的 4 行**，**禁止**为失败方案填入任何占位行/兜底行。具体规则：
   - **一个成功一个失败** → `title_comparison_card` 只展示成功方案的 4 行（`rows.length = 4`）；由于只有 1 个方案可选，用户直接勾选该方案即可；在对话中简要告知用户另一方案本次未生成成功
   - **两个都失败** → **不弹** `title_comparison_card` 表格；直接在对话中告知用户"两种优化方案均未生成成功，建议稍后重试"，并提示可重新触发优化
   - **两个都成功** → 正常展示 8 行（不变）

**用户回传后处理**（统一兼容 v2 客户端 与 未升级客户端，**无需事先判断端侧版本**，按此顺序执行）：

> **前置要求**：触发本交互之前，Agent 必须确保 `optimize_title`（方案A）和 `optimize_title_llm`（方案B）的 CLI 完整返回 JSON **仍可在当前对话上下文中访问**（用于降级场景下重新弹窗时重构 payload，**禁止**为此重新调用 CLI）。

1. **空选判定**：`selectedRows.length === 0` → 视为跳过，**禁止**进入 `confirm_apply_title`，应回退询问"是否重新生成 / 结束优化"

2. **按 `plan` 字段分组聚合**：`groups = group_by(selectedRows, row => row.plan)`

3. **跨方案混勾的兜底**（分组数 ≥ 2，仅未升级客户端可能出现）：**严禁**用"取行数最多的方案"等启发式猜测算法。必须：
   1. 给用户对话提示："检测到您勾选了多个方案的行（方案 A：N₁ 行 / 方案 B：N₂ 行），由于本次只能采用一个方案，请在重新弹出的表格中**仅勾选您想采用的那一个方案**，再点「采用此方案」"
   2. **重新触发 `title_comparison_card`**，用前置小节提到的成功方案的原始 CLI 返回值**重新构造 payload**（仅填入成功方案的行；**禁止**重新调用 `optimize_title` / `optimize_title_llm`）
   3. 等待新一轮回传，从第 1 步重新走

4. **缺字段的兜底**（分组数 = 1 但唯一方案的行集合中缺少 `"方案名称"` 或 `"新标题"`，仅未升级客户端可能出现）：
   1. 给用户对话提示："您勾选的行不完整（缺少 `<缺失的 field 列表>`），请在重新弹出的表格中**勾选包含「方案名称」和「新标题」的完整行集合**"
   2. **重新触发 `title_comparison_card`**（同第 3 步：用原始 CLI 返回值重构 payload，**禁止**重调 CLI）
   3. 等待新一轮回传，从第 1 步重新走

5. **（已移除）**：由于失败方案不再进入表格，无需在回传后识别失败方案。直接进入第 6 步

6. **读取最终新标题（仅采用「新标题」行的编辑值）**：在唯一选中方案的行集合里找 `field === "新标题"` 的行（第 4 步已保证此行存在），取其 `value`（**可能已被用户在 cell 内编辑**，以此为准，**禁止**回退读 CLI 原始 `new_title`，**禁止**用其他 field 的 value 当标题）。
   - ⚠️ **关于其他 3 行的用户编辑**：协议层已通过**不在这 3 行设置** `editable: true` 让端侧渲染为只读。但万一端侧暂不识别 `rows[i].editable` 退化为"全部 cell 可编辑"，Agent 仍须**显式忽略**这些行的编辑值（双层保护）：
     - 方案名称行的 value 仅用于"识别选中方案"，**不参与最终标题构造**
     - 生成逻辑 / 预估曝光变化 行的 value **完全不读**，仅作 UI 展示
     - **严禁**因用户改了其他行就把它当成新标题写入 `confirm_apply_title`

7. **进入应用确认**：携带"方案标识（来自分组的唯一 key）+ 最终新标题（仅来自「新标题」行的编辑值）+ 商品 ID + 商品原标题"触发 `confirm_apply_title`

> **设计原则**：上述算法只依赖 `selectedRows` 的扁平结构 + `plan`/`field` 字段语义，不依赖端侧"组"/"单选"实现细节。在 v2 客户端上第 3、4 步的兜底永不触发（端侧已保证完整性），算法退化为"取 `groups` 唯一 key + 找新标题行"的极简路径；在未升级客户端上兜底按需启用，依靠 context 中已有的 CLI 原始返回值重构 payload 重新弹窗，**不再调用任何 CLI**。**待 1688 客户端升级到 v2 后无需任何回滚**。完整算法说明见 `references/interaction-specs.md` 中"Agent 处理逻辑"小节。

### 规则4：用户偏好提取

如果用户在优化请求中提到特殊要求，需要提取并传入 `--preference` 参数：

**识别偏好的关键词**：

- "加入xxx"、"添加xxx"、"包含xxx" → 提取关键词
- "突出xxx"、"强调xxx"、"体现xxx" → 提取特点要求
- "要xxx风格"、"面向xxx" → 提取风格要求

**示例**：

```
用户："优化商品831034165952的标题，加入'防潮'这个词"
  ↓
提取：preference = "加入'防潮'单词"
  ↓
调用：cli.py optimize_title_llm --item_id 831034165952 --preference "加入'防潮'单词"
```

## 安全声明

| 风险级别 | 命令 | Agent 行为 |
|---------|------|----------|
| 只读 | configure | 可直接执行，无需确认 |
| 只读 | optimize_title | 可直接执行，无需确认 |
| 只读 | optimize_title_llm | 可直接执行，无需确认 |
| 只读 | get_keyword_info | 可直接执行，无需确认 |
| 只读 | get_tokenizers | 可直接执行，无需确认 |

> 所有命令均为只读操作，不会修改商品标题。优化结果仅供参考，需用户确认后手动应用。

## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词 | Agent 额外动作 |
|----------------|--------------|
| "AK 未配置" 或 "签名无效" 或 "401" | 提示用户当前发送能力所需鉴权未就绪，请补充有效 AK 或检查鉴权配置后重试 |
| "限流" 或 "429" | 建议用户等待 1-2 分钟后重试 |
| 其他 | 仅输出 markdown 即可 |

## 环境变量（.env）

项目根目录的 `.env` 文件存储 skill 基础信息，供埋点上报等模块读取。发布到不同环境时可直接替换该文件中的变量值。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_NAME` | `1688-item-title-optimizer` | skill 名称 |
| `SKILL_VERSION` | `1.0.0` | skill 版本号 |
| `SKILL_CHANNEL` | `clawhub` | 发布渠道 |

> 已存在的系统环境变量优先级高于 `.env`，CI/CD 注入的变量不会被覆盖。

## 埋点上报

每次 CLI 命令执行时，自动向 skill 网关上报一次调用记录，用于统计 skill 调用次数。

- **实现位置**：`scripts/_tracker.py` → `report_skill_usage()`，在 `cli.py` 的 `main()` 中每次命令执行后自动调用
- **上报接口**：`POST /api/reportSkillsUsage/1.0.0`
- **上报参数**：

  | 参数 | 值来源 | 说明 |
  |------|--------|------|
  | `apiName` | 固定 `null` | 固定传 null |
  | `skillsName` | `.env` `SKILL_NAME` | skill 名称 |
  | `version` | `.env` `SKILL_VERSION` | skill 版本号 |
  | `scene` | 固定 `CLI` | 固定值 |
  | `channel` | `.env` `SKILL_CHANNEL` | 发布渠道 |

- **失败处理**：上报失败静默忽略，不影响主流程

## 输出格式

采用标准 JSON 输出：

```json
{
  "success": true,
  "markdown": "✅ 标题优化完成",
  "data": {
    "item_id": 831034165952,
    "old_title": "304不锈钢水杯",
    "new_title": "304不锈钢保温杯便携大容量",
    "optimize_reason": "添加热词:保温杯,便携,大容量",
    "new_title_words": [...],
    "other_words": [...]
  }
}
```

## 两种优化方式对比

| 特性 | optimize_title（方式A） | optimize_title_llm（方式B） |
|------|----------------------|--------------------------|
| 优化方式 | 规则 + 统计 | LLM 深度重写 |
| 优化质量 | ★★★★☆ | ★★★★★ |
| 优化速度 | < 1 秒 | 2-5 秒 |
| 标题自然度 | 较自然 | 非常自然 |
| 成本 | 低 | 较高 |
| 偏好支持 | ❌ | ✅ |
| 适用场景 | 快速优化、批量处理 | 深度优化、新品发布 |

### 规则5：曝光量变化预测

展示优化结果时，**必须**对每种方案给出曝光量变化预估。预估规则如下：

1. **热词数量变化**：新标题相比原标题每新增 1 个类目热搜词（tag=`热词`），预估曝光提升 5%-15%
2. **热词权重参考**：`new_title_words` 和 `other_words` 中的 `weight`（权重值）、`min_rnk`（搜索排名）可辅助判断词的流量价值——权重越高、排名越靠前，预估提升越大
3. **年份更新加成**：如果新标题包含当前年份词（如"2026新款"），预估额外提升 3%-8% 曝光
4. **综合预估**：给出一个保守区间（如 "+10% ~ +25%"），并标注免责说明

**免责说明（必须展示）**：
> ⚠️ 曝光预估基于关键词热度数据，实际效果受类目竞争、商品权重、市场环境等多因素影响，仅供参考。

**示例**：

| 方案 | 新增热词数 | 年份更新 | 预估曝光变化 |
|------|----------|---------|------------|
| 方式A | +3 个热词 | 无 | +15% ~ +25% |
| 方式B | +4 个热词 | 含"2026新款" | +20% ~ +35% |

## 使用原则

1. 所有命令均为只读操作，不会修改商品标题
2. 优化结果仅供参考，需用户确认后手动应用
3. 收到优化请求后，应同时调用两种方式并展示结果
4. 如果用户有特殊偏好，应提取并传入 `--preference` 参数
5. 传入 ≥3 个商品时，必须先触发 `select_items_to_optimize` 交互让用户筛选
6. 结果展示必须使用 `title_comparison_card` 表格（3列×每方案4行，方案列合并单元格 + 组级单选），标注生成逻辑及优化说明（含热度）和曝光预估

## 执行前置（首次命中能力时必须）

- 如果用户没有提供商品ID（上下文里没有商品ID），直接按 [`references/interaction-specs.md`](./references/interaction-specs.md) 中 `open_tab_select_product` 的数据结构输出 JSON，流程结束，**不允许反问用户，不允许输出其他内容**
- 首次执行 `optimize_title` 前：先完整阅读 `capabilities/optimize_title.md`
- 首次执行 `optimize_title_llm` 前：先完整阅读 `capabilities/optimize_title_llm.md`
- 首次执行 `get_keyword_info` 前：先完整阅读 `capabilities/get_keyword_info.md`
- 首次执行 `get_tokenizers` 前：先完整阅读 `capabilities/get_tokenizers.md`

## Agent 执行检查清单
在执行优化时，请确认：
- [ ] 提取商品ID
- [ ] 若商品数 ≥ 3，已触发 `select_items_to_optimize` 交互并等待用户选择
- [ ] 已识别并提取用户偏好（如果有）
- [ ] 并发调用 `optimize_title` 和 `optimize_title_llm` 命令
- [ ] 等待两个结果都返回
- [ ] 使用 `title_comparison_card` 表格展示两个结果（含生成逻辑 + 曝光预估）
- [ ] 已给出每种方案的曝光量变化预估及免责说明
