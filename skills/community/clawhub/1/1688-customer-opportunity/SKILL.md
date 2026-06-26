---
name: 1688-customer-opportunity
version: 0.1.0
description: |
  1688 买家跟进与客群运营。可以帮你做：
  ① 查看AI客群列表 — 店铺有哪些高价值老客客群、各客群特征和买家数
  ② 展开客群买家明细 — 选一个客群，看具体有哪些买家
  ③ 开启客群运营计划 — 对选定客群自动发送旺旺营销文案
  ④ 查买家成交机会 — 输入买家账号，获取画像和跟进建议
  ⑤ 客户机会监控 — 智能找出近期最值得主动联系的买家
metadata:
  interactions:
    - name: select_buyers_from_cluster
      type: table
      selectionType: merchant
      description: "展开客群买家明细后，从买家列表中选择要进一步操作的买家，并通过自定义 Actions 选择下一步动作"
      required_data:
        rows: "买家列表，每项含 buyer_login_id、画像（agent 构造，格式 '画像：xxx\\n建议：xxx'，画像/建议各 ≤50 字）两列"
        actions: "按planId区分按钮：有planId用查看客群运营计划（view_plan，primary），无planId用换一批（next_batch，primary）；详见 interaction-specs.md"
    - name: confirm_marketing_plan
      type: input
      selectionType: 确认客群运营计划
      description: "确认/编辑客群旺旺文案，商家可选择 get_cluster_marketing_plan 返回的推荐文案或自行输入"
      required_data:
        questions: "一题数组：旺旺文案=[get_cluster_marketing_plan.sale_desc原文, 固定通用兜底文案]"
---

# 1688 客户机会挖掘 Skill

## 🚨 铁律（最高优先级，违反即视为流程错误）

### 0. CLI 入口路径（最先执行，路径写错直接报错）

CLI 入口文件：`{baseDir}/cli.py`（`{baseDir}` = skill 根目录，含 `SKILL.md` 和 `cli.py`）。**禁止** `{baseDir}/scripts/cli.py`——`cli.py` 不在 `scripts/` 子目录。

### A. tool 输出原样输出
所有 tool 输出 JSON `{"success", "markdown", "data"}`，**必须完整、逐字、原样输出 `markdown` 字段**（含 `>` 引用块前缀、HTML 注释、空行、表格分隔符）。**禁止** 精简 / 改写 / 提炼 / 合并 blockquote / 加开场白 / 从 `data` 重构内容。Agent 的分析或追问必须放在 markdown **之后**。

**唯一例外：客户机会监控场景**（命中触发词"最近哪些客户重要/需要主动联系的客户/待跟进客群买家"等）
- 调 `list_customer_cluster` 时**只取 data 用**，**禁止输出 markdown**（agent 要自动取 data.list[0].plan_id 进下一步，不展示客群表格给用户）
- 调 `list_cluster_buyer_detail` 时**只取 data 用**，**禁止输出 markdown**（仅取买家 loginId 列表喂 customer_reception_advice）
- 命中 "AI客群/查看客群/客群列表" 等查看客群触发词时**不适用**此例外，仍原样输出客群表格

### A2. 全程中文输出（强制）
**Agent 所有面向用户的输出（含思考过程、执行步骤说明、分析、追问、tool 调用前后的描述）必须 100% 用中文**。**禁止**任何形式的英文表述：
- ❌ 禁止 "Now I have..."、"Let me..."、"Per the skill's..."、"trigger scenario"、"flow" 等英文短语
- ❌ 禁止中英混排（如 "执行 list_customer_cluster trigger" 应为 "执行 list_customer_cluster 触发"）
- ✅ 技术标识符（tool 名、字段名如 `plan_id`/`buyer_login_id`、JSON key）保留原英文，但说明文字用中文
- ✅ 思考链 / 执行步骤折叠区里的内容也必须中文（包括"查看技术细节"折叠块内的描述）

### A3. 三段式交付强制（所有客户机会场景的最终回答）

show_interaction 完成 action 之后，或降级输出客户名单时，最终回答**必须三段**：

1. 【名单】每位 `buyer_login_id` + 身份标签（来自 `credit_level` / `if_ka` / `procurement_mode`）
2. 【画像】每人的 `lst_inq_time` / `ord_cnt_1m_level` / `gmv_1m_level` / `inq_relation`
3. 【建议】每人差异化跟进话术（来自 `customer_reception_advice.sale_desc`，**禁止模板化复制**）

**🚨 强约束（违反即流程错误）：**
- ❌ 禁止只输出"已发送"、"已执行"、"已完成"等短回复
- ❌ 禁止省略其中任意一段
- ❌ 禁止用列表/段落"概要"代替结构化交付（必须明确出现"名单/画像/建议"或等价的分段标题）

> 📌 **展示时按下方铁律 A4 字段映射表翻译**：本段列出的 `credit_level` / `if_ka` / `lst_inq_time` 等字段名仅供 agent 取值，**严禁直接出现在商家可见输出里**，必须翻译成「信用等级」「KA 标签」「最近询盘时间」等商家术语。

### A4. 商家友好语言（最高优先级，违反即流程错误）

商家不是开发者，agent 面向商家的所有可见文字（含"正在思考中"流式区块、执行步骤说明、过渡话术、追问、错误反馈）**禁止暴露任何技术内部信息**。

**🚨 思考过程静默原则（最强子约束）：**

1. **tool 调用前后零文字**：调 tool 前不写"我要调 XXX"，调完后不写"刚刚调了 XXX"。端侧自带「📄 读取文件」「🔄 执行命令」状态卡片，agent **禁止再用文字复述同一动作**。
2. **同一句话一个 turn 内只说一次**：如「商家已确认旺旺文案」「正在为你查询客群」——多步流程里**只在第一步说**，后续静默；连续两个流式区块说同一句即违规。
3. **禁止流程拼盘**：交付前不复盘"客群列表→买家明细→画像建议→展示交互→…"这种链路串烧——商家只想看结果，不想看你的工作流。
4. **禁止铁律元注释**：不说"现在按铁律 A3 三段式交付"「按 SKILL.md 第 X 步」「触发 XX 场景立即执行」等——做就行，别解释为什么做。
5. **结果交付不加过渡话术**：直接给三段式（名单/画像/建议），**禁止**"下面为你汇总…"「以下是…」「为你梳理…」等开场白。

**❌ 禁言清单（出现即违规）：**

| 类别 | 反例 |
|------|------|
| tool/函数名 | `list_customer_cluster`、`list_cluster_buyer_detail`、`customer_reception_advice`、`list_customer_details`、`get_cluster_marketing_plan`、`activate_cluster_plan`、`show_interaction`、`AskUserQuestion`、`customer-ww-send`、`customer-sms-info` |
| JSON 字段/路径 | `data.list[0]`、`plan_id`、`buyer_login_id`、`credit_level`、`if_ka`、`lst_inq_time`、`ord_cnt_1m_level`、`gmv_1m_level`、`crowd_type`、`cluster_name`、`buyer_num` 等 |
| 参数/CLI 标志 | `--plan-id`、`--buyer-login-ids`、`--fetch-all`、`--crowd-type`、`--date-type`、`--gmv-1m-level` 等 |
| 英文短语 | "Now I have..."、"Let me..."、"Call X to get..."、"Per the skill..."、"trigger / flow / scenario" |
| 流程元注释 | 「我现在要…」「按 SKILL.md 第 X 步…」「触发 XX 场景，立即执行…」「按 M1/M2/M3/M4/M5 执行…」「公共流程 M…」「子场景 X…」「现在按铁律 A3 三段式交付…」 |
| 内部动作描述 | 「立即读取 activate_cluster_plan 文档」「读取 references/xxx.md」「执行开启计划」「调用 XX 接口」「商家已确认旺旺文案，立即…」「现在已 XXX，立即 XXX」——**读文档 / 调接口 / 内部跳转**都是 agent 自己的事 |
| 步骤链路拼盘 | 「所有步骤已完成：客群列表→买家明细→画像建议→展示交互→查看运营方案→确认文案→开启计划」「按以下顺序执行：①…②…③…」 |
| 交付过渡话术 | 「下面为你汇总…」「以下是本次客群的…」「为你梳理…」「下面是结果」——三段式直接开始，不要开场白 |

**📖 字段翻译表 + 话术模板见 `references/lang-rules.md`**（首次面向商家输出前必读）。

**优先级：** 与 A、A2、A3 同级，**高于流程描述里的所有 tool 名引用**——SKILL.md 写「调 list_customer_cluster」是给 agent 看的指令，agent 面向商家只能说「正在查询客群」。

### B. 严禁自由发挥
1. ❌ 主动调 `get_cluster_marketing_plan`（仅在商家点 `view_cluster_plan` 按钮时才调）
2. ❌ 给所有客群拉买家明细（客户机会监控**只拉第一个客群**）
3. ❌ 生成长篇分析（综合策略 / 优先级排序 / 差异化话术 / 客群对比 / 附加建议等）—— 展示内容**必须**直接来自 tool markdown 或 show_interaction
4. ❌ 向 show_interaction rows 添加 spec 未定义的字段（如「所属客群」「等级」「跟进建议」）
5. ❌ 在 show_interaction 之前用 Markdown 表格/列表"预览"买家信息

### C. show_interaction 强制使用
| 场景 | 必须用 |
|------|--------|
| 展示 **≥2 个**买家供商家选择 | `show_interaction(name='select_buyers_from_cluster')` |
| 让商家确认/编辑客群运营方案 | `show_interaction(name='confirm_marketing_plan')` |

**单买家场景**（买家数 = 1）：**跳过 show_interaction，直接按铁律 A3 三段式输出该买家的名单/画像/建议**；有 planId 时再用 AskUserQuestion 弹「查看客群运营计划 / 换一批 / 结束」，无 planId 时弹「换一批 / 结束」，选后直接执行，不再追问。

**唯一例外**：买家数 = 0（无任何匹配买家）时告知"暂无数据"。

**🚨 强约束（违反即流程错误）：**
- ❌ 禁止用 Markdown 表格 / 列表 / `1. xxx` 段落 / 文字描述替代 show_interaction（≥2 买家场景）
- ❌ 禁止说"需要我帮你..."、"以下是建议行动..."等开放式追问替代 AskUserQuestion
- ❌ 禁止在 show_interaction / AskUserQuestion 之前用 Markdown "汇总分析"或"高价值机会识别"长篇内容（铁律 B 已禁，再次强调）

### D. show_interaction 完成后处理

**step 1：按 `data.action.key` 执行对应操作（或跳过）：**

| action.key | 执行动作 | 执行后 |
|------------|---------|--------|
| `view_plan`（查看客群运营计划，**有 planId 时**） | 进开启客群方案分支：`get_cluster_marketing_plan` → `confirm_marketing_plan` input → `activate_cluster_plan` | 进入 step 2 |
| `next_batch`（换一批，**无 planId 时**） | 直接重新拉列表，重复 show_interaction（**不进入 step 2**——本身即换一批） | — |
| `skip`（跳过） | 不执行任何操作 | 进入 step 2 |

**step 2：action 执行完毕（或跳过）后，弹 AskUserQuestion：**

```python
AskUserQuestion(
  question="接下来怎么做？",
  options=[
    {"label": "换一批"},
    {"label": "继续跟进这批"},
    {"label": "结束"}
  ]
)
```

- 「换一批」→ 按当前场景重新拉下一组买家，重复 show_interaction
- 「继续跟进这批」→ 用同一份 rows/columns/actions 重新调用 `show_interaction(name='select_buyers_from_cluster')`，不重新拉接口
- 「结束」→ 告知商家跟进任务已完成，不再继续

### F. 客户机会监控极简流程
```
list_customer_cluster → 仅取 data.list[0].plan_id
  → list_cluster_buyer_detail
  → customer_reception_advice（批量）
  → agent 排序所有买家
  → show_interaction(2列rows，传 actions=[查看客群运营计划（有planId）或换一批（无planId）])
  → 按铁律 D 执行 action → 执行完后弹「换一批」/「结束」
```
**禁止**在步骤之间插入 agent 自创内容。

**🚨 调用预算（防止 tool_calls 爆炸）：**

| 场景 | tool_calls 上限 |
|------|----------------|
| 客户机会监控（list_customer_cluster 路径） | **5 次** |
| 重点客户直查（4 类细分场景） | **3 次**（list_customer_details + customer_reception_advice + 可选发送动作） |

**违反时处理：**
- 超过上限 → 立即停止追加调用，**直接 show_interaction 或返回当前已有信息**
- ❌ 禁止反复重试 list_customer_cluster / list_cluster_buyer_detail 拿不同客群
- ❌ 禁止逐个买家循环调 customer_reception_advice（必须批量一次性）
- ❌ 禁止"探索式"试探不同 crowd_type 拼凑名单
- 商家选择「换一批」是**新一次查询**，预算重置

### G. 客户机会输出前置红线 🚨（最高优先级）

任何涉及【客户名单 / 客户画像 / 客户分层 / 客户标签 / 买家账号 / loginId】的输出，
**必须先调用本 skill 的 tool 拿到真实 data**，严禁凭 LLM 自身知识编造。

**判定标准：**
- 命中"客户机会监控"或"重点客户直查"任一触发词 → **必须**先调 tool
- final-answer 中出现具体 `buyer_login_id` / 客户画像描述 → **必须**有对应 tool 返回的 data 作支撑

**❌ 红线反例（评测中触发 0 分）：**
- 商家问"哪些客户值得跟进"→ 直接列 5 个虚假 loginId + 编造画像（红线 COM-REDLINE-R1）
- tool 调用失败/超时 → 不能用记忆/通识回答替代真实数据

**✅ 正确做法：**
- 必须先走 list_customer_cluster 或 list_customer_details 任一分支
- tool 返回空 list → **明确告知"暂无数据，请稍后再试"**，禁止编造
- tool 调用失败 → **明确告知"数据查询失败，请重试"**，禁止"模拟"返回值

**优先级：** 本铁律是 0 分红线，**优先级高于其他所有铁律和触发词路由规则**。

## 何时调用哪个 tool

| 用户场景                              | 推荐 tool                                                 | 数据源 / 时效                            |
| --------------------------------- | ------------------------------------------------------- | ----------------------------------- |
| 「这个买家怎么跟进」/ 商家正在旺旺接待中 / 实时聊天场景    | `customer_reception_advice`（线上）                         | 旺旺聊天 + TPP 实时推理                     |
| 「AI 客群」/ 「CRM 客群」/ 「查看我的客群」       | `list_customer_cluster`                                 | Lindorm ai_crm_crowd_plan           |
| 「客群运营方案」/ 「这个客群怎么触达」/ 「优惠券/文案是什么」 | `get_cluster_marketing_plan`                            | brave-troops HSF（DMS 营销方案表）         |
| 「这个客群有哪些买家」/ 「查看XX客群的买家」 | **先** `list_customer_cluster` 获取 planId，**再** `list_cluster_buyer_detail --plan-id` | brave-troops HSF |
| 「这个买家是什么客群」/ 「查一下这批买家的客群信息」/ 提供买家 loginId 列表 | `list_customer_details --buyer-login-ids` | CustomerManageDataBoardV2（订单+询盘双维度）|
| 模糊场景                              | 优先 `customer_reception_advice`（数据时效性更好）                 | —                                   |

## 触发词

**命中 customer_reception_advice：**
实时跟进、聊天接待、当前对话、买家咨询中、即时建议、这个客户怎么办、聊天给点建议、画一下买家、接待中的买家

**命中 list_customer_cluster：**
AI客群、CRM客群、客群列表、查看客群、我的客群、智能客群、哪些客群、客群有哪些、看下客群

**命中 get_cluster_marketing_plan：**
客群运营方案、这个客群怎么做、触达方案、优惠券是什么、文案是什么、海报、planId 对应的方案

**命中 list_cluster_buyer_detail（必须先有 planId，先调 list_customer_cluster）：**
客群买家明细、这个客群有哪些买家、买家等级、加入客群时间、查看XX客群的买家

**命中"查所有客群买家汇总"场景：**
查询所有客群的所有客户明细、查所有客群的买家、全量客群买家、所有AI客群有哪些买家、查询客群所有客户明细

**命中 list_customer_details（买家客群查询）：**
这个买家是什么客群、查一下这批买家的客群信息、买家客群、用户所在客群、这些 loginId 的客群、指定买家查客群

**命中"客户机会监控"场景：**
最近哪些客户重要、需要主动联系的客户、重要客户跟进、哪些客户需要联系、帮我看看重要客户、待跟进客群买家、N个待跟进客群买家、分析店铺待跟进客户、分析店铺X个待跟进客户、什么客户适合联系、什么客户适合发旺旺、什么客户适合发短信、哪些客户适合发旺旺、哪些客户适合发短信、适合联系的客户、适合发旺旺的客户、适合发短信的客户、客户触达建议、客户联络建议

**命中"重点客户直查"场景（按客群类型直接拉取，跳过 list_customer_cluster）：**

| 细分场景 | 触发词示例 | 对应 crowd_type |
|---------|----------|----------------|
| 流失客户预警 | 流失客户、流失买家、客户流失预警、流失老客、流失客户预警、流失客户挽回 | `流失买家` |
| 复购客户提醒 | 复购客户、复购提醒、周期采购、需要复购、复购买家、复购挖掘 | `周期采购` |
| 老客促活发现 | 老客促活、需要促活、老客户激活、激活老客、促活买家、沉默老客 | `老客促活` |
| 询盘未成交 | 询盘未成交、询盘没成交、有询盘没下单、询盘未转化、询盘客户 | `询盘未成交` |

**显式不命中（避免误导）：**
客户运营、客户分析、客户管理、CRM、客户洞察、客户分层、复购预测、交叉销售、升级销售、流失预警
批量画像、导入名单、Excel买家（→ 用 1688-buyer-batch-profile）

**能力边界（命中以下场景必须声明边界 + 推荐替代路径，严禁伪造数据）：**

| 用户问到 | 应答模板 |
|---------|---------|
| 业务员跟进进度、任务完成率、谁负责跟进 | "客户机会监控不维护业务员跟进任务状态，建议到 1688 后台『任务管理』页面查看，或使用对应任务管理类 skill" |
| 客服响应时长、接待质量、消息回复率 | "客服接待质量数据由 `1688-inquiry-quality`（客服质检）skill 提供，建议切换该 skill 查询" |
| 已标记风险客户、客户风险等级 | "客户机会监控未维护风险标记状态，可降级用『流失客户画像』分析：调用 `list_customer_details --crowd-type 流失买家 --fetch-all` 查看高流失风险客户" |
| 联系人变更、修改买家手机号、改买家姓名 | "联系人/手机号变更不在客户机会监控能力范围，请到 1688 后台 CRM 客户管理页面操作" |
| 店铺整体经营数据、GMV 趋势、流量来源 | "店铺整体经营分析由 `1688-shop-operate` skill 提供，建议切换该 skill 查询" |

**🚨 强约束（违反即流程错误）：**
- ❌ 禁止伪造业务员跟进数据（如"今日跟进 5 个客户"、"跟进率 80%"）
- ❌ 禁止伪造客服接待数据（如"今日响应时长 12 秒"、"5 单已回复"）
- ❌ 禁止伪造风险标记（如"3 个客户已标记高风险"）
- ❌ 禁止伪造联系方式变更状态（如"已为 X 修改手机号"）
- ✅ 命中以上场景时，**必须**先用应答模板声明边界，再视情况给出"基于客户机会维度的相关分析"（如流失客户画像）作为补充

**❗ 命中"重点客户直查"4 类细分触发词时禁止走 list_customer_cluster 流程：**
- 流失客户/复购客户/老客促活/询盘未成交 → 必须走 `list_customer_details --crowd-type {对应 crowd_type} --date-type RECENT_30 --fetch-all`
- ❌ 禁止先调 list_customer_cluster
- ❌ 禁止追加 view_plan action（无 planId 场景）
- **混合语义优先级**：当 prompt 同时包含 4 类细分词（如「流失客户」）和触达词（如「适合发短信」）时，**细分词优先**，走「重点客户直查」分支

## 命令速查

CLI 入口文件：`{baseDir}/cli.py`


| 命令 | 参数 | 说明 |
|------|------|------|
| `configure` | `YOUR_AK` | 配置 AK |
| `list_customer_cluster` | 无参数 | 查老客 AI 客群列表（含 planId / 客群特征） |
| `get_cluster_marketing_plan` | `--plan-id PLAN_ID` | 查客群运营方案（优惠券/文案/海报）|
| `list_cluster_buyer_detail` | `--plan-id PLAN_ID` | 查客群买家明细（触达状态）|
| `list_customer_details` | `--buyer-login-ids '["nick1","nick2"]'` | 查指定买家的客群信息（订单+询盘双维度）|
| `customer_reception_advice` | `--buyers '<对象数组 JSON>'` | 批量实时画像 + 跟进建议（统一对象数组入参；详见下方「customer_reception_advice 入参示例」）|
| `activate_cluster_plan` | `--plan-json '<JSON>'` | 开启 AI 客群运营计划 |

### customer_reception_advice 入参示例

`--buyers` 是对象数组 JSON，每个对象**通过字段名**声明类型——`login_id` 或 `phone` 二选一，Java 端自动识别并转 userId。一手机号可能对应多账号，会拆成多条结果。

```bash
# 场景 1：纯 loginId（最常见，从客群明细 / 客户列表拿到的都是 loginId）
python cli.py customer_reception_advice --buyers '[{"login_id":"alice"},{"login_id":"bob"}]'

# 场景 2：纯 phone（用户上传通讯录、外部名单只有手机号时）
python cli.py customer_reception_advice --buyers '[{"phone":"13800138000"},{"phone":"13900139000"}]'

# 场景 3：loginId + phone 混合（用户名单同时含两种身份信息）
python cli.py customer_reception_advice --buyers '[{"login_id":"alice"},{"phone":"13800138000"},{"login_id":"bob"}]'

# 场景 4：单买家（仍走数组）
python cli.py customer_reception_advice --buyers '[{"login_id":"nick"}]'
python cli.py customer_reception_advice --buyers '[{"phone":"13800138000"}]'
```

**禁止**：
- 传字符串数组 `["alice","bob"]`（旧格式，已废弃）
- 传对象但缺 `login_id` 和 `phone` 字段（会被收集到 `invalid_entries`，不阻断其他条目处理）
- 传同时含 `login_id` 和 `phone` 的对象（行为：优先 `login_id`，`phone` 被忽略；建议拆成两条）

## Agent 使用流程

**🚨 禁止向用户索取主账号 `user_id` / `login_id`**。调用方身份由后端通过 AK 自动解析。Agent 只需收集买家身份（login_id / phone）作为业务参数。

**线下批量场景（分析单个/多个客户的客群信息）：**
1. 用户提供本地文件（Excel/CSV 等）→ 大模型解析，提取买家 loginId 列表
2. **必须先**调 `list_customer_details --buyer-login-ids '["loginId1","loginId2"]'`，获取每个买家的客群归属
3. 根据返回结果映射每个买家的 crowd_type：
   - `order_list[].procurement_mode = "periodic"` → 周期采购
   - `order_list[].procurement_mode = "old_buyer"` → 老客促活
   - 该买家在 `inquiry_list` 中有数据 → 询盘未成交
   - 其他 → 流失买家
4. **禁止跳过步骤2直接调** `customer_crowd_analysis`——crowd_type 必须来自 list_customer_details 的返回，不可猜测
5. 按 crowd_type 分组，每组各调一次 `customer_crowd_analysis --buyers '[...]' -t {crowd_type}`（同一组内线程池并发）

**线上实时场景：**
1. 用户在旺旺接待 / 询问"这个买家怎么跟进" → 直接调 `customer_reception_advice`
2. 该 tool 内部自动拉聊天历史 + TPP 推理，无需用户提供其他参数

**通用：**
- 首次使用报 AK 错误 → 引导 `python cli.py configure YOUR_AK`

**老客机会挖掘场景（统一入口）：**

> 触发任一买家挖掘/客群相关触发词时，**禁止询问用户想做什么、立即执行**。

### 公共流程 M（子场景 2-7 全部套用）

> 🚨 **M1-M5 / 子场景 X / 公共流程 M 均为 SKILL.md 内部步骤编号**，仅供 agent 自己路由用，**严禁出现在面向商家的任何可见文字里**（含思考过程流式区块、过渡话术、追问、复盘），按铁律 A4 禁言清单"流程元注释"分类处理。


| Step | 动作 | 关键约束 |
|------|------|---------|
| M1 | 拉买家 loginId 列表（数据源见下方场景表） | — |
| M2 | 取所有 loginId 一次性批量调 `customer_reception_advice --buyers '[{"login_id":"..."},...]'` 拿画像 + 建议 | ❌ 禁止逐个循环、禁止询问选哪位 |
| M3 | agent 按成单机会从高到低排序：a. 近期聊天+采购意向 > b. 有询盘未成交 > c. 历史下单近期静默 > d. 无互动；同级保持 API 顺序 | — |
| M4 | 按 2 列 rows 构造（`buyer_login_id` + 「画像：xxx\n建议：xxx」各 ≤50 字），调 `show_interaction(name='select_buyers_from_cluster')`；**actions：有 planId → `[view_plan]`；无 planId → `[next_batch]`** | ❌ 严禁 Markdown 表格替代、严禁 `view_plan` 与 `next_batch` 同时出现、严禁展示 userId |
| M5 | 按铁律 D 处理 `action.key`，执行完弹 AskUserQuestion「换一批 / 继续跟进这批 / 结束」 | — |

**单买家**（loginId 数=1）：跳过 M4，按铁律 A3 三段式输出，弹 AskUserQuestion「换一批 / 结束」；有 planId 追加「查看客群运营计划」。
**空数据**：告知「暂无待跟进客户，可以尝试其他客群场景」。

### 子场景 1：查看 AI 客群列表（命中 "AI客群/查看客群/客群列表"）

1. 调 `list_customer_cluster`，**完整、逐字、原样**输出返回的 markdown（铁律 A，含 `>` 引用块前缀、空行、HTML 注释；禁加开场白、禁从 data 重构）
2. **markdown 渲染完成后**才能弹 AskUserQuestion 两题（**禁止在表格渲染前弹出**）：
   - 问题一「要操作哪个客群？」：选项格式 `"{cluster_name}（{buyer_num}人）"`，**禁用"第1个客群"序号文案**
   - 问题二「选择下一步操作」：「展开客群买家明细」/「查询运营方案」/「查看所有客群汇总买家明细」
3. 取答案匹配 `data.list[].plan_id`，进入对应子场景
- 若 prompt 同时命中 "所有客群买家/全量客群买家"：**跳过 AskUserQuestion，直接进入子场景 3**

### 场景分发表（M1 数据源 + 差异点）

| 子场景 | 触发条件 | M1 数据源 | planId | 差异点 |
|--------|---------|----------|--------|--------|
| 2. 展开客群明细 | 子场景 1 选「展开客群买家明细」 | `list_cluster_buyer_detail --plan-id PLAN_ID` → `data.list[].buyer_login_id` | ✅ | — |
| 3. 查所有客群汇总买家明细 | 子场景 1 选「查看所有客群汇总买家明细」**或** prompt 命中"所有客群买家/全量客群买家" | 对子场景 1 已有的全部 `plan_id` **并行**调 `list_cluster_buyer_detail`，按 loginId 合并去重 | ❌ | 禁止重新调 `list_customer_cluster`；告知"共 X 客群，去重后 Y 位" |
| 4. 客户机会监控-有 AI 客群 | "客户机会监控" 触发词 + `cluster_count > 0` | 调 `list_customer_cluster`（**只取 data，禁输 markdown**）→ 取 `data.list[0].plan_id` → `list_cluster_buyer_detail`（同禁输 markdown） | ✅ | M5「换一批」用 AskUserQuestion 列剩余客群（`data.list[1:]`，同问题一格式），选中后取对应 plan_id 重复 M1-M5 |
| 5. 客户机会监控-无 AI 客群（按优先级） | "客户机会监控" 触发词 + `cluster_count = 0` | 按优先级**逐级**执行（**禁止并行、禁止跨级跳转**）：① `list_customer_details --gmv-1m-level 高` ② `list_customer_details --ord-cnt-1m-level 高` ③ `list_customer_details --user-label-list '["B类买家"]'` | ❌ | M5「换一批」选项：当前级「下一批」+ 切下一级；③ 仅「下一批」无切换 |
| 6. 客户机会监控-无 AI 客群-所有客群汇总 | "客户机会监控" + "所有客群买家/全量客群买家" + `cluster_count = 0` | **并行** 3 条 `list_customer_details`（`--gmv-1m-level 高` / `--ord-cnt-1m-level 高` / `--user-label-list '["B类买家"]'`），按 loginId 合并去重 | ❌ | 告知"暂无 AI 客群数据，将为你从全部老客中筛选高价值买家" |
| 7. 重点客户直查 | 4 类细分触发词（流失/复购/老客促活/询盘未成交） | `list_customer_details --crowd-type {crowd_type} --date-type RECENT_30 --fetch-all`；`{crowd_type}` = `流失买家`/`周期采购`/`老客促活`/`询盘未成交` | ❌ | **禁止**调 `list_customer_cluster` / `list_cluster_buyer_detail`；**禁输** `list_customer_details` markdown；M5「换一批」重拉同一 crowd_type 全量 |

> ⚠️ `list_cluster_buyer_detail` 和 `get_cluster_marketing_plan` 都必须先有 planId。planId 只能来自 `list_customer_cluster` 的返回，**禁止猜测**。

### 开启客群方案分支（M5 选 `view_plan` 或子场景 1 选「查询运营方案」时进入）

1. 调 `get_cluster_marketing_plan --plan-id PLAN_ID` 拿方案详情（**忽略 offer_list**）
2. 调 `show_interaction(name='confirm_marketing_plan')` 让商家确认/修改旺旺文案（按 `references/interaction-specs.md` §2 构造 questions），**禁止用 AskUserQuestion 文字交互替代**
3. **🚨 input 完成强红线**：回传中 `selectionType="确认客群运营计划"` 且 `data.questions[0]` 含答案——**这是 input 已完成的唯一信号**，agent 必须**同一 turn 内静默**执行步骤 4（**读 activate_cluster_plan.md / 构造 JSON / 调 tool 全部是 agent 内部动作，禁止对商家用任何过渡话术**，如「商家已确认旺旺文案，立即读取 activate_cluster_plan 文档并执行开启计划」这类描述属于铁律 A4「内部动作描述」违规），**禁止**：
   - ❌ 重新调 `list_customer_cluster` 或重新展示 AI 客群列表
   - ❌ 再次弹 `confirm_marketing_plan` 或任何 AskUserQuestion 二次确认
   - ❌ 仅回复"已确认"等文字而不调 `activate_cluster_plan`
   - ❌ 把端侧"已确认需求·确认客群运营计划"渲染态当作"待用户继续操作"——那只是 input 完成的展示气泡，不是按钮
   - ❌ 把"已确认 / 立即执行 / 读取文档"等内部动作描述说出来（应直接调 tool）
4. 取 `data.questions[0]` 答案作 `saleDescription`，按 `references/capabilities/activate_cluster_plan.md` 构造 JSON（**不传 coupon 字段**），调 `activate_cluster_plan --plan-json '<JSON>'`
5. 成功后直接展示命令输出的 markdown（含 CRM 链接），**禁止调用 `open_tab`**，由用户自行点击链接

**展示规范见 `references/display-rules.md`**（agent 初始化时会读取）

## 执行前置（首次命中能力时必须）
- 首次触发 `show_interaction` 前：先完整阅读 `references/interaction-specs.md`
- 首次执行 `configure` 前：先完整阅读 `references/capabilities/configure.md`
- 首次执行 `list_customer_cluster` 前：先完整阅读 `references/capabilities/list_customer_cluster.md`
- 首次执行 `list_customer_details` 前：先完整阅读 `references/capabilities/list_customer_details.md`
- 首次执行 `list_cluster_buyer_detail` 前：先完整阅读 `references/capabilities/list_cluster_buyer_detail.md`
- 首次执行 `customer_reception_advice` 前：先完整阅读 `references/capabilities/customer_reception_advice.md`
- 首次执行 `customer_crowd_analysis` 前：先完整阅读 `references/capabilities/customer_crowd_analysis.md`
- 首次执行 `activate_cluster_plan` 前：先完整阅读 `references/capabilities/activate_cluster_plan.md`
- 首次执行 `get_cluster_marketing_plan` 前：先完整阅读 `references/capabilities/get_cluster_marketing_plan.md`
- 首次渲染输出前：先完整阅读 `references/display-rules.md`
