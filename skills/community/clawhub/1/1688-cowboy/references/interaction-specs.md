# 交互组件详细规范（interaction-specs）

本文档定义 1688-reception-assistant Skill 在 `metadata.interactions` 中声明的所有交互组件的**渲染数据结构**与**字段映射规则**。

主 Agent 在调用 `show_interaction(name=...)` 之前 **MUST** 先阅读对应章节，**严格按照本文规定的字段构造入参**，禁止凭印象拼装 JSON。

> 🚨 **调用节奏红线（重点，曾出事故）**：**每轮主 Agent 回复中，招聘 4 步剧情里最多只能调 1 次 `show_interaction`**。调完 Step N 后本轮立即结束，等到商家在前端点击该卡按钮回传后，下一轮才允许调 Step N+1；**严禁** 在同一轮回复里并行 / 串行批量推出多张招聘剧情卡，否则前端会多卡堆叠、商家无法逐步交互。

---

## 通用约定

| 项 | 约束 |
| --- | --- |
| 入参根字段 `type` | 标准 5 类 `card` / `table` / `input` / `open_tab` / `notice`；**端侧扩展** `rich_card`（富卡片）、`conversation_sim_card`（模拟对话卡） |
| 入参根字段 `selectionType` | 数据类型标识；本 Skill 使用业务语义命名（5 个值：`hire_intro` / `platform_auth` / `buyer_levels` / `sim_dialog` / `reception_management`），决定云端落库分类与回传结构 |
| `questions[]`（仅 `card` 使用） | 问题数组；`question` 支持 Markdown；`options` 候选项；`allowMultiple` 多选；`required` 必填 |
| `rich_card` 字段 | `title` / `submittedTitle`（可选：仅在需要“提交后换标题”的卡传，如 Step 1 面试前/后标题不同；其他卡不传） / `body` / `iconUrl` / `buttons[{key,label,submittedLabel,description,variant}]`；**无 `questions`**；**`iconUrl` 必填**（卡片标题左侧图标，缺失会导致 UI 标题前无 icon） |
| `conversation_sim_card` 字段 | `title` / `submittedTitle` / `iconUrl` / `simQuestions[]` / `defaultSelectedQuestion` / `buyerLabel` / `agentLabel` / `conversations[]` / `confirmButtonLabel`；**无 `questions`** |
| 回传结构 | `card`：`{ selectionType, data: { answers: [{ question, answer, skipped? }] } }`，多选 `answer` 为数组；`rich_card` / `conversation_sim_card`：前端把按钮 `submittedLabel`（或 `confirmButtonLabel`）作为用户消息回传，主 Agent 据文案推进 |

---

## 1. hire_step1_intro（rich_card 组件）

### 组件类型

`type: rich_card`（端侧扩展类型；端侧不识别时可回退到 `card` 渲染）

### 业务语义

招聘 4 步剧情流的 **Step 1 接待助手自我介绍卡**。商家点击「好的，开始面试」即进入 Step 2 站内授权。

**仅用于首次招聘剧情流，不调任何后端接口**（前端写死文案）。

### 数据槽位定义

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `title` | string | 固定 "你好老板，我是接待专员应聘者"（提交前 / 面试前标题） |
| `submittedTitle` | string | 固定 "你好老板，我是你的接待助手"（提交后 / 面试后标题；UI 据此区分面试前/后状态） |
| `iconUrl` | string | 固定 `https://gw.alicdn.com/imgextra/i2/O1CN01xHrmut1q0pMVzzNB7_!!6000000005434-2-tps-32-32.png` |
| `body` | string（Markdown） | 固定文案 "**能力介绍**\n\n我可以 7X24替你接待买家、跟进高意向、识别经营机会。\n试用期 30天免费。让我们先聊聊吧～"，不可改写 |
| `buttons` | Array<Button> | 长度固定 1，唯一按钮 key=`start`，label="好的，开始面试"，submittedLabel="进入面试流程"，variant=`primary` |

> ⚠️ `title` / `submittedTitle` / `iconUrl` / `body` / `buttons` **全部必填**，且必须与上表的字面文案 / CDN 链接完全一致，不可省略、不可替换。`submittedTitle` 是本卡特例（仅 Step 1 需要），用于区分面试前/后两种标题状态。

### 完整数据示例

```json
{
  "type": "rich_card",
  "selectionType": "hire_intro",
  "title": "你好老板，我是接待专员应聘者",
  "submittedTitle": "你好老板，我是你的接待助手",
  "iconUrl": "https://gw.alicdn.com/imgextra/i2/O1CN01xHrmut1q0pMVzzNB7_!!6000000005434-2-tps-32-32.png",
  "body": "**能力介绍**\n\n我可以 7X24替你接待买家、跟进高意向、识别经营机会。\n试用期 30天免费。让我们先聊聊吧～",
  "buttons": [
    { "key": "start", "label": "好的，开始面试", "submittedLabel": "进入面试流程", "description": "用户同意开始面试", "variant": "primary" }
  ]
}
```

### 回传

商家点击「好的，开始面试」后，前端把按钮的 `submittedLabel`（"进入面试流程"）作为用户消息回传，主 Agent 据此推进 Step 2。

---

## 2. hire_step2_platform_auth（rich_card 组件）

### 组件类型

`type: rich_card`

### 业务语义

招聘 4 步剧情流的 **Step 2 信息读取确认卡**。商家点击「确认」后进入站内授权页完成授权动作，主 Agent 推进至 Step 3。

**本步不调任何后端接口**（含 `cowboy_config` 任何子命令），授权动作由站内授权页自闭环。

### 数据槽位定义

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `title` | string | 固定 "信息读取确认" |
| `body` | string（Markdown） | 列出将读取的 4 项数据（询盘对话 / 站内知识库 / 商品库与详情页 / 历史订单），不可改写 |
| `iconUrl` | string | 固定 `https://gw.alicdn.com/imgextra/i3/O1CN0132cHKR1UMQUfVTUWV_!!6000000002503-2-tps-32-32.png` |
| `buttons` | Array<Button> | 长度固定 1：`confirm`（确认, variant=`primary`） |

> ⚠️ 本卡 **不需要** `submittedTitle`（点击「确认」后即跳走并推进 Step 3，无需展示提交后替换标题；仅 Step 1 需要该字段）。`iconUrl` 必填，且必须为上述 CDN 链接，不可省略或替换。

### 完整数据示例

```json
{
  "type": "rich_card",
  "selectionType": "platform_auth",
  "title": "信息读取确认",
  "body": "*将通过您店铺的以下信息进行了解*  \n近180天询盘对话  \n站内知识库  \n商品库与详情页  \n历史订单（用于售后场景）",
  "iconUrl": "https://gw.alicdn.com/imgextra/i3/O1CN0132cHKR1UMQUfVTUWV_!!6000000002503-2-tps-32-32.png",
  "buttons": [
    { "key": "confirm", "label": "确认", "description": "确认", "variant": "primary" }
  ]
}
```

### 回传

- 点击 `confirm` → 前端把 `label`（"确认"）作为用户消息回传 → 主 Agent 推进至 Step 3

### 异常分支

- 商家拒绝授权 / 关闭授权弹窗：主 Agent 提示「没站内数据我对你店里的事情就两眼一抹黑，请尽快授权」，**4 步流程不中断**，可继续走 Step 3，但后续接待时站内数据相关问题会答得不完整。

---

## 3. hire_step3_buyer_levels（card 组件）

### 组件类型

`type: card`（标准 5 类之一）

### 业务语义

招聘 4 步剧情流的 **Step 3 接待范围配置卡**。商家在 **1 张卡 1 个问题**「可接待买家等级」中完成配置：从 `L0~L6` 共 7 个等级中多选必填、勾选愿意由接待助手接待的买家等级（直接对应子账号 `allowBuyerLevelList` 字段 / `cowboy_config create --levels` 入参）。

商家答完点提交后，主 Agent 把该题答案直接映射为可接待 L 等级列表，**仅写入会话上下文暂存**（不调任何后端接口），并 **推进至 Step 4 `hire_step4_sim_dialog`**；`cowboy_config create` 严格绑定 Step 4 「确认模拟效果」后由 §4 后置动作触发。

### 数据槽位定义

根字段：

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `type` | string | 固定 `card` |
| `showSkipButton` | boolean | 固定 `false`（必答，无跳过） |
| `allowCustomOption` | boolean | 🔴 **必须显式传 `false`，禁止省略、禁止传 `true`**；L0~L6 七选项是与子账号 `allowBuyerLevelList` 字段强绑定的协议套选值，任何商家自填项都会破坏 `--levels` 推导、导致 `cowboy_config create` 失败；**省略该字段与传 `true` 效果相同——端侧默认开启自定义选项按钮，必须显式关闭** |
| `confirmedHeaderLabel` | string | 提交后头部标题，固定 "确认模拟效果" |
| `confirmedActionLabel` | string | 提交按钮文案，固定 "开始上岗！" |
| `questions` | Array<Question> | 长度固定 1，仅「可接待买家等级」一题，不可增删 |

`questions[]` 题目定义：

| # | question | options | allowMultiple | required |
| --- | --- | --- | --- | --- |
| 1 | "哪些买家让我接待" | `["L0买家","L1买家","L2买家","L3买家","L4买家","L5买家","L6买家"]` | `true` | `true` |

> 🚨 **高频漏填红线**：`allowCustomOption` **必须显式写 `false`**。Agent 曾多次漏传该字段，导致端侧默认开启「自定义选项」按钮，商家手填任意文字后 `--levels` 映射失败、`cowboy_config create` 返回错误。**每次拼装本卡 JSON 时，MUST 检查 `allowCustomOption: false` 是否在字段列表中**。

### 完整数据示例

```json
{
  "type": "card",
  "selectionType": "买家等级",
  "showSkipButton": false,
  "allowCustomOption": false,  // 🔴 必须显式传 false，禁止省略
  "confirmedHeaderLabel": "确认模拟效果",
  "confirmedActionLabel": "开始上岗！",
  "questions": [
    {
      "question": "哪些买家让我接待",
      "options": ["L0买家","L1买家","L2买家","L3买家","L4买家","L5买家","L6买家"],
      "allowMultiple": true,
      "required": true
    }
  ]
}
```

### 回传结构（多选 answer 为数组）

```json
{
  "selectionType": "买家等级",
  "data": {
    "answers": [
      { "question": "哪些买家让我接待",        "answer": ["L0买家","L1买家"] }
    ]
  }
}
```

### 后置动作

收到回传后，主 Agent **必须**按下列顺序执行：

1. 取 `answers[0].answer`（"哪些买家让我接待"，已是商家勾选的可接待买家等级集合）按下表逐项映射为 L 等级 → 拼成 `--levels` 入参：
   - "L0买家" → `L0`
   - "L1买家" → `L1`
   - "L2买家" → `L2`
   - "L3买家" → `L3`
   - "L4买家" → `L4`
   - "L5买家" → `L5`
   - "L6买家" → `L6`
   - 至少 1 项必选；若 `answer` 为空数组（端侧 `required: true` 已拦截），主 Agent 仍需兜底提示「至少勾 1 个买家等级」并要求重答
2. **将映射出的 L 等级列表写入会话上下文暂存**（建议 key：`hire.reception_levels`），**不调任何后端接口**；`cowboy_config create` 严禁在本步调起
3. **推进至 Step 4**：调用 `show_interaction(name='hire_step4_sim_dialog')` 渲染模拟对话卡（详见 §4）；接待助手**不在本步激活**，须等 §4 「确认模拟效果」后由主 Agent 调 `cowboy_config create` 成功后才正式设为 `status: active`

`cowboy_config create --levels` **严禁在 Step 1 / 2 / 3 触发**，严格绑定 Step 4 「确认模拟效果」后（详见 §4 后置动作）；调用时 **必须带 `--levels`**（不传会被 CLI 硬拒）。后续修改买家等级由管理页面走 `cowboy_config update --levels`，**主对话框不发起** update。

---

## 4. hire_step4_sim_dialog（conversation_sim_card 组件）

### 组件类型

`type: conversation_sim_card`（端侧扩展类型）

### 业务语义

招聘 4 步剧情流的 **Step 4 模拟对话效果确认卡**。在 Step 3 接待范围配置提交（L 等级已暂存）之后、接待助手正式上岗之前，先让商家**预览**接待助手对常见买家问题（发货时效 / 商品材质 / 现货库存 等）的拟答效果。商家点「确认模拟效果」后，主 Agent **此时才调** `cowboy_config create --levels {Step 3 暂存值}` 一步完成子账号创建 + 买家等级写入，成功即把 `status` 写为 `active`、接待助手正式上岗。

**Q 由前端预置 / A 由 testChat 实时生成**：`simQuestions[]` 是前端预置的固定问题列表（题目内容 + 顺序均不变）；`conversations[].answer` **不再随卡预生成一次性下发**，而是主 Agent 在 `show_interaction(name='hire_step4_sim_dialog')` 之前，按每个 `simQuestions[].label` 并行（或顺序）调用 `cli.py test_chat --query "{label}"`（接口 `api/cowboy_test_chat/1.0.0`），按 `actionType` 三类映射出最终 A：

- `actionType=answer` → A = 接待助手实际回答内容（`message` 字段原文）
- `actionType=human`  → A = `"转人工"`（兑底文案，不暴露 message）
- `actionType=ask`    → A = `"询问买家"`（兑底文案，不暴露 message）

「确认模拟效果」是 **`cowboy_config create` 唯一的起点**，所有接口调用 + 激活动作都在本步完成。

### 数据槽位定义

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `title` | string | 固定 "模拟对话" |
| `submittedTitle` | string | 固定 "确认模拟效果"（提交后标题） |
| `iconUrl` | string | 固定 icon（CDN 链接） |
| `simQuestions` | Array<{key,label}> | 模拟问题候选 2~6 个；商家点击切换查看不同问答 |
| `defaultSelectedQuestion` | string | 默认选中的 `simQuestions[].key`，决定卡片首屏展示哪段问答 |
| `buyerLabel` | string | 对话气泡左侧标识，固定 "买家" |
| `agentLabel` | string | 对话气泡右侧标识，固定 "接待员" |
| `conversations` | Array<{question,answer}> | 完整问答清单；与 `simQuestions` 的 label 一一对应（前端按当前选中项过滤展示）。**`question` 取自 `simQuestions[].label`（前端预置，固定不变）**；**`answer` 由主 Agent 在调 `show_interaction` 之前并行调 `test_chat` 拿到，按 `actionType` 三类映射后填入**（answer→message 原文 / human→"转人工" / ask→"询问买家"） |
| `confirmButtonLabel` | string | 主按钮文案，固定 "确认模拟效果" |

### 完整数据示例

```json
{
  "type": "conversation_sim_card",
  "selectionType": "sim_dialog",
  "title": "模拟对话",
  "submittedTitle": "确认模拟效果",
  "iconUrl": "https://gw.alicdn.com/imgextra/i4/O1CN014o8zCI1aoGFy2oaRS_!!6000000003376-2-tps-66-63.png",
  "simQuestions": [
    { "key": "ship_today", "label": "这个商品预计什么时候发货呢？" },
    { "key": "material", "label": "这个商品是什么材质？" },
    { "key": "in_stock", "label": "有现货吗？" }
  ],
  "defaultSelectedQuestion": "ship_today",
  "buyerLabel": "买家",
  "agentLabel": "接待员",
  "conversations": [
    { "question": "这个商品预计什么时候发货呢？", "answer": "现货 SKU 当日 15:00 前下单可当天顺丰发出；预售 / 定制款依货期安排，下单页面会标注货期。" },
    { "question": "这个商品是什么材质？", "answer": "主体面料 95% 棉 + 5% 弹力纤维，里料涤纶，亲肤透气；详情页规格栏可看完整成分。" },
    { "question": "有现货吗？", "answer": "标准 SKU 全部现货，库存实时同步详情页；告诉我型号 + 数量，我马上为您核库。" }
  ],
  "confirmButtonLabel": "确认模拟效果"
}
```

### 回传

商家点击「确认模拟效果」后，前端把 `confirmButtonLabel`（"确认模拟效果"）作为用户消息回传，主 Agent 据此**调用 `cowboy_config create --levels {Step 3 暂存值}`**（一步完成子账号创建 + 买家等级写入），成功后将接待助手**激活上岗**（status: `active`）并输出招聘完成话术（参考 SKILL.md §1.3）。

### 前置动作（show_interaction 调用之前）

主 Agent 在调 `show_interaction(name='hire_step4_sim_dialog')` 之前，**必须**按下列顺序执行：

1. 取 `simQuestions[].label` 列表（前端预置 2~6 个，固定不变）
2. 对每个 `label` 调用 `cli.py test_chat --query "{label}"`（可并行；接口 `api/cowboy_test_chat/1.0.0`），拿到 `data.replies[0]`
3. 按 `actionType` 三类映射出最终 A 文案：
   - `answer` → A = `replies[0].message` 原文
   - `human`  → A = `"转人工"`
   - `ask`    → A = `"询问买家"`
4. 拼装 `conversations[]`：每项 `{ question: simQuestions[i].label, answer: 上一步得到的 A }`
5. 把完整渲染数据下发给 `show_interaction`

如某个 `test_chat` 失败 / 超时，该条 `answer` 写 `"系统忙，稍后再试"`（不阻断整卡渲染）。

### 后置动作

收到「确认模拟效果」回传后，主 Agent **必须**按下列顺序执行：

1. 从会话上下文取 Step 3 暂存的 L 等级列表（key 例：`hire.reception_levels`）；若丢失则返回 Step 3 重新提交
2. **立即调用 `cowboy_config create --levels {Step 3 暂存值}`**（CLI：`python3 {baseDir}/cli.py cowboy_config create --levels L0,L1,L2`），**一步**完成子账号创建 + 买家等级写入；失败时按 SKILL.md §1.4 重试与降级策略处理
3. 接口成功 → 将接待助手状态标为 `active`（招聘完成、正式上岗）
4. 输出招聘完成话术（参考 SKILL.md §1.3）
5. 退出 4 步招聘剧情流，后续任何配置修改（改 L 等级 / 暂停 / 恢复）一律跳管理页面，主对话框不发起任何 `cowboy_config` 写入动作

本卡 `conversations[].answer` 由主 Agent 在前置动作中调 `test_chat` 实时生成；**`cowboy_config create` 由本步「确认模拟效果」触发**，严禁提前到 Step 1/2/3。

---

## 5. manage_reception（open_tab 组件）

### 组件类型

`type: open_tab`（标准 5 类之一）

### 业务语义

**招聘完成后所有配置修改与查看的统一入口**。商家在主对话里说出以下意图时，主 Agent 调 `show_interaction(name='manage_reception')` 立即打开端侧「接待管理」Tab（`componentKey='reception_management'`），由页面内部完成写入：

- 改 L 等级范围（增减接待哪些等级的买家）
- 切暂停 / 恢复接待
- 查看授权范围只读区（接待需求 / 接待时间 / 红线 — 平台定不可改）
- 查看接待质检状况

**fire-and-forget**：调用后立即返回（不等用户操作），不阻塞后续工具调用；聊天区同步出现一张「已为你打开接待管理」的只读气泡卡片。

### 数据槽位定义

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `type` | string | 固定 `open_tab` |
| `selectionType` | string | 固定 `reception_management` |
| `pageTitle` | string | 固定 `接待专员`（≤ 20 字符；超出会在 Tab 上被 `…` 截断） |
| `pageDescription` | string | 固定 `查看接待管理和质检状况`（≤ 80 字符；用于气泡卡片第二行） |
| `componentKey` | string | 固定 `reception_management`；端侧据此路由到已注册的接待管理组件页 |
| `url` | — | **禁止填**：本交互不走外链 URL，由 `componentKey` 路由到端侧组件 |
| `iconUrl` | string（可选） | 卡片左侧 18×18 方形图标；不传则显示默认 🌐 |

### 完整数据示例

```json
{
  "type": "open_tab",
  "selectionType": "reception_management",
  "pageTitle": "接待专员",
  "pageDescription": "查看接待管理和质检状况",
  "componentKey": "reception_management"
}
```

### 触发场景（与 SKILL.md §4.2 / 意图路由表对齐）

| 商家意图 / 触发源 | 主 Agent 行为 |
| --- | --- |
| 调接待范围 / 改 L 等级 / 再加 L3 / 不接 KA / 改买家等级 | 调 `show_interaction(name='manage_reception')` |
| 暂停接待 / 恢复接待 / 让它休息 / 不要它接了 / 重新上岗 | 调 `show_interaction(name='manage_reception')` |
| 管理接待助手 / 看看配置 | 调 `show_interaction(name='manage_reception')` |
| 改接待时间 / 改红线 / 改接待需求（平台默认不可改） | 先答「平台默认不可改」，再调 `show_interaction(name='manage_reception')`（能改的 L 等级 / 暂停项还是给入口） |
| paused 状态首页卡片点击 | 调 `show_interaction(name='manage_reception')` |

### 回传

fire-and-forget，端侧立即返回 `{ displayed: true, pageTitle, pageDescription, componentKey }`，**不等用户操作**，主 Agent 不基于回传做后续动作；商家所有写入操作（改 L 等级 / 切暂停 / 切恢复）均由页面内部直接调底层接口（页面内调 `cowboy_config update / pause / resume`）完成，**主 Agent 在主对话里不再发起任何 `cowboy_config update / pause / resume` 写入**。

### 严禁

- **禁止填 `url` 字段**：本交互由 `componentKey` 路由，不走外链 URL；填 `url` 会让端侧二选一时优先走错路径
- **禁止改 `componentKey`**：与端侧已注册组件键强绑定，写错即页面打不开
- **禁止主 Agent 在对话里调 `cowboy_config update / pause / resume`**：写入动作仅能由本 Tab 页面内部完成

---

## 字段映射速查（一图流）

| Step | interaction name | type | selectionType | 关键字段 | 必答 |
| --- | --- | --- | --- | --- | --- |
| Step 1 | `hire_step1_intro` | `rich_card` | `hire_intro` | 单按钮 `start` | `true` |
| Step 2 | `hire_step2_platform_auth` | `rich_card` | `platform_auth` | 单按钮 `confirm` | `true` |
| Step 3 | `hire_step3_buyer_levels` | `card` | `buyer_levels` | 单题多选「哪些买家让我接待」（L0~L6 共 7 选项） | `true` |
| Step 4 | `hire_step4_sim_dialog` | `conversation_sim_card` | `sim_dialog` | `simQuestions` 3 选 1 / `confirmButtonLabel` | `true` |
| 招聘后管理入口 | `manage_reception` | `open_tab` | `reception_management` | `componentKey='reception_management'` / `pageTitle='接待专员'` | fire-and-forget（不需回传） |

---

## 严禁事项

1. **禁止改 `selectionType`**：5 个值（`hire_intro` / `platform_auth` / `buyer_levels` / `sim_dialog` / `reception_management`）与云端落库表 / 端侧组件路由强绑定，改动会导致回调写错位置 / 页面打不开
2. **禁止改按钮 / `confirmButtonLabel` / `options` 文案**：前端按字面量匹配触发后续动作（"好的，开始面试" / "确认" / "确认模拟效果" / §3 「L0~L6 买家」7 选项全是协议契约）
3. **禁止增删 §3 的题目 / 选项**：仅 1 题「哪些买家让我接待」7 选项（L0~L6），与子账号 `allowBuyerLevelList` 字段强绑定，增删任一项都会破坏 `--levels` 推导；**同时禁止将 `allowCustomOption` 设为 `true` 或省略**，必须显式传 `false`，任何商家自填项会走不下去 `--levels` 映射、导致 `cowboy_config create` 失败
4. **禁止替换组件类型**：5 个交互的 `type` 已在 frontmatter 锁定（§1 `rich_card` / §2 `rich_card` / §3 `card` / §4 `conversation_sim_card` / §5 `open_tab`），调用方不可改用其它类型
5. **禁止主 Agent 在 §4 之外的任何位置调 `cowboy_config create`**：必须严格绑定 Step 4 「确认模拟效果」后 + 必带 `--levels`
6. **禁止在 §3（Step 3 提交）调 `cowboy_config create` 或激活接待助手**：§3 仅将该题映射出的 L 等级写入会话上下文暂存；接口调用 + status 写入 `active` 均由 §4 「确认模拟效果」后主 Agent 完成
7. **禁止主 Agent 在对话里调 `cowboy_config update / pause / resume`**：招聘完成后任何配置修改仅能调 `show_interaction(name='manage_reception')` 打开接待管理 Tab，写入动作由页面内部完成
8. **禁止给 `manage_reception` 填 `url` 字段**：本交互由 `componentKey` 路由到端侧已注册组件，不走外链URL
9. 🚨 **禁止在同一轮主 Agent 回复中并行 / 批量调多次 `show_interaction`**：招聘 4 步剧情卡必须一步一停—调完 Step N 后本轮立即结束，等用户在前端点击卡片回传后，下一轮才允许调 Step N+1；同轮多卡会让前端堆叠 3+ 张未确认卡、彻底破坏交互。
