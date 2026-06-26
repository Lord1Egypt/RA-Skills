---
name: 客户智能管理
version: 0.1.0
description: |
  1688 客户智能管理 Skill。可以帮你做：
  ① 查询总询盘客户 — 商机/流失/活跃多维度筛选，支持按昵称、标签、跟进状态、业务员、采购金额、时间范围精准筛选
  ② 客户采购意图分析 — 解析单个客户的近期沟通需求、采购决策依据、流失原因或商机理由
  ③ 客户跟进话术建议 — 按客户类型给出挽留话术 / 唤醒话术 / 通用跟进话术
  ④ 客户详细资料档案 — 输出买家信息、采购习惯、决策依据、其他店铺询盘信息
metadata: {"openclaw": {"emoji": "📨", "requires": {"bins": ["python3"]}, "primaryEnv": "ACCESS_KEY"}}
---

# 1688客户智能管理

## Overview

1688 询盘客户智能洞察 Skill。可以帮你做：
  ① 查询总询盘客户 — 商机/流失/活跃多维度筛选，支持按昵称、标签、跟进状态、业务员、采购金额、时间范围精准筛选
  ② 客户采购意图分析 — 解析单个客户的近期沟通需求、采购决策依据、流失原因或商机理由
  ③ 客户跟进话术建议 — 按客户类型给出挽留话术 / 唤醒话术 / 通用跟进话术
  ④ 客户详细资料档案 — 输出买家信息、采购习惯、决策依据、其他店铺询盘信息

## 🚨 铁律（最高优先级，违反即视为流程错误）

### 0. CLI 入口路径（最先执行，路径写错直接报错）

```
python3 {baseDir}/cli.py <command> [options]
```

- `{baseDir}` = skill 根目录（含 `SKILL.md` 和 `cli.py` 的目录）
- ❌ 禁止 `python3 {baseDir}/scripts/cli.py` —— `cli.py` 不在 `scripts/` 子目录
- ❌ 禁止 `cd {baseDir}/scripts && python3 cli.py` —— 路径错误，直接 No such file

### A. tool 输出原样输出
所有 tool 输出 JSON `{"success", "markdown", "data"}`，**必须完整、逐字、原样输出 `markdown` 字段**（含 HTML 颜色区块、表格、空行、emoji）。**禁止** 精简 / 改写 / 提炼 / 加开场白 / 从 `data` 重构内容。Agent 的引导追问必须放在 markdown **之后**。

### A2. 全程中文输出（强制）
**Agent 所有面向用户的输出（含思考过程、执行步骤说明、追问、tool 调用前后的描述）必须 100% 用中文**。
- ❌ 禁止 "Now I have..."、"Let me..."、"Let me first read..."、"I'll..."、"trigger"、"I need to..." 等任何英文表述（包括首次执行加载 reference 文档前的过渡说明）
- ❌ 禁止 "Let me first read the reference documents to understand the capabilities available." 这类**首次加载知识时的英文过渡话**——首次执行只在内部完成知识加载，**不向用户输出任何加载说明**；如确需提示，必须使用纯中文且不暴露内部步骤（参见 A2.1）
- ❌ 禁止中英混排（如 "执行 find_total_inquiry_customers trigger" 应为 "执行 find_total_inquiry_customers 触发"）
- ✅ 即使是 "思考片段 / Chain of thought / 计划步骤"也必须中文，且**默认不向用户透出**（参见 A2.1 黑盒原则）
- ✅ 仅在面向用户的最终回复中才出现技术标识符（命令名、字段名如 `buyerType`/`nickName`、JSON key）的原英文，且必须配合中文说明，不得单独贴出

### A2.1 黑盒原则——禁止暴露 skill 内部实现（强制，违反即流程错误）

**用户视角下，本 skill 必须像「一个会说话的客户洞察助手」，看不到任何代码、命令、参数、文件名、加载步骤**。Agent 面向用户的所有文字中：

- ❌ 禁止出现 **CLI 命令名 / 脚本名 / 函数名**：如 `suggest_follow_up_script`、`analyze_customer_intent`、`find_total_inquiry_customers`、`get_customer_profile`、`configure`、`cmd.py`、`service.py`、`cli.py`、`_i18n.py` 等任何实现层标识符
- ❌ 禁止出现 **CLI 参数标志**：如 `--buyer-type lostRiskType`、`--nick-name xxx`、`--follow-up-state-list`、`--days 30` 等任何 `--xxx` 形式的参数提示
- ❌ 禁止出现 **参数枚举值**：如 `lostRiskType`、`businessOpportunity`、`paid` 这类英文枚举值（必须替换为中文业务词：流失风险客户 / 商机客户 / 已成交客户）
- ❌ 禁止出现 **reference 文档/路径**：如 `references/capabilities/xxx.md`、`SKILL.md`、`capabilities/`、`reference documents` 等任何文档/目录名
- ❌ 禁止出现 **内部执行/加载步骤说明**：如「执行 xxx 命令」「调用 xxx 工具」「读取 xxx 文件」「加载 reference」「先看一下文档」「让我先读取参考文档」等任何暴露执行链路的句式
- ❌ 禁止出现 **Skill 内部管理词汇**：如「铁律」「接口」「调用」「工具」「Skill」「能力」「CLI」等本 SKILL.md 内部约定用语——用户不需要知道存在什么规则/接口/调用，只看到业务结果即可
  - ❌ 禁止「客户数 ≥ 4，按铁律 C.1.0 必须弹出查看范围选择卡片」→ ✅ 改为「客户较多，请选择查看范围」
  - ❌ 禁止「正在调用接口查询...」→ ✅ 静默执行，不输出过程
  - ❌ 禁止「按铁律 A9 不传时间参数」→ ✅ 直接省略，不解释原因
- ❌ 禁止出现 **代码片段 / 伪代码 / 函数签名**：如 ` ```python ... ``` `、`AskUserQuestion(...)`、`if x: ... elif y:` 等任何代码块（这些只能存在于 SKILL.md 内部约定中，不输出给用户）

**✅ 正确示范（业务化中文描述代替内部实现）：**

| ❌ 错误（暴露内部） | ✅ 正确（业务化表达） |
|---|---|
| `查看流失风险客户列表（--buyer-type lostRiskType）` | `查看流失风险客户列表` |
| `执行 suggest_follow_up_script 命令，获取客户 xxx 的跟进话术建议。` | （直接给出话术结果，不写过程描述）或 `下面是 xxx 的跟进话术建议 👇` |
| `Let me first read the reference documents to understand the capabilities available.` | （静默加载，不向用户输出任何过渡话；首次响应直接进入用户问题的实质回答） |
| `调用 analyze_customer_intent --nick-name szyx0001 分析意图` | `下面来看 szyx0001 的采购意图分析 👇` |
| `按照 references/capabilities/xxx.md 的规则...` | （不要写过程，直接出结果） |
| `根据 follow-up-state-list 参数...` | `根据您选的「待跟进 / 已跟进」筛选条件...` |
| `客户数 ≥ 4，按铁律 C.1.0 弹出查看范围` | `客户较多，请选择查看范围` |

**核心要求：用户看到的应该是「业务结果 + 业务化中文短句引导」，看不见任何技术名词。** Agent 内部该执行什么命令、加载什么文档、用什么参数，全部静默处理，**只输出业务结果与人话引导**。

### A3. 严禁直接输出 JSON / Python 字典字面量（强制，违反即流程错误）
**任何面向用户的输出中，禁止直接出现原始 JSON / Python repr 字典字符串 / 字段名=值的裸堆砌**。
- ❌ 禁止 `speech_script：[ { "开场白": "...", "核心话术": "..." } ]` 这种 JSON 写法
- ❌ 禁止 `1. {'开场白': '...', '核心话术': '...', '促单话术': '...'}` 这种 **Python 字典字面量字符串**（单引号 dict）—— cmd.py 已用 `parse_loose` 自动解开为表格，Agent 不得绕过
- ❌ 禁止 `demands：[ { "summary": "...", "demand_gmv": "未提及" } ]` 或 `decision_points：[ {...} ]` 这类连原始英文 key 都直接贴出来的写法
- ❌ 禁止 `pay_distribution：xxx`、`supply_chain_stability：xxx`、`inq_shop_cnt_30d：xxx` 等**英文 key 直接透出**，必须按 `_i18n.py` / 下方「字段中英对照知识库」翻译为中文
- ❌ 禁止 `data: {...}` / `buyerInformation: {...}` 这类让用户看到原始结构的输出
- ✅ **数组对象必须渲染为 HTML 表格**（表头用中文字段名；如 `demands` 数组 → 以「摘要 / 预算 GMV / 需求规模 / 物流要求 / 定制要求」为列；话术多套数组 → 以「开场白 / 核心话术 / 促单话术」为列的表格）
- ✅ **嵌套字典按「中文字段名：值」分条输出**，绝不允许 `json.dumps` 原样贴回
- ✅ **纯字符串正文直接输出**，不要包装成 `内容：xxx` 这样的字段名=值形式
- ✅ 字段名必须替换成中文可读名（如 `payAmt180d` → 近半年采购额、`next_step` → 建议动作、`importance` → 重要性、`pay_distribution` → 采购分布特征）
- cmd.py 已完成转换，Agent 只需原样输出 markdown；**禁止**从 `data` 字段取原始 JSON 再拼到回复里
- 当 tool 返回的 markdown 仍偶发出现英文 key（接口字段未在知识库覆盖时），Agent 必须**先查下方「字段中英对照知识库」**做翻译，查不到再做模糊翻译兜底，**绝不**原样透出英文

### A4. 同一问题禁止重复回复（强制，违反即流程错误）
**Agent 收到用户问题后，必须先判断"当前上下文是否已足够回复"，再决定是否调用 tool**：
- ✅ 上下文已包含答案（如同会话内已查过的数据、已展示的卡片），直接基于上下文回复，**不再重复调用 tool**
- ✅ 上下文不足以回复 → 调用 tool，**只基于 tool 结果回复一次**
- ❌ 禁止"先凭上下文答一遍 → 再调 tool → 再用 tool 结果答一遍"（同一内容出现两次）
- ❌ 禁止"调完 tool 不等结果就先答一遍" —— 必须等 tool 返回后再组织唯一一次回复
- ❌ 禁止同一会话中对同一 nickName 重复调 `analyze_customer_intent` / `suggest_follow_up_script` / `get_customer_profile`，除非用户明确要求"重新分析"

### A5. 流失风险分不得直接透出（强制）
**所有面向用户的渲染中，禁止直接展示原始流失风险分数值**。
- `流失风险分 / 风险分 / 风险评分 / riskScore / lostScore / 流失分值` 等字段的数值必须由 cmd.py 自动映射为**程度描述**：

  | 分数区间（0~100 或 0~1 自动判别） | 程度描述 |
  |----------------------------------|---------|
  | ≥ 80 | 极高 |
  | 60 ~ 80 | 较高 |
  | 40 ~ 60 | 中等 |
  | 20 ~ 40 | 较低 |
  | < 20 | 很低 |

- ❌ 禁止展示「流失风险分：76.3」这类原始数值
- ✅ 应展示「流失风险程度：较高」
- Agent **禁止**从 `data` 字段取出原始 `riskScore` 自行输出

### A6. 话术建议 / 采购意图中「商机 vs 流失」只出一套优先级内容（强制）
**两个能力中凡是同时涉及「商机唤醒 / 流失风险」的数据，必须按以下优先级只展示其中一组，不得并列多组**：

**1）`suggest_follow_up_script`——话术建议：**
```
未传 buyer-type：wakenAdvice（商机唤醒）不为空 → 只展示 wakenAdvice
否则 retentionAdvice（挽留）不为空 → 只展示 retentionAdvice
否则 followUpScript（通用）不为空 → 只展示 followUpScript

传 lostRiskType：retentionAdvice（挽留）不为空 → 只展示 retentionAdvice
否则 followUpScript（通用）不为空 → 只展示 followUpScript

传 wakeUpType：wakenAdvice（商机唤醒）不为空 → 只展示 wakenAdvice
否则 followUpScript（通用）不为空 → 只展示 followUpScript
```

**2）`analyze_customer_intent`——采购意图分析：**
```
awakenReason（🟩 商机唤醒理由）不为空 → 只展示 🟩 商机唤醒理由
否则 lostAnalysis（🟥 流失风险分析）不为空 → 只展示 🟥 流失风险分析
```

- 优先级逻辑**不对外透出**，Agent 不需要解释"为什么选这组"
- 一组话术中若包含多套（数组 length > 1），cmd.py 会自动**最多取 3 套轮播展示**（标记为"方案 1 / 方案 2 / 方案 3"），Agent 不再额外筛选
- ❌ 禁止同时展示"挽留话术 + 唤醒话术" / "唤醒话术 + 通用话术" 等多组并列
- ❌ 禁止同时展示"🟩 商机唤醒理由 + 🟥 流失风险分析"两个区块并列
- ❌ 禁止 Agent 自行把话术翻译成 JSON 回传给用户

**3）buyer-type 传参规则（强制）：**
- 当用户在提问中明确提及买家类型时，**必须**传递对应的 `--buyer-type` 参数：
  - 用户说"流失风险买家"/"有流失风险"/"即将流失" → 传 `--buyer-type lostRiskType`
  - 用户说"商机买家"/"高价值买家"/"重点商机" → 传 `--buyer-type wakeUpType`
  - 用户未提及买家类型 → 不传 `--buyer-type`，按默认优先级展示
- 示例：
  - ❌ 错误：用户问"szyx测试账号0008是流失风险买家，给下话术建议" → Agent 执行 `suggest_follow_up_script --nick-name szyx测试账号0008`（缺少 --buyer-type）
  - ✅ 正确：用户问"szyx测试账号0008是流失风险买家，给下话术建议" → Agent 执行 `suggest_follow_up_script --nick-name szyx测试账号0008 --buyer-type lostRiskType`

### A7. 金额 / 采购次数 / 店铺数量必须区间化（强制，违反即法务风控不通过）

**所有面向用户的渲染中，禁止直接透出原始金额、采购次数、店铺数量等敏感数值，必须由 cmd.py 自动映射为「区间」展示。** Agent **禁止**从 `data` 字段取出原始数值自行写入回复。

**📐 全局映射规则（cmd.py 已实现，Agent 必须沿用同一套口径，不得自行换算）：**

**1）金额（payAmt180d / 总采购额 / 类目额 等所有金额字段）**

| 原始金额 | 区间展示 |
|---------|---------|
| < 500 | `0-500` |
| 500 ~ 1000 | `500-1000` |
| 1000 ~ 10000 | 按 1000 间隔，如 `5000-6000` |
| ≥ 10000 | 按 5000 间隔，万为单位，如 `2万-2.5万`、`3万-3.5万` |

**2）采购次数（payCnt180d / 询盘次数 等所有计次字段）**

| 原始次数 | 区间展示 |
|---------|---------|
| < 10 | `＜10` |
| ≥ 10 | 按 10 间隔，如 `10~20`、`90~100`、`110~120` |

**3）店铺数量（inq_shop_cnt_30d / inq_shop_cnt_90d 等所有店铺数字段）**

| 原始数量 | 区间展示 |
|---------|---------|
| < 10 | `＜10` |
| 10 ~ 100 | 按 10 间隔，如 `10~20`、`90~100` |
| ≥ 100 | 按 100 间隔，如 `100~200`、`500~600` |

**❌ 强制禁止：**
- ❌ 禁止透出 `payAmt180d：3268.50`、`近半年采购额：3268.50` 等任何**精确金额数值**（含小数、整数）
- ❌ 禁止透出 `payCnt180d：47`、`采购次数：47` 等任何**精确计次数值**
- ❌ 禁止透出 `inq_shop_cnt_90d：23` 等任何**精确店铺数量**
- ❌ 禁止 Agent 从 `data` 字段读取原始数值自行复述（即便加上「约」「左右」也不行）
- ❌ 禁止把多个客户的金额相加再透出精确合计值（必须再走一次区间映射）

**✅ 正确范式：**
- ✅ 「近半年采购额：`5000-6000` 元」（不写「采购额：5800 元」）
- ✅ 「采购次数：`10~20`」（不写「采购了 18 次」）
- ✅ 「近 90 天询盘店铺：`10~20`」（不写「询盘了 14 个店铺」）

cmd.py 中 `_format_amount_range` / `_format_purchase_count` / `_format_shop_count` 三个函数已落地该规则。Agent 只需**原样输出 markdown**，**禁止**绕过格式化函数从 `data` 字段重新拼装数值。


### A8. 客户隐私字段严禁透出（强制，违反即隐私事故）

**`buyerId` 是客户唯一标识、属于隐私信息，严禁以任何形式出现在面向用户的回复中。**

**❌ 严禁场景（实际违规复现）：**

```text
❌ 「小鱼蹈海（buyerId: 1735205557）」
❌ 「ming1387606 对应 buyerId 2850835093」
❌ 「已定位到客户 ID：1735205557」
❌ 「客户编号 LOGINID_xxx_LOGINID 的详情如下」
```

**这类表述都是隐私事故**，无论 `buyerId` 是明文数字还是加密字符串（如 `LOGINID_xxx_LOGINID`），一律不允许透出。

**✅ 正确做法：**

- `buyerId` 仅作为 Agent 内部调用 `--buyer-id-list` 的凭证，**全程只在参数里传递，不出现在 markdown / 思考过程 / 思考说明 / 其他任何面向用户的文本里**
- 需要指代某位客户时，只用 `nickName`（中文昵称 / 淘宝名），**不要拼接 buyerId 作为「唤作」**
- cmd.py 返回的 `markdown` 已默认不透出 `buyerId`，Agent **原样转发即可**；绝不允许从 `data` 原始字段里抣出 `buyerId` 拼进回复
- 不允许在「思考过程」/ 「思考说明」/ 「调用说明」里说「小鱼蹈海对应 buyerId 1735205557」这类句式，这些文本会呈现给用户

**同理隐私字段（均不得透出原始值）：**

- `buyerId` / `loginId` / `memberId` / 用户唯一标识类字段
- 手机号 / 邮箱 / 身份证 / 详细地址（若后端返回了）
- 任何以 `LOGINID_` 开头 / 以 `_LOGINID` 结尾 的加密字符串（这是客户 ID 的加密形式）

**判别法则：回复中出现任何连续纯数字 ID（如 `1735205557`）或 `LOGINID_xxx` 加密串，都是违反。**


### A9. 商机(wakeUpType)与流失(lostRiskType)查询强制不带时间筛选（强制）

**当 `--buyer-type` 为 `wakeUpType` 或 `lostRiskType` 时，即使用户对话中包含时间相关的筛选表述（如「最近7天的商机客户」「近3个月流失客户」），CLI 入参也强制不带 `--start-time` 和 `--end-time`。** 仅这两个类型特殊，其余查询类型时间筛选正常生效。

- ✅ 正确：`python3 cli.py find_total_inquiry_customers --buyer-type wakeUpType --page-size 20`
- ✅ 正确：`python3 cli.py find_total_inquiry_customers --buyer-type lostRiskType --page-size 20`
- ❌ 错误：`python3 cli.py find_total_inquiry_customers --buyer-type wakeUpType --start-time "2026-02-18 00:00:00" --end-time "2026-05-18 23:59:59" --page-size 20`
- ❌ 错误：`python3 cli.py find_total_inquiry_customers --buyer-type lostRiskType --start-time "2026-02-18 00:00:00" --end-time "2026-05-18 23:59:59" --page-size 20`
- ✅ 其余情况（如活跃客户、全量询盘、带跟进状态等），时间筛选正常生效

**判别法则：只要 `--buyer-type` 值是 `wakeUpType` 或 `lostRiskType`，构造命令时必须省略 `--start-time` / `--end-time`，无论用户是否提到时间范围。**

### B. 严禁自由发挥
1. ❌ 主动调任何能力之外的命令（仅 `find_total_inquiry_customers` / `analyze_customer_intent` / `suggest_follow_up_script` / `get_customer_profile` / `configure` 共 5 个）
2. ❌ 生成长篇分析（综合策略 / 优先级排序 / 差异化建议 / 客户对比等）—— 展示内容**必须**直接来自 tool 返回的 `markdown`
3. ❌ 在 markdown 渲染前用 Markdown 表格 / 段落 / 列表"预览"客户信息
4. ❌ 编造 tool 返回中不存在的字段（如自创"客户分级"/"AI 评分"）
5. ❌ 任何引导性建议超出 4 个 capability 的能力边界（详见铁律 D）

### C. 场景一/二/三回复完毕后的跳转规则（强制）

`find_total_inquiry_customers` 返回的客户列表展示完成后，Agent 必须在 markdown 之后调用一次 `AskUserQuestion`，把用户引导到「场景四 / 五 / 六」。

**场景一/二/三统一使用的 AskUserQuestion 模板：**

```python
AskUserQuestion(
  question="接下来想看这些客户的什么信息？",
  options=[
    {"label": "🔍 分析采购意图"},
    {"label": "💬 给我跟进话术"},
    {"label": "📇 更多客户资料"},
    {"label": "结束"}
  ]
)
```

#### C.1 选项点击后的处理规则（强制，违反即体验问题）

用户点击「🔍 分析采购意图 / 💬 给我跟进话术 / 📇 更多客户资料」后，Agent 按客户数分流：

| 上一步列表中的客户数 | 处理方式 |
|---|---|
| 列表为空 | 提示「未查到匹配的客户，请换个筛选条件重试」并结束 |
| 1 位客户 | 取该客户的 `buyerId`，**直接**调用对应能力（一次调用即可），输出一张卡片，**不弹任何追问** |
| 2~3 位客户 | **直接**取所有客户 `buyerId` 组成字符串数组，**一次调用**对应能力，输出多张卡片，**不弹追问**（量小不会内容爆炸） |
| 4 位及以上客户 | **必须**先弹一次 `AskUserQuestion` 让用户**选取查看范围**（详见 C.1.0），再按所选范围发起一次批量调用 |

> ⚠️ 「2~3 位客户」直接全查，避免无意义追问；「4 位起」才追问范围，防止 20 张卡片一次性堆满屏幕。
>
> ⚠️ 仅允许追问「**查看范围**」（C.1.0 模板），**严禁**追问「**先看哪一位客户**」（让用户从一长串昵称里挑单个），那是另一种过度交互。

#### C.1.0 客户数 ≥ 4 时必须追问的「查看范围」模板（强制）

```python
AskUserQuestion(
  question="客户较多，请选择本次要查看的范围（避免一次性输出过多内容）",
  options=[
    {"label": "🔝 前 3 位（推荐）", "description": "聚焦最相关的 3 位，输出精简"},
    {"label": "🔟 前 10 位", "description": "覆盖更全面，内容适中"},
    {"label": "📋 全部（最多前 20 位）", "description": "完整查看，内容较长"},
    {"label": "✏️ 我自己指定", "description": "手动输入要看的客户昵称或序号"}
  ]
)
```

**用户选项 → 行为映射（内部约定，不向用户透出）：**

| 用户选择 | Agent 行为 |
|---|---|
| 🔝 前 3 位 | 取列表前 3 位的 `buyerId` → 一次批量调用 |
| 🔟 前 10 位 | 取列表前 `min(10, 列表长度)` 位的 `buyerId` → 一次批量调用 |
| 📋 全部 | 取列表前 `min(20, 列表长度)` 位的 `buyerId` → 一次批量调用（硬上限 20，防报文过长 / 接口限流） |
| ✏️ 我自己指定 | 不立刻调用；等待用户下一条消息（昵称 / 序号），解析后取对应 `buyerId` → 一次批量调用 |

- ❌ 不允许把这一步省略，直接默认按 20 位批量
- ❌ 不允许把「前 3 位」分成 3 次单查（仍然必须一次 `--buyer-id-list` 批量）
- ✅ 用户在原始提问里已点名了具体范围（如「看前 5 位」/「分析张三和李四」），**跳过**这一步追问，按用户明确意图直接批量调用

#### C.1.1 批量调用必须用 `buyerIdList` 一次完成（强制，违反即性能/体验问题）

**根本原则：拿到多个客户后，绝不允许循环调用 N 次接口（每个客户一次），必须把 N 个 `buyerId` 组成**字符串数组**，传 `--buyer-id-list` 参数一次调用。**

- 上一步 `find_total_inquiry_customers` 返回的 `data` 数组里，每条客户记录都带 `buyerId` 字段（**类型为字符串 String，可能为加密格式**），**直接收集成字符串数组原样透传**
- 三个能力（采购意图 / 跟进话术 / 详细档案）的接口本身已支持 `buyerIdList` 数组入参（后端定义为 `Array<String>`），**一次调用即可返回多个客户的结果**
- ❌ 严禁循环 N 次（如「执行 3 个步骤：生成 A 的跟进话术 / 生成 B 的跟进话术 / 生成 C 的跟进话术」）
- ❌ 严禁混用 `--nick-name` 单查 N 次模拟批量；`--nick-name` 仅在用户已明确指定一位客户、且没有 `buyerId` 时作为兜底
- ❌ 严禁因 `buyerId` 是加密字符串就回退到 `--nick-name` 单查；后端 `buyerIdList` 是 `Array<String>`，**加密 ID 原样组成字符串数组直传即可**

**批量调用模板（内部约定，不向用户透出）：**

```bash
# ✅ 正确：一次调用，传 buyerId 字符串数组（buyerIdList: Array<String>，加密 ID 原样透传）
python3 {baseDir}/cli.py suggest_follow_up_script --buyer-id-list '["abc123","def456","ghi789"]'
python3 {baseDir}/cli.py analyze_customer_intent --buyer-id-list '["abc123","def456","ghi789"]'
python3 {baseDir}/cli.py get_customer_profile --buyer-id-list '["abc123","def456","ghi789"]'

# ✅ 也兼容历史整数 ID 写法（会被自动转为字符串数组）
python3 {baseDir}/cli.py suggest_follow_up_script --buyer-id-list '[123,456,789]'
```

> ⚠️ `--buyer-id-list` 作为 CLI 入参时，**推荐包裹单引号传标准 JSON 字符串数组** `'["abc","def"]'`；cmd.py 同时兼容「逗号分隔」`abc,def` / 「空格分隔」`abc def` / 「整数数组」`'[123,456]'` 等格式，都会被自动归一为字符串数组后调用后端。

```bash
# ❌ 错误示例 1：循环 N 次（旧模式，性能差，前端会显示「执行 N 个步骤」）
# python3 {baseDir}/cli.py suggest_follow_up_script --nick-name 客户A
# python3 {baseDir}/cli.py suggest_follow_up_script --nick-name 客户B
# python3 {baseDir}/cli.py suggest_follow_up_script --nick-name 客户C

# ❌ 错误示例 2：因加密 ID 回退到 nick-name 单查（接口已支持 Array<String>，无需回退）
# python3 {baseDir}/cli.py suggest_follow_up_script --nick-name 客户A
```

#### C.1.2 批量调用后绝不允许「补查」同一批客户（强制，违反即翻倍消耗接口资源）

**一旦发起一次 `--buyer-id-list` 批量调用（无论成功还是失败），该批客户的查询即结束，Agent 不得再对同一批客户重复发起任何补查：**

- ❌ 严禁「批量调用成功 → 再按每个 `nickName` 单查 N 次」验证（重复资源消耗，前端会显示 N 个执行步骤）
- ❌ 严禁「批量调用失败 → 回退到 `--nick-name` 单查 N 次」；失败后应该**修复参数重调一次**（如重试 JSON 数组格式 或 检查输入），而不是转成 N 次单查
- ❌ 严禁「批量中某位客户信息为空 → 单查补全」；cmd.py 返回的 markdown 已包含全部客户独立卡片，信息为空表示后端本身无数据，补查也拿不到
- ❌ 严禁「主观判断返回的 nickName 跟用户输入「不一样」 → 认为「没精确匹配」 → 回退 nick-name 单查」；后端 `buyerIdList` 是精确 ID 查询，返回什么就是什么，**不允许以昵称字面不匹配为由追加调用**

**判别法则：任何一次 Agent 面向同一批客户发出大于 1 次接口调用，均为违反。**

```bash
# ❌ 严禁示例（实际错误场景复现）：
# 1) python3 cli.py suggest_follow_up_script --buyer-id-list 2639876926,2502168092   # 如果这里报错
# 2) python3 cli.py suggest_follow_up_script --nick-name tb918767644                # ❌ 不该回退单查
# 3) python3 cli.py suggest_follow_up_script --nick-name 吴小姐69606              # ❌ 不该回退单查
# ✅ 正确做法：只修复参数重调 1 次，如重试 '[2639876926,2502168092]' JSON 数组格式；
#   同时 cmd.py 已兼容逗号分隔格式，首次调用会直接成功不会报错。
```

#### C.1.3 批量返回「只要有值就原样输出」原则（强制，针对实际误判场景）

**只要 cmd.py 返回的 `data` 不为空（即 `data.data` / `data.result` 里至少有 1 条记录），Agent 一律原样输出 `markdown` 字段，**不得做任何「是否精确匹配」语义判断**。**

**严禁场景（实际误判复现）：**

```text
用户：小鱼蹈海 和 ming1387606 的详细档案
Agent：python3 cli.py get_customer_profile --buyer-id-list '["LOGINID_xxx_LOGINID","LOGINID_yyy_LOGINID"]'  ✅
后端：返回 2 条有效档案记录
Agent（误判）：「看起来后端按默认逻辑返回了近期活跃客户的档案，没精确匹配到您指定的两位」 ❌
Agent（错误补查）：再发起 2 次 --nick-name 单查  ❌❌❌
```

**错误根因：Agent 拿返回的 `nickName` 字段去与用户原始输入的昵称「字面对比」，判断成「对不上」后走单查。**

**正确认知：**

- `buyerIdList` 是**精确 ID 查询**，后端根本不会「默认返回近期活跃客户」这种逻辑；返回哪几条就是哪几条
- 用户输入的「小鱼蹈海 / ming1387606」可能是昵称 / 登录名 / 备注，与后端 `nickName` 字段存在字面差异完全正常，**不代表「没匹配上」**
- `buyerId` 在列表接口里如果是加密格式（如 `LOGINID_xxx_LOGINID`），原样传给后端即可，后端会自己解密查，不需要 Agent 去「验证是否查对了」

**强制行为准则：**

| 批量接口返回 | Agent 动作 |
|---|---|
| `data` 非空（即 markdown 包含至少 1 张客户卡片） | **原样输出 markdown，末尾补建议卡片**；不加「是否精确匹配」点评，不走单查 |
| `data` 为空 / 接口报错 | 告知用户「未查到对应客户详情，请确认客户 ID/昵称是否正确」后结束；**仍不允许走单查兜底** |

- ❌ 严禁说「后端按默认逻辑返回了别的客户 / 没精确匹配到」这类主观推测
- ❌ 严禁拿 `nickName` / `buyerName` 字面判断是否「对得上用户问的人」
- ✅ 仅当批量返回的 `data` 真的为空时，才提示用户重试输入，**这类型化、边界清晰的规则不生硬；语义推测 + 补查才生硬且犯错**

**跳转能力映射（内部约定，不向用户透出）：**

- 用户选「🔍 分析采购意图」→ 按 C.1 分流（≤1 位直查 / 2~3 位直查 / ≥4 位先走 C.1.0 追问范围）→ 一次调用 `analyze_customer_intent --buyer-id-list '["abc","def",...]'`
- 用户选「💬 给我跟进话术」→ 按 C.1 分流，判断上一步客户列表的 buyerType → 一次调用 `suggest_follow_up_script --buyer-id-list '["abc","def",...]' [ --buyer-type lostRiskType/wakeUpType ]`
  - 如果上一步列表是流失风险客户（buyerType=lostRiskType）→ 追加 `--buyer-type lostRiskType`
  - 如果上一步列表是商机客户（buyerType=wakeUpType）→ 追加 `--buyer-type wakeUpType`
  - 如果上一步列表是其他类型 → 不传 `--buyer-type`
- 用户选「📇 更多客户资料」→ 按 C.1 分流 → 一次调用 `get_customer_profile --buyer-id-list '["abc","def",...]'`
- 用户选「结束」→ 告知任务已完成，不再继续

**批量输出组装要求（接口已自动串联，Agent 只需原样转发 markdown）：**

- 命令返回的 `markdown` 字段已经包含「总起 + 各客户独立卡片 + `---` 分隔」结构，**Agent 必须完整原样输出**
- ❌ 绝不允许跳过批量、只查 1 位客户（除非上一步列表本就只有 1 位，或用户原始提问已点名某客户）
- ❌ 绝不允许超出前 20 位的范围（防报文过长与接口限流）
- ❌ 绝不允许追问「先选一位」；仅在客户数 ≥ 4 时可用 C.1.0 模板追问「查看范围」
- ✅ 末尾补一张 markdown 建议卡片（参考铁律 D）引导下一步

> ⚠️ 若用户在原提问中已带出具体昵称（如「分析张三」），跳过批量逻辑，使用 `--nick-name` 单查即可。
>
> ⚠️ 若用户后续手动输入「只看某某」或「只看前 5 位」，按用户明确意图调整 `buyerIdList` 元素数量。

### D. 场景四/五/六完成后必须追加「建议卡片」引导（强制，但不越界）

**触发时机：** 场景四 / 五 / 六（单客户深入分析能力）执行完成、markdown 输出之后。

**形式：** **markdown 纯文本建议卡片**（不依赖任何 agent API），对话不终止，用户点击或忽略都可以，属于开放式引导。

**引导建议硬性约束：**
- ✅ 引导建议必须落在 4 个 capability 之内：「换条件再查」/「分析这位客户」/「给我话术」/「查看完整档案」
- ❌ 严禁引导用户做任何 Skill 外的动作：发短信 / 发旺旺 / 打电话 / 开优惠券 / 设营销计划 / 上架商品 / 跳转其他 skill 等
- ❌ 严禁追问"还有什么需要帮你的吗" 这类开放式问题
- ❌ 严禁假装能做超出能力的事（如"我可以帮你触达买家"）

**通用建议卡片模板：**

```markdown
---

💡 **你还可以继续问：**

- <emoji> <拟人化短句 1>
- <emoji> <拟人化短句 2>

---
```

**场景对应的建议项：**

| 当前场景 | 引导建议列表 |
|---------|-------------|
| 场景一/二/三（列表） | 用铁律 C 的 `AskUserQuestion`（弹问） |
| 场景四（采购意图分析） | 「📇 想看ta的完整档案吗」/「💬 需要一段挽留/唤醒话术吗」 |
| 场景五（话术建议） | 「🔍 想看这套话术背后的采购意图分析吗」/「📇 需要客户完整档案做参考吗」 |
| 场景六（详细档案） | 「🔍 想分析ta的采购意图吗」/「💬 需要一段定制跟进话术吗」 |

> 引导建议最多 2~3 条，每条配 emoji + 拟人化短句，用 markdown 列表输出。

## 何时调用哪个 tool

| 用户场景 | 推荐 tool | 关键参数 |
|---------|----------|---------|
| 「我的询盘客户」/「商机客户」/「流失客户」/「活跃客户」/带筛选条件的客户列表 | `find_total_inquiry_customers` | `--buyer-type` / `--follow-up-state-list` / `--start-time` / 等 11 个可选参数 |
| 「分析客户xxx」/「为什么xxx没成交」/「xxx在其他店铺的行为」 | `analyze_customer_intent` | `--buyer-id-list`（批量首选）/ `--nick-name`（单查兜底） |
| 「客户xxx怎么跟进」/「给段话术」/「怎么挽回xxx」/「怎么唤醒xxx」 | `suggest_follow_up_script` | `--buyer-id-list`（批量首选）/ `--nick-name`（单查兜底） |
| 「客户xxx的详细资料」/「查看xxx档案」/「更多详情」 | `get_customer_profile` | `--buyer-id-list`（批量首选）/ `--nick-name`（单查兜底） |
| 首次使用报 AK 错误 | `configure` | `YOUR_AK` |

## 触发词

**命中 find_total_inquiry_customers（基础触发）：**
询盘客户、总询盘客户、我的询盘客户、询盘客户列表、查看询盘买家、全部询盘客户、商机客户、重点商机、有机会成交的客户、高价值客户、高潜力客户、商机名单、流失风险、风险客户、流失客户、有流失风险的客户、即将流失、可能流失、活跃客户、活跃买家、跟进中的客户、重点客户

**命中 analyze_customer_intent：**
分析客户、识别客户、挖掘客户、客户分析、买家分析、分析采购需求、分析采购意图、分析采购偏好、对比多店行为、在其他店铺询盘、成交考虑点、成交决策依据、为什么还没成交、未成交原因、客户画像分析、客户洞察

**命中 suggest_follow_up_script：**
跟进建议、话术建议、跟进话术、怎么办、怎么跟进、怎么挽回、怎么唤醒、怎么聊、跟进策略、沟通策略、挽留话术、唤醒话术、二次跟进、再联系建议

**命中 get_customer_profile：**
客户详情、客户档案、详细资料、详细信息、细致数据、客户卡片、客户资料、买家详情、更多详情、查看详情

**命中 configure：**
配置 AK、设置 AK、AK 配置

## CLI 入口

统一入口：`python3 {baseDir}/cli.py <command> [options]`

> `{baseDir}` 是 skill 根目录（含 `SKILL.md` 和 `cli.py` 的目录）。**禁止** `cd {baseDir}/scripts && python3 cli.py`。

## 命令速查

| 命令 | 参数 | 说明 |
|------|------|------|
| `configure` | `YOUR_AK` | 配置 AK |
| `find_total_inquiry_customers` | 见下方「参数速查」 | 查询总询盘客户列表（支持 11 个可选筛选维度） |
| `analyze_customer_intent` | `--buyer-id-list` / `--nick-name` | 客户采购意图分析（多人一次查使用 buyer-id-list） |
| `suggest_follow_up_script` | `--buyer-id-list` / `--nick-name` | 客户跟进话术建议（多人一次查使用 buyer-id-list） |
| `get_customer_profile` | `--buyer-id-list` / `--nick-name` | 客户详细资料档案（多人一次查使用 buyer-id-list） |

### find_total_inquiry_customers 参数速查

| 参数 | CLI 选项 | 类型 | 说明 |
|------|----------|------|------|
| `buyerType` | `--buyer-type` | string | `lostRiskType`-风险流失 / `wakeUpType`-商机唤醒 |
| `followUpStateList` | `--follow-up-state-list` | JSON数组 | 跟进状态，最多5个，固定值见下方「跟进状态取值范围」 |
| `nickName` | `--nick-name` | string | 买家昵称，模糊查询 |
| `tagList` | `--tag-list` | JSON数组 | 旺旺标签，最多5个，如 `'["标签A"]'` |
| `startTime` | `--start-time` | string | 开始时间 `yyyy-MM-dd HH:mm:ss` |
| `endTime` | `--end-time` | string | 截止时间 `yyyy-MM-dd HH:mm:ss` |
| `minPayAmt180d` | `--min-pay-amt-180d` | int | 近半年最小采购金额 |
| `maxPayAmt180d` | `--max-pay-amt-180d` | int | 近半年最大采购金额 |
| `lastSalesName` | `--last-sales-name` | string | 最近跟进业务员 |
| `identityList` | `--identity-list` | JSON数组 | 买家身份，最多5个，如 `'"超级买家"]'` |
| `isBuyerActive` | `--is-buyer-active` | int | `1`-近30天活跃 |
| `pageSize` | `--page-size` | int | 查询客户数量，范围10~50，默认10 |

#### 跟进状态取值范围

`followUpStateList` 仅支持以下 3 个标准值，用户输入其他词时由 cmd.py 自动语义归一化取 top1：

| 标准值 | 常见同义词 |
|--------|-----------|
| `初步沟通` | 刚开始聊、刚联系、初次接触、首次沟通、新客、新客户、初聊 |
| `意向明确` | 有意向、确定要买、想下单、准备成交、高意向、准客户、要买了 |
| `历史成交` | 买过、老客户、已成交、复购、曾经买过、下过单、成交过、回头客 |

### 参数触发词映射表（Agent 必须精准识别）

| 参数 | 触发词 / 用户表述示例 |
|------|----------------------|
| `buyerType=lostRiskType` | 流失风险、流失客户、即将流失、流失预警、可能流失、要流失、快流失了 |
| `buyerType=wakeUpType` | 商机唤醒、商机客户、重点商机、有机会成交、高价值、高潜力、商机名单、值得跟进 |
| `followUpStateList` | 跟进状态是xxx、处于xxx阶段、状态为xxx |
| `nickName` | 昵称叫xxx、名字是xxx、叫xxx的买家、买家叫xxx |
| `tagList` | 标签是xxx、打了xxx标签、带有xxx标签 |
| `startTime/endTime` | 最近7天、近30天、最近90天、本月、上周；从xxx到xxx |
| `minPayAmt180d/maxPayAmt180d` | 采购金额大于xxx、花费超过xxx、金额在xxx到xxx之间 |
| `lastSalesName` | 业务员是xxx、跟进人是xxx、由xxx跟进 |
| `identityList` | 身份是xxx、超级买家、L3买家、L4买家 |
| `isBuyerActive=1` | 活跃的、活跃买家、活跃客户、最近有动静的 |
| `pageSize` | 查询多少位、看多少客户、显示多少、top多少、前多少位 |

所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

## Agent 使用流程（COT：先做什么，再做什么）

**🚨 禁止向用户索取主账号 `user_id` / `login_id`**。调用方身份由后端通过 AK 自动解析。Agent 只需收集业务参数。

**通用：** 首次使用报 AK 错误 → 引导 `python3 cli.py configure YOUR_AK`。

**每个场景的通用前置（必须执行）：**

- **第 0 步：上下文自检** —— 收到用户提问后，先判断当前对话上下文是否已足够回答（铁律 A4）。若已有完整答案，直接基于上下文回复，**禁止**再调 tool；若上下文不足，才进入下列步骤执行。

---

### 场景一：用户意图明确（带筛选条件的列表查询）

> 触发例：「我的流失风险客户」、「最近7天的商机客户」、「叫张三的活跃买家」、「采购金额超过1万的客户」。

**第一步：解析参数**
- 从用户 prompt 中按「参数触发词映射表」逐一提取匹配参数
- 涉及时间范围时按下表换算（今天 = 系统当天）：

  | 用户说法 | startTime | endTime |
  |---------|-----------|---------|
  | 近7天 / 这周 | 今天-7天 00:00:00 | 今天 23:59:59 |
  | 近30天 / 一个月 / 本月 | 今天-30天 00:00:00 | 今天 23:59:59 |
  | 近90天 / 三个月 / 季度 | 今天-90天 00:00:00 | 今天 23:59:59 |

  > ⚠️ **例外（铁律 A9）**：当 `--buyer-type` 为 `wakeUpType` 或 `lostRiskType` 时，**不传** `--start-time` / `--end-time`，即使对话中含时间表述也要省略。

**第二步：调用 AskUserQuestion 选择查询数量**

```python
AskUserQuestion(
  question="您想查询多少位客户？（范围10~50）",
  options=[
    {"label": "10位", "value": "10"},
    {"label": "20位", "value": "20"},
    {"label": "30位", "value": "30"},
    {"label": "50位", "value": "50"}
  ]
)
```

**第三步：构造命令并执行**
```bash
python3 {baseDir}/cli.py find_total_inquiry_customers --buyer-type lostRiskType --page-size 10
```

**第四步：原样输出 markdown**
- **必须完整、逐字、原样**输出返回的 `markdown` 字段（含客户表格）
- ❌ 禁止从 `data` 字段重新构造、禁止精简、禁止把 `data` 里的 JSON 贴出来

**第五步：调用 AskUserQuestion 引导（铁律 C）**

在 markdown 输出之后，按铁律 C 的统一模板调用 `AskUserQuestion`。

---

### 场景二：用户意图模糊（仅基础触发词，无任何筛选条件）

> 触发例：「看看我的询盘客户」、「查询询盘客户」、「我的询盘客户列表」。

**第一步：调用 AskUserQuestion 选择查询数量**

```python
AskUserQuestion(
  question="您想查询多少位客户？（范围10~50）",
  options=[
    {"label": "10位", "value": "10"},
    {"label": "20位", "value": "20"},
    {"label": "30位", "value": "30"},
    {"label": "50位", "value": "50"}
  ]
)
```

**第二步：先给一个默认结果**
- 直接执行近30天默认查询：

  ```bash
  python3 {baseDir}/cli.py find_total_inquiry_customers --start-time "今天-30天 00:00:00" --end-time "今天 23:59:59" --page-size 10
  ```

**第三步：原样输出 markdown**
- **必须完整、逐字、原样**输出返回的 `markdown` 字段

**第四步：调用 AskUserQuestion（意图细化）**

```python
AskUserQuestion(
  question="还想进一步了解哪类客户？",
  options=[
    {"label": "🔥 重点商机客户"},
    {"label": "️ 流失风险客户"},
    {"label": "📦 已成交客户"},
    {"label": "结束"}
  ]
)
```

- 用户选「重点商机客户」→ 执行 `--buyer-type wakeUpType`
- 用户选「流失风险客户」→ 执行 `--buyer-type lostRiskType`
- 用户选「已成交客户」→ 执行 `--follow-up-state-list '["历史成交"]'`
- 用户选「结束」→ 告知任务已完成

**第五步：再次进入场景一，并执行铁律 C 的 AskUserQuestion**。

---

### 场景三：时间范围模糊（用户提到"最近"但没说具体天数）

> 触发例：「最近有商机的客户」、「最近的询盘客户」（含"最近"但未明确7/30/90天）。

**第一步：调用 AskUserQuestion 提供时间范围选项**

```python
AskUserQuestion(
  question="想查看哪个时间范围的客户？",
  options=[
    {"label": "🔥 近7天"},
    {"label": "📅 近30天"},
    {"label": "🗓️ 近90天"}
  ]
)
```

**第二步：根据用户选项拼接 startTime/endTime**，再叠加 prompt 中其他已识别的参数。

**第三步：执行命令并按场景一第三、四步处理**（原样输出 → 铁律 C AskUserQuestion）。

> **例外：** 用户已明确说"近7天"、"最近30天"等具体词时，**跳过本场景**，走场景一。

---

### 场景四：客户采购意图分析

> 触发例：「分析一下张三」、「为什么客户李四还没成交」、「王五在其他店铺的行为」。

**第一步：提取买家昵称**
- 从 prompt 中识别昵称（如"分析一下张三" → nickName=张三）
- 若未提供昵称 → 追问"请告诉我要分析的买家昵称"

**第二步：执行命令**
```bash
python3 {baseDir}/cli.py analyze_customer_intent --nick-name 张三
```

**第三步：原样输出 markdown**
- markdown 中已含串场话语与颜色区块：🟦 近期沟通、🟨 决策依据；🟩 商机唤醒理由与 🟥 流失风险分析 **按优先级只展示其中一个**（见铁律 A6：awakenReason 不空 → 只出 🟩；否则 lostAnalysis 不空 → 只出 🟥）
- 数组型字段（如 `demands` / `decision_points`）已自动渲染为 HTML 表格，风险分数已自动模糊化为「极高/较高/中等/较低/很低」
- ❌ 禁止 Agent 自行重排、改写、补充 tool 返回外的字段、或把 `data` 里的原始 JSON 贴出来

**第四步：追加「建议卡片」（铁律 D）**

```markdown
---

💡 **你还可以继续问：**

- 💬 给我一段跟进话术 — 立刻可发
- 📇 查看完整档案 — 多店询盘 + 决策依据

---
```

---

### 场景五：客户跟进话术建议

> 触发例：「客户张三怎么跟进」、「给我一段挽回李四的话术」、「怎么唤醒王五」、「张三是个流失风险买家，给下话术建议」。

**第一步：提取买家昵称和识别买家类型**
- 从 prompt 中识别昵称（如"分析一下张三" → nickName=张三）
- 同时识别买家类型关键词，决定传参：

  | 用户表述 | 传参 |
  |---------|------|
  | 流失风险买家、有流失风险、可能流失、即将流失 | `--buyer-type lostRiskType` |
  | 商机买家、高价值买家、重点商机、可唤醒 | `--buyer-type wakeUpType` |
  | 未明确提及买家类型 | 不传 `--buyer-type` |

**第二步：执行命令**
```bash
# 未识别到买家类型
python3 {baseDir}/cli.py suggest_follow_up_script --nick-name 张三

# 识别为流失风险买家
python3 {baseDir}/cli.py suggest_follow_up_script --nick-name 张三 --buyer-type lostRiskType

# 识别为商机买家
python3 {baseDir}/cli.py suggest_follow_up_script --nick-name 张三 --buyer-type wakeUpType
```

**第三步：原样输出 markdown**
- cmd.py 已按以下规则选中**一组**话术，并最多取 3 套"方案 1 / 2 / 3"轮播展示：
  - **未传 buyer-type**：wakenAdvice > retentionAdvice > followUpScript
  - **传 lostRiskType**：retentionAdvice（挽留话术）> followUpScript
  - **传 wakeUpType**：wakenAdvice（唤醒话术）> followUpScript
- Agent **禁止**再去拼接另一组话术、**禁止**把话术翻回 JSON

**第四步：追加「建议卡片」（铁律 D）**

```markdown
---

💡 **你还可以继续问：**

- 🔍 看下采购意图分析 — 理解话术背后的逻辑
- 📇 查看完整档案 — 全面了解客户

---
```

---

### 场景六：客户详细资料档案

> 触发例：「客户张三的详细资料」、「查看李四的档案」、「王五更多详情」。

**第一步：提取买家昵称**（同场景四第一步）

**第二步：执行命令**
```bash
python3 {baseDir}/cli.py get_customer_profile --nick-name 张三
```

**第三步：原样输出 markdown**
- 四个颜色区块：👤 客户基础信息（蓝）、🛒 客户采购习惯（绿）、🟨 采购决策依据（黄）、🏪 跨店询盘信息（紫）
- 每块前已带串场话语，风险分数已模糊化

**第四步：追加「建议卡片」（铁律 D）**

```markdown
---

💡 **你还可以继续问：**

- 🔍 分析采购意图 — 看ta为什么没成交
- 💬 给我跟进话术 — 立刻可发

---
```

---

## 跳转与引导规范（汇总）

| 当前完成的场景 | 必须执行 | 形式 | 引导内容 |
|--------------|---------|------|---------|
| 场景一 / 二 / 三（客户列表） | 铁律 C | `AskUserQuestion`（与 1688-shop-operate 一致） | 🔍 分析意图 / 💬 跟进话术 / 📇 更多客户资料 / 结束 |
| 场景四（采购意图分析） | 铁律 D | markdown 建议卡片 | 💬 跟进话术 / 📇 完整档案 |
| 场景五（话术建议） | 铁律 D | markdown 建议卡片 | 🔍 采购意图 / 📇 完整档案 |
| 场景六（详细档案） | 铁律 D | markdown 建议卡片 | 🔍 采购意图 / 💬 跟进话术 |

> **核心原则：所有引导建议严格落在本 skill 4 个 capability 之内，禁止越界；场景一/二/三用 `AskUserQuestion`（与 1688-shop-operate 对齐），场景四/五/六用 markdown 建议卡片（对话不终止，跨平台可渲染）。**

## 📖 字段中英对照知识库（强制查阅）

> 本表与 `scripts/_i18n.py` 中的 `FIELD_NAME_ALIAS` **一一对应**，cmd.py 调用 `tr()` 已自动转换。
> 但如果 tool 返回的 markdown 偶发还出现英文 key（如接口新增字段未覆盖），**Agent 必须先查本表**做人工翻译，查不到再按「下划线拆词 + 常见词汇」模糊翻译兜底，**绝不**原样透出英文。

### 🔑 客户采购习惯（`buyerPurchaseHabits` 子字段）

| 英文 key | 中文译名 |
|---------|---------|
| `pay_distribution` | 采购分布特征 |
| `supply_chain_stability` | 供应链选择稳定性 |
| `supply_cnt` | 供应链上游数目 |
| `supply_change_cycle` | 供应链新增状况 |
| `supply_change_cnt` | 供应链新增数量 |
| `inq_shop_cnt_30d` | 近90天询盘店铺 |
| `inq_cates_30d` | 近90天询盘品类 |
| `inq_items_30d` | 近90天询盘商品 |
| `search_keyword_30d` | 近90天搜索词 |
| `inq_shop_cnt_90d` | 近90天询盘店铺 |
| `inq_cates_90d` | 近90天询盘品类 |
| `inq_items_90d` | 近90天询盘商品 |
| `search_keyword_90d` | 近90天搜索词 |

### 🔑 近期沟通需求（`recentChatNeedsAna` 子字段）

| 英文 key | 中文译名 |
|---------|---------|
| `demands` | 需求清单 |
| `summary` | 摘要 |
| `demand_gmv` | 预算/GMV |
| `demand_scale` | 需求规模 |
| `wuliu_requirement` | 物流要求 |
| `dingzhi_requirement` | 定制要求 |

### 🔑 采购决策依据（`purchaseDecisions` 子字段）

| 英文 key | 中文译名 |
|---------|---------|
| `decision_points` | 决策点 |
| `title` | 关注点 |
| `summary` | 摘要 |
| `next_step` | 建议动作 |
| `importance` | 重要性 |

### 🔑 流失 / 商机（`lostAnalysis` / `awakenReason` 子字段）

| 英文 key | 中文译名 |
|---------|---------|
| `lostReason` / `lost_reason` | 流失原因 |
| `lostRiskType` | 流失类型 |
| `lostScore` | 流失风险程度（已按 A5 模糊化） |
| `awakenType` | 唤醒类型 |
| `awaken_reason` | 唤醒切入点 |

### 🔑 客户画像 / 卡片字段

| 英文 key | 中文译名 |
|---------|---------|
| `buyerId` | 客户 ID（**下游能力批量调用凭证**，类型为字符串，可能为加密格式，从列表接口返回中原样收集为 `buyerIdList` 字符串数组） |
| `nickName` | 买家昵称 |
| `buyerType` | 客户类型 |
| `followUpState` | 跟进阶段 |
| `lLevel` | 客户等级 |
| `buyerConstitution` | 客户体质 |
| `mainCate` | 主采类目 |
| `payCnt180d` | 近半年采购次数 |
| `payAmt180d` | 近半年同类目采购额 |
| `buyerPurchaseHabits` | 客户采购习惯 |
| `otherShopInqInfor` | 跨店询盘信息 |
| `purchaseDecisions` | 采购决策依据 |
| `recentChatNeedsAna` | 近期沟通需求分析 |
| `lostAnalysis` | 流失风险分析 |
| `awakenReason` | 商机唤醒理由 |
| `wakenAdvice` | 唤醒话术建议 |
| `retentionAdvice` | 挽留话术建议 |
| `followUpScript` | 跟进话术建议 |

### 🔑 跨店询盘 / 常规字段

| 英文 key | 中文译名 |
|---------|---------|
| `shopName` / `shop_name` | 店铺名称 |
| `inqCnt` / `inq_cnt` | 询盘次数 |
| `lastInqTime` / `last_inq_time` | 最近询盘时间 |
| `cate` / `cates` | 类目 |
| `item` / `items` | 商品 |
| `keyword` / `keywords` | 关键词 |

### 📦 话术字段（`speech_script` / 各话术套）

| 中文 key | emoji | 说明 |
|---------|-------|------|
| `开场白` | 👋 | 开启对话的问候语 |
| `核心话术` | 💡 | 面对需求的主体推荐 |
| `促单话术` | 🎯 | 促进下单的推动语 |
| `场景` | 📌 | 当前话术适用场景 |
| `挽留话术` | 🛡️ | 挽留场景专用 |
| `唤醒话术` | 🔥 | 唤醒商机场景专用 |

### 🔧 查不到时的模糊翻译規则（兜底）

当 tool 返回的 markdown 包含本表未覆盖的英文 key 时，Agent 按以下顺序做转换：

1. **下划线拆词**：`some_key_30d` → `some` + `key` + `30d`
2. **逐词查字典**（常见片段译名）：
   - `pay`采购 / `supply`供应链 / `inq`询盘 / `shop`店铺 / `cate`类目 / `item`商品
   - `search`搜索 / `keyword`关键词 / `name`名称 / `type`类型 / `level`等级
   - `count`/`cnt`/`num`数量 / `amt`/`amount`金额 / `time`时间 / `date`日期
   - `stability`稳定性 / `cycle`周期 / `change`变更 / `distribution`分布
   - `30d`近30天 / `60d`近60天 / `90d`近90天 / `180d`近半年 / `365d`近一年
3. **拼接**：逐词译名拼接（中文之间不加空格）。例：`inq_shop_cnt_60d` → 询盘 + 店铺 + 数量 + 近60天 = `近60天询盘店铺数量`。
4. **如果逐词也查不到**：保留原英文加上 `（未译）` 后缀提醒后续补充词典，如 `xxx_yyy_zzz（未译）`。

## 安全声明

| 风险级别 | 命令 | Agent 行为 |
|---------|------|-----------|
| **读取** | find_total_inquiry_customers | 用户触发查询意图时直接执行 |
| **读取** | analyze_customer_intent | 用户触发分析意图时直接执行 |
| **读取** | suggest_follow_up_script | 用户触发话术建议意图时直接执行 |
| **读取** | get_customer_profile | 用户触发详情查询意图时直接执行 |

## 环境变量（.env）

项目根目录的 `.env` 文件存储 skill 基础信息，供埋点上报等模块读取。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_NAME` | `1688-shop-zkt-buyer-manage` | skill 名称 |
| `SKILL_VERSION` | `1.0.0` | skill 版本号 |
| `SKILL_CHANNEL` | `clawhub` | 发布渠道 |

> 已存在的系统环境变量优先级高于 `.env`。

## 埋点上报

每次 CLI 命令执行时，自动向 skill 网关上报一次调用记录。

- **实现位置**：`scripts/_tracker.py` → `report_skill_usage()`
- **上报接口**：`POST /api/reportSkillsUsage/1.0.0`
- **失败处理**：上报失败静默忽略，不影响主流程

## 执行前置（首次命中能力时必须）

- 首次执行 `configure` 前：先完整阅读 `references/capabilities/configure.md`
- 首次执行 `find_total_inquiry_customers` 前：先完整阅读 `references/capabilities/find_total_inquiry_customers.md`
- 首次执行 `analyze_customer_intent` 前：先完整阅读 `references/capabilities/analyze_customer_intent.md`
- 首次执行 `suggest_follow_up_script` 前：先完整阅读 `references/capabilities/suggest_follow_up_script.md`
- 首次执行 `get_customer_profile` 前：先完整阅读 `references/capabilities/get_customer_profile.md`
- 同一会话内后续重复调用可复用已加载知识；仅在规则冲突或文档更新时重读。

## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词 | Agent 额外动作 |
|----------------|--------------|
| "AK 未配置" 或 "签名无效" 或 "401" | 提示用户当前能力所需鉴权未就绪，请补充有效 AK 或检查鉴权配置后重试 |
| "限流" 或 "429" | 建议用户等待 1-2 分钟后重试 |
| 其他 | 仅输出 markdown 即可 |
