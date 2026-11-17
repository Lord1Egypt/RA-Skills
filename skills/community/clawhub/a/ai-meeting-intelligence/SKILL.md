---
name: "AI Meeting Intelligence Expert"
description: "AI-powered meeting intelligence assistant — automatically transcribe, summarize, extract action items, generate follow-ups, and track decisions across your meeting lifecycle. Supports multi-language transcription, speaker identification, sentiment analysis, and integration with calendar/email tools. Built for project managers, executives, sales teams, and distributed teams who need to capture and act on meeting insights without manual note-taking. Keywords: meeting notes, meeting transcription, action items extraction, meeting summary, decision tracking, calendar integration, agenda preparation, meeting efficiency, AI meeting assistant, 会议纪要, 会议转录, 智能摘要, 行动项提取, 会议效率, 待办跟进, 决策追踪."
version: "1.0.4"
---

# AI Meeting Intelligence Expert

## Overview

Transform chaotic meetings into structured, actionable insights. This AI-powered meeting intelligence assistant handles the complete meeting lifecycle—from agenda preparation to decision tracking—freeing you to focus on what matters: the conversation itself.

## Triggers

**Activate only when the request is about a meeting artefact** — an agenda, a
transcript, a set of notes, a decision log or an action-item list. The keywords
below are necessary but not sufficient on their own.

- 中文触发词：`会议纪要`、`智能会议`、`会议分析`、`会议摘要`、`提取行动项`、`会议转录`、`开会被忘`
- English triggers: `meeting notes`, `meeting summary`, `transcribe meeting`, `action items`, `decision tracking`, `prepare meeting`, `meeting agenda`

**Required context (at least one must be present)**

1. There is a meeting artefact in the request (notes, transcript, agenda, minutes), or
2. A meeting is being prepared for, or
3. A decision or action item from a meeting is being tracked or followed up.

**Non-triggers — do not activate for these**

| Ambiguous request | Why not this skill | Route to |
|---|---|---|
| "action items" from a project plan or a document | No meeting artefact; it is task management | Project/task tooling |
| "summarise this contract / report" | Document summarisation, not a meeting | Document summarisation skill |
| "transcribe this audio" of a lecture or interview | Not a meeting; consent and purpose differ | Transcription tooling |
| "notes" meaning personal study notes | No meeting, no attendees, no decisions | Note-taking app |
| "meeting room booking" / calendar scheduling | Logistics, not content | Calendar tooling |
| "draft an email" with no meeting source | General writing | Writing assistance |

**Scope note**: this skill drafts artefacts for you to review. It does not join or
record meetings, does not access your calendar or mailbox, and does not write files
or send email without the explicit confirmation described in the next section.

## Data Handling & Privacy (read first / 前置声明)

Meeting content is one of the easiest ways to leak sensitive information into a
model context. Apply these rules before pasting anything:

**Data minimisation（数据最小化）**
1. Paste only what is needed for the task. A 200-line verbatim transcript is
   rarely necessary — a structured bullet list carries the same decisions.
2. Strip the following before sharing: 身份证号/护照号、银行账号、保单号、
   手机号、家庭住址、薪酬数字、未公开财务数据、客户名单、医疗健康信息。
3. Replace identifiers with stable pseudonyms (`客户A`、`Region-2`) and keep the
   mapping locally, outside the conversation.
4. If a meeting is legally or regulatorily sensitive, keep processing local and
   do not send content to third-party services without an approved DPIA.

**Save-and-send gate（保存与外发必须先预览确认）**
- Never write a summary to a file, send a follow-up email, or update a tracker
  as a bare action. Always:
  1. Show the full draft to the user,
  2. Mark the items that contain personal or confidential data,
  3. Wait for explicit confirmation ("确认发送" / "确认保存"),
  4. Only then persist or send.
- Drafts are inert until confirmed. Treat "send" and "save" as separate,
  individually confirmed actions.

**Consent（录音与转录的同意）**
- Recording and transcribing meetings requires the consent of participants;
  requirements differ by jurisdiction. Confirm your organisation's policy
  before enabling automatic transcription.

**Accuracy boundary**
- A summary is a lossy artifact. For anything with legal, financial or
  regulatory effect, the authoritative record is the approved minute, not the
  AI-generated draft.

## Features

### 1. Pre-Meeting Preparation
- Generate structured meeting agendas based on topic keywords
- Create attendee briefing documents from CRM/project data
- Suggest time allocations for each agenda item
- Provide historical context from past meeting notes


**Worked example — 15-minute agenda generated from a one-line brief**

Brief: `"理赔时效专项复盘会，参会：运营、客服、IT，60 分钟"`

| Slot | Item | Owner | Min | Output expected |
|---|---|---|---|---|
| 0–5 | 上期行动项闭环情况 | 运营 | 5 | 3 项已闭环 / 2 项延期及原因 |
| 5–20 | 时效数据：结案时长分布 | 运营 | 15 | P50 / P90 与上月对比 |
| 20–40 | 卡点归因：系统与人工各占多少 | IT + 客服 | 20 | Top 3 卡点及责任方 |
| 40–55 | 决策：是否调整时效考核口径 | 全体 | 15 | 明确是/否 + 生效日 |
| 55–60 | 行动项与责任人确认 | 主持人 | 5 | 每项一责任人一截止日 |

The last two rows are what generic agenda generators omit: a named decision and
a named owner per item."


**第二例 — 议程被压缩到 30 分钟时怎么砍**

原 60 分钟议程压缩到 30 分钟时，不要按比例缩短每一项（那会让每一项都做不完），
而是整段删除：保留"决策项"与"行动项确认"（共 20 分钟），把数据汇报改为会前阅读材料，
卡点归因改为会后专项。判断标准很简单——**需要多人当场表态的环节必须留在会上，
只需要传递信息的环节一律移出会议**。


### 2. Real-Time Transcription Support
- Process live meeting notes and convert to timestamped transcript
- Identify and label different speakers
- Flag action items, decisions, and questions in real-time
- Highlight sentiment shifts during discussions


**Worked example — live tagging shorthand**

Use single-character marks while the meeting runs, then expand them afterwards:

```
[D] decision   [A] action   [Q] question   [R] risk   [T] tbd/需要补数据
   ↓
09:12 [D] 万元以下的案件不再要求人工复核 —— 运营负责人确认
09:20 [A] IT 在 9/20 前提交接口改造方案
09:31 [Q] 带病体案件是否适用同一时效口径？—— 未决
09:44 [R] 若 10 月上线，与年终结算并行，存在回归风险
09:52 [T] 缺少 8 月分中心数据，待补
```

Two rules that make the expansion reliable:
- Every `[A]` must get an owner and a date before the meeting ends; an action
  without both is not an action.
- Every `[Q]` must be either answered or carried to the next agenda. Unanswered
  questions that silently disappear are the main failure mode of meeting notes.

**第二例 — 打断与跑题的现场处理**

```
10:05 [T] 话题从"时效口径"跳到"系统改造预算" —— 记为新议题，不合并
10:18 [A] 预算部分另开一次会，主持人在会后 1 天内发出邀请
10:22 [D] 本次会议只解决时效口径，预算不在本次决策范围
```

要点：跑题不等于无效。把被搁置的话题记为独立的 `[T]`，并显式记下"本次不决策"，
比强行拉回主线更能保护会议产出——被拉回的话题往往下次会议原样重现。


### 3. Post-Meeting Intelligence
- Generate comprehensive meeting summaries (30-second, 1-minute, 5-minute versions)
- Extract and format action items with owners and deadlines
- Create follow-up email drafts for stakeholders
- Update project trackers and task managers


**Worked example — three summary lengths from the same meeting**

| Version | Length | Reader | Contains | Must NOT contain |
|---|---|---|---|---|
| 30-second | 2–3 句 | 高管/未参会者 | 结论 + 金钱/时间影响 | 过程、争论细节 |
| 1-minute | 1 段 | 参会者 | 结论 + 行动项 + 责任人 | 逐字引用、情绪描述 |
| 5-minute | 1 页 | 项目组/审计 | 决策依据、反对意见、数据、未决问题 | 与决策无关的闲聊 |

Rule: the same 3 facts must appear in all three versions. If they differ, the
short version is editorialising rather than summarising.

**Follow-up email micro-example**

```
Subject: 理赔时效专项复盘会 - 决策与你的行动项（9/10）

本次确认：
1. 万元以下案件取消人工复核，10/1 起生效
2. 时效考核口径维持不变（未调整）

你的下一步：
- IT 接口改造方案 —— 9/20 前提交
- 8 月分中心数据 —— 9/12 前补齐

待决事项：带病体案件是否适用同一口径，下次会议定
```
Note the last line: unresolved items are stated as unresolved. Omitting them is
what makes follow-ups misleading.


### 4. Meeting Analytics
- Track meeting frequency, duration, and attendance
- Identify recurring discussion topics
- Measure action item completion rates
- Generate meeting ROI reports


**Worked example — a quarterly meeting-health report**

| Metric | This quarter | Last quarter | Read | Action if bad |
|---|---|---|---|---|
| 会议总时长/人/周 | 9.5 h | 11.2 h | 下降，健康 | — |
| 无议程会议占比 | 41% | 38% | 恶化 | 强制模板 |
| 决策会占比 | 22% | 25% | 略降 | 合并周会 |
| 行动项按期完成率 | 63% | 71% | 恶化 | 减少并行项 |
| 平均参会人数 | 8.4 | 7.9 | 微增 | 拆小会 |
| 重复议题次数 | 6 | 3 | 翻倍 | 该议题需专项决策 |

Interpretation guardrails:
- A high action-completion rate with very few action items usually means the
  meeting produced nothing, not that the team is efficient.
- "Recurring topics" is the strongest signal: the same topic 3+ times means it
  needs a decision owner, not another meeting.

**第二例 — 用会议健康度数据砍掉一场会**

同样的数据如果显示：`无议程会议占比 41%` 且 `决策会占比 22%`，最有效的动作通常不是
"提高会议质量"，而是结构性调整：把每周例会改为双周，并要求无议程的会议自动取消。
会议分析的输出应当落在"会议数量与形式"上，而不是落在"参会者态度"上——后者无法度量，
也容易变成对个人的评价。


## Workflow

### Basic Meeting Summary Workflow

```
1. INPUT: Meeting transcript/notes/raw text
   ↓
2. PROCESS: AI extracts key information
   - Speakers and roles
   - Topics discussed
   - Decisions made
   - Action items assigned
   - Questions raised
   ↓
3. OUTPUT: Structured meeting intelligence
   - Executive summary
   - Action item list
   - Decision log
   - Follow-up recommendations
```

### Full Meeting Lifecycle Workflow

```
Phase 1: Preparation
├── Receive meeting topic/context
├── Generate agenda template
├── Pull relevant background data
└── Prepare attendee briefings

Phase 2: During Meeting
├── Log notes in real-time
├── Mark key moments
├── Track time vs. agenda
└── Note unresolved items

Phase 3: Post-Meeting
├── Transcribe and clean up notes
├── Generate summary versions
├── Extract action items
├── Draft follow-ups
└── Update trackers

Phase 4: Follow-Through
├── Send summaries to attendees
├── Create task reminders
├── Track action item status
└── Flag overdue items
```

## Input Examples

### Example 1: Meeting Notes Input
```
Meeting: Q2 Product Planning
Date: 2026-05-15
Attendees: Sarah (PM), Mike (Eng), Lisa (Design), John (Sales)

Notes:
- Sarah opened with Q1 review, metrics looking good
- Mike mentioned technical blockers on API integration
- Lisa showed new mockups, everyone loved the dark mode
- John said enterprise clients are asking for SSO
- Decided to prioritize SSO for next sprint
- Mike will create technical spec by Friday
- Lisa to update mockups with SSO flows by next week
- Sarah to schedule follow-up with enterprise team
```

**Expected Output:**
```markdown
## Meeting Summary: Q2 Product Planning

### Quick Take (30 sec)
Q1 metrics positive. Team aligned on Q2 priorities: SSO feature for enterprise clients. Technical spec due Friday, mockups by next week.

### Decisions Made
1. Prioritize SSO implementation in next sprint
2. Enterprise team meeting to be scheduled

### Action Items
| Item | Owner | Due Date |
|------|-------|----------|
| Create technical spec for SSO | Mike | 2026-05-20 |
| Update mockups with SSO flows | Lisa | 2026-05-22 |
| Schedule enterprise team follow-up | Sarah | 2026-05-18 |

### Discussion Highlights
- Enterprise clients requesting SSO (high priority)
- Dark mode mockups well received
- API integration blockers acknowledged
```

### Example 2: Action Item Extraction
**Input:** Raw meeting transcript or bullet points
**Output:** Structured action item list with:
- Task description
- Assigned owner
- Deadline (if mentioned)
- Priority level
- Related context

### Example 3: Meeting Agenda Generation
**Input:** "Quarterly planning meeting with engineering and product teams"
**Output:**
```markdown
## Q2 Planning Meeting Agenda

### Pre-Meeting (15 min)
- Review Q1 OKRs and completion status
- Prepare Q2 targets draft

### Agenda (60 min total)
1. Q1 Retrospective (15 min)
   - Wins to celebrate
   - Areas for improvement
   
2. Q2 Goal Setting (25 min)
   - Product roadmap alignment
   - Engineering capacity planning
   - Resource requirements
   
3. Team Updates (10 min)
   - Cross-functional dependencies
   - Blockers and risks
   
4. Wrap-Up (10 min)
   - Confirm decisions
   - Assign next steps
```

### Example 4: 中文会议纪要（金融场景，含脱敏）

**Input（用户已自行脱敏）:**
```
会议：医惠锡城产品定价讨论
时间：2026-09-08  参会：产品部A、精算B、数据C、合规D

- A：带病体承保的赔付率数据还没拿到，医保局接口预计 9 月下旬开通
- B：没有带病体数据，只能先用行业经验值做区间定价，误差可能 ±15%
- C：健康体部分数据已够，可以先出健康体方案
- D：区间定价对外披露要谨慎，定价说明里不能出现未经验证的假设
- 决定：先出健康体方案（9/20 前），带病体等数据到齐后第二版
- B 负责健康体精算假设文档，9/18 前
- C 负责与医保局对接，每周反馈接口进度
```

**Expected Output:**
```markdown
## 会议纪要：医惠锡城产品定价讨论（2026-09-08）

### 30 秒摘要
带病体赔付数据尚未获取（医保局接口预计 9 月下旬开通），会议决定分两版推进：
健康体方案 9/20 前先出，带病体方案待数据齐备后出第二版。

### 决策
1. 采用分版推进：健康体先行（9/20 前），带病体后置
2. 带病体暂不使用未经验证的行业经验值作为对外定价依据

### 行动项
| 事项 | 责任人 | 截止 | 交付物 |
|---|---|---|---|
| 健康体精算假设文档 | B（精算） | 09-18 | 假设说明 + 敏感性测试 |
| 医保局接口对接周报 | C（数据） | 每周五 | 进度反馈 |
| 健康体方案初稿 | A（产品） | 09-20 | 方案文档 |

### 未决事项
- 带病体赔付率数据来源与时效（依赖外部接口，非本团队可控）
- 区间定价的对外披露口径（需合规复核）

### 风险
- 若接口延迟超过 10 月中旬，带病体方案将错过产品报备窗口 —— 建议 9/30 设检查点
```

**保存前提示**: 本纪要含产品名称与内部时间安排，属内部信息。
请确认分发范围后再保存或外发；对外版本需删除"风险"与"未决事项"两节。

### Example 5: 跨会议决策追踪

**Input:**
```
我们有 6 次关于"是否上数据中台"的会议记录。这个决策到底定了没有？
```

**Output:**
```
决策追踪结果：未定（已讨论 6 次）

| # | 日期 | 结论 | 阻塞原因 | 状态 |
|---|---|---|---|---|
| 1 | 06-12 | 待评估 | 需要成本测算 | 已闭环 |
| 2 | 06-26 | 待评估 | 需要成本测算（未做） | 延期 |
| 3 | 07-10 | 倾向做 | 需要确定牵头部门 | 未闭环 |
| 4 | 07-24 | 待评估 | 牵头部门未定（重复阻塞） | 延期 |
| 5 | 08-14 | 倾向做 | 预算未批 | 未闭环 |
| 6 | 09-04 | 待评估 | 又回到成本测算 | 回退 |

诊断：
- 6 次会议中，"成本测算"出现 3 次、"牵头部门"出现 2 次，均未闭环
- 这不是信息不足的问题，是没有人为这两件事负责
- 会议在"倾向做"和"待评估"之间循环，属于典型的无主决策

建议（不是再开一次会）：
1. 指定一名决策提案人（不是会议召集人），负责写出一页纸提案
2. 明确决策人与决策日期（例如 9/30 前由分管领导拍板）
3. 若 9/30 无法决策，则显式记录"本季度不做"，并在下季度重新评估
4. 第 7 次会议的议程应只含一项：拍板或明确否决

给管理层的提示：重复议题超过 3 次，成本已经超过决策本身的价值。
```

### Example 6: A request that looks in-scope but is not

**Input:**
```
帮我整理一下这份项目计划里的 action items。
```

**Output:**
```
This is task management, not meeting intelligence — the source is a project plan,
not a meeting artefact, so the meeting-specific handling (consent, distribution
scope, decision-vs-discussion distinction) does not apply.

What to do instead:
1. Confirm the source document and who owns its action list.
2. Extract owner + due date per item; skip the decision log entirely.

Come back to this skill if any of the following becomes true:
- The action items originate from a meeting and you have the notes or transcript.
- You need a decision log that distinguishes "decided" from "discussed".
- You are preparing the agenda for the meeting where these items will be reviewed.
```



## Output Templates

### Template 1: Meeting Summary
```markdown
## [Meeting Title]

**Date:** [Date]
**Time:** [Start] - [End]
**Location:** [Room/Video Link]
**Attendees:** [Names and Roles]

### Executive Summary
[2-3 sentence overview]

### Agenda vs. Actual
| Topic | Planned | Actual |
|-------|---------|--------|
| ... | ... | ... |

### Key Decisions
1. [Decision 1]
2. [Decision 2]

### Action Items
- [ ] [Task] - @Owner - Due: [Date]
- [ ] [Task] - @Owner - Due: [Date]

### Open Questions
- [Question 1]
- [Question 2]

### Next Meeting
- Scheduled: [Date/Time]
- Focus: [Topics]
```

### Template 2: Follow-Up Email
```markdown
Subject: [Meeting Title] - Key Decisions & Your Action Items

Hi [Name],

Following up on today's [meeting name]. Here's a quick summary:

**What We Decided:**
- [Decision 1]
- [Decision 2]

**Your Next Steps:**
- [Action item 1] - by [date]
- [Action item 2] - by [date]

**Resources:**
- [Link to meeting notes]
- [Link to relevant documents]

Let me know if you have any questions!

Best,
[Your name]
```

## Meeting Type → Template Cheat Sheet

| 会议类型 | 核心产出 | 纪要侧重 | 最常遗漏 | 分发范围 | 保存前确认点 | 建议的 AI 参与度 |
|---|---|---|---|---|---|---|
| 例会/站会 | 进度同步 |  blockers 与变更 | 上周行动项状态 | 团队内部 | 是否含未公开排期 | 全自动：结构化后直接分发 |
| 决策会 | 一个明确决策 | 决策 + 依据 + 反对意见 | 决策生效日与适用范围 | 决策相关方 | 决策表述是否与决议一致 | 半自动：决策措辞必须人工定稿 |
| 评审会 | 通过/不通过 + 修改清单 | 问题清单与责任人 | 未通过项的重审时间 | 项目组 | 是否含个人绩效评价 | 半自动：问题清单可生成，结论人工填 |
| 1on1 | 成长与障碍 | 约定项（不写细节） | 双方共同确认 | 仅双方 | 默认不留存细节，确认后再存 | 最低：只做格式整理，内容人工写 |
| 客户/外部会议 | 承诺与下一步 | 对外承诺的准确措辞 | 内部推测被写入对外版 | 内外部版本分开 | 内外两版分别确认 | 半自动：内外部两版分别生成并人工比对 |
| 复盘会 | 可复用结论 | 时间线 + 根因 + 改进项 | 谁负责跟改进项 | 相关团队 | 是否含追责性表述 | 半自动：时间线可生成，根因人工判断 |
| 董事会/监管类 | 合规留痕 | 逐项决议、表决情况 | 出席与回避记录 | 法定范围 | 须与正式决议文本核对 | 最低：仅做留痕模板，须与决议文本核对 |

## Integration Recommendations

| Use Case | Recommended Tools | 数据敏感度 | 是否需要脱敏 | 保存/外发前的人工确认点 | 典型误用 |
|---|---|---|---|---|---|
| Calendar sync | Google Calendar, Outlook | 低（标题/时间） | 一般不需要 | 外部参会人是否可见 | 把议题详情写进日历标题外泄 |
| Note-taking | Notion, Obsidian, Evernote | 高（全文） | 需要 | 全文预览 + 确认落库 | 未脱敏全文直接同步到云端 |
| Task management | Todoist, Asana, Linear, Jira | 中（任务描述） | 视描述内容 | 任务名是否含客户名 | 把客户名写进公开看板 |
| Video conferencing | Zoom, Google Meet, Teams | 高（录音/转录） | 需要 | 参会人同意 + 保留期限 | 未经同意开启自动转录 |
| CRM sync | Salesforce, HubSpot | 高（客户信息） | 需要 | 字段级确认 | 把内部猜测写入客户档案 |
| Email follow-ups | Gmail, Outlook | 高（对外） | 需要 | 内外部版本分别确认 | 直接发送未经确认的草稿 |
| 本地归档（推荐） | 本地 Markdown / 内网 Wiki | 可控 | 视内容 | 落盘路径与权限确认 | 默认保存到公共目录 |

## Ecosystem & Compliance Notes (as of 2026-11-13 / 截至 2026-11-13)

Verify every item against your vendor's documentation and your own compliance
function before acting on it.

| 关注点 | 需向谁确认 | 与本技能的关系 |
|---|---|---|
| 会议录音/转录的告知同意要求 | 本单位合规/法务 | 决定能否开启自动转录 |
| 会议记录的保存期限与归档方式 | 档案与合规部门 | 决定纪要落哪里、存多久 |
| 金融/保险机构会议留痕要求 | 监管机构最新规定（以官方发布为准） | 涉及决策类会议的纪要完整性 |
| 第三方会议 AI 服务的数据出境与存储地 | 供应商 DPIA/合同 | 决定能否使用云端转录 |
| 生成式 AI 处理内部信息的内部政策 | 本单位 AI 治理制度 | 决定哪些内容可进入模型上下文 |
| 会议 AI 生成内容的标识与可追溯要求 | 本单位 AI 治理 / 合规 | 决定纪要是否需标注 AI 参与及保留修改痕迹 |

**最近动态（截至 2026-11-13，以官方最新发布为准）**
1. 会议 AI 功能（实时转录、自动摘要、行动项提取）已成为主流办公与会议
   平台的标配，竞争重点从"能否生成"转向"生成结果能否被审计与追溯"。
2. 金融机构对会议记录留痕与可追溯性的要求持续强化，决策类会议纪要往往
   需要与正式决议文本一致，AI 草稿不能替代正式记录。
3. 数据最小化与本地化处理成为会议 AI 选型的常见前置条件，部分场景要求
   在内网完成转录与摘要。
4. 会议 AI 的"可追溯性"要求继续细化：越来越多机构要求纪要标注 AI 参与环节、
   保留修改痕迹，并能区分"AI 草稿"与"经确认的正式记录"。
5. 本地化/内网部署的会议转录与摘要方案在受监管行业的采用度上升，选型时通常把
   "数据不出网"作为硬性前置条件而非加分项。
6. 以上为趋势性描述，具体义务以所在司法辖区与监管机构最新规定为准。

## Best Practices

### For Meeting Organizers
1. Share agenda 24h before meeting
2. Designate a note-taker or use AI assistance
3. Start and end on time
4. Review and share summary within 2 hours

### For Action Item Tracking
1. Assign one clear owner per item
2. Set specific, achievable deadlines
3. Include context for why the task matters
4. Follow up within 48 hours of deadline

### For Meeting Efficiency
1. Default to 25 or 50-minute meetings
2. Include breaks for meetings over 90 minutes
3. Limit attendees to decision-makers and contributors
4. Record meetings (with consent) for accurate transcription

## Edge Cases & Troubleshooting

### Challenge: Incomplete Notes
**Solution:** Provide the AI with whatever you have—bullet points, partial transcripts, even voice memos. The assistant can work with fragmentary input and will clearly indicate confidence levels.

### Challenge: Multiple Meetings in One Day
**Solution:** Use the daily digest feature to get an overview of all meetings, cross-reference action items, and identify scheduling conflicts.

### Challenge: Unclear Action Item Ownership
**Solution:** When ambiguous, flag the item for clarification rather than assigning arbitrarily. Include a "Verify owner" tag.

### Challenge: Confidential Discussions
**Solution:** Emphasize that sensitive meetings should be handled locally. Provide a "sanitize" mode that removes sensitive names/companies while preserving structure.

## Version History

- **1.0.1** (2026-09-10)
  - Added "Data Handling & Privacy" front matter: data minimisation rules,
    save/send preview-and-confirm gate, consent and accuracy boundaries
  - Added worked examples to all four feature groups (agenda with decision+owner
    rows, live tagging shorthand, three summary lengths, quarterly health report)
  - Added "Meeting Type → Template Cheat Sheet" (7 meeting types, 6 columns)
  - Expanded integration table from 2 to 6 columns (sensitivity, masking need,
    human checkpoint, typical misuse)
  - Added Example 4 (Chinese meeting minutes with masking) and Example 5
    (cross-meeting decision tracking)
  - Added "Ecosystem & Compliance Notes (as of 2026-09-10)"
- **1.0.2** (2026-09-28)
  - Narrowed the trigger section: keywords are now necessary-but-not-sufficient,
    with a required-context rule, a six-row non-trigger disambiguation table and
    an explicit scope note that the skill does not join, record, read calendars or
    send anything unconfirmed (SQP-1, both Chinese and English trigger sets)
  - Added an "建议的 AI 参与度" column to the meeting-type cheat sheet
  - Added a compliance row on AI-generated content labelling and traceability
  - Added a second worked example to three feature modules (agenda compression,
    digression handling, structural fixes from health data)
  - Added Example 6 showing an out-of-scope request and its routing
  - Ecosystem & Compliance notes updated to 2026-09-28 with two added dynamics
- **1.0.0** (2026-05-15): Initial release
  - Core meeting summary generation
  - Action item extraction
  - Decision tracking
  - Basic agenda generation

**Last Updated**: 2026-11-13

## 本轮增量（2026-11-13）：复核维度与举例补充

> 本节为 2026-11-13 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**1. Pre-Meeting Preparation**：

- 议程模板先固定「决策项 / 讨论项 / 同步项」三类并标注每类预期产出，避免把需要拍板的事项混入同步项导致会后无结论。
- 会前材料准备时附「需预先阅读的页数与预计耗时」，并把保密级别标注在文件名与正文首页，减少会中临时投屏带来的暴露面；后续处理按文首的保存与外发确认门控执行，本技能不预设口径。

**Edge Cases & Troubleshooting**：

- 多人同时发言且转写串轨时，先按发言人标签切分并标注「疑似重叠」区间，交参会人确认后再进纪要，不自动归并成一段。
- 会议中途有临时旁听者加入时，纪要草稿先记「参会变更时点」，并把该时点前后的敏感内容列为「待人工确认区段」；是否纳入最终纪要、以及后续如何处理，均由会议组织者在人工确认环节决定，本技能不预设口径。

### 新增复核维度表（2026-11-13）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 议程产出标注 | 会议组织者 | 议程模板 + 会前材料 | 三类事项是否分明、预期产出是否可验收 | 中 | 仅作纪要草稿，正式纪要须参会人确认 |
| 参会变更与待确认区段 | 会议组织者 + 纪要复核人 | 参会记录 + 转写分段 | 变更时点、待确认区段、确认留痕 | 高 | 涉及敏感内容须人工复核后由人员按既有流程处理 |

### 适用边界 / 数据最小化 / 执行边界（本期补齐）

**适用边界**：本技能仅用于会议纪要与会议协同的文本处理的方法论参考与结构拆解，输出为供具备相应资质人员复核的草稿；不构成对具体主体、标的、客户或案件的最终结论、指令或承诺。超出该范围的场景（如实盘执行、自动审批、对外正式报送、系统登记）不适用本技能，应转由相应业务系统与授权人员处理。

**执行边界**：本技能不内置、不代为执行任何工具调用、网络请求、落盘写入、外发或审批动作；文中流程均为示意步骤，由宿主代理在用户授权环境内按机构规范执行。涉及不可逆或高影响动作须经人工预览与确认，并保留输入、输出、版本、耗时与责任人的最小留痕；无人工确认环节不得自动推进。


> **口径澄清（2026-11-13 修正）**：本节所有条目均为纪要草稿与纸面清单，不含任何自动分发、自动共享或自动外发动作；涉及敏感内容的状态变更与后续处理，一律以文首的保存与外发确认门控为准，由具备权限的人员在人工确认后执行。
### 时效性说明

- 本期时效性核查：**截至 2026-11-13**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
