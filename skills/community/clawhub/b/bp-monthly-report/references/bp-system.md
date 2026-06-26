# BP System

This file captures the BP business semantics and the recommended fetch order for monthly report drafting.

Source documents:

- API document: [BP系统API说明](https://github.com/xgjk/dev-guide/blob/main/02.%E4%BA%A7%E5%93%81%E4%B8%9A%E5%8A%A1AI%E6%96%87%E6%A1%A3/BP/BP%E7%B3%BB%E7%BB%9FAPI%E8%AF%B4%E6%98%8E.md)
- Business document: [BP系统业务说明](https://github.com/xgjk/dev-guide/blob/main/02.%E4%BA%A7%E5%93%81%E4%B8%9A%E5%8A%A1AI%E6%96%87%E6%A1%A3/BP/BP%E7%B3%BB%E7%BB%9F%E4%B8%9A%E5%8A%A1%E8%AF%B4%E6%98%8E.md)

## Core business semantics

- `目标` is the desired end state. It should describe the result state, not the action.
- `关键成果` is the acceptance basis for whether the goal is achieved.
- `衡量标准` belongs to the key result and is the main evaluation basis.
- `关键举措` is the action path for achieving the key result.

For monthly report drafting, the main evaluation chain is:

`目标 -> 关键成果 -> 衡量标准 -> 关联汇报`

Not:

`目标 -> 关键举措 -> 做了什么`

This means:

- use actions to explain why progress happened
- do not use action count as the primary proof of achievement
- judge completion pressure mainly against result-level standards
- still fetch and read action-linked reports, because many month-specific operating facts are attached at the action layer

## What must be confirmed first

Before fetching any BP data, confirm:

1. BP period
2. target node

The target node should be resolved to one of:

- `groupId`
- `employeeId`
- a unique node name that can be resolved to a BP group

Without `period + node`, the report scope is unstable.

## Recommended API fetch order

Use this order when fetching from the BP system.

### Step 1: resolve period

- `GET /bp/period/getAllPeriod`

Prefer the enabled period, but if the user specified a period, use that exact period.

### Step 2: resolve node to group

If the user gives an employee:

- `POST /bp/group/getPersonalGroupIds`

If the user gives a node name or needs tree browsing:

- `GET /bp/group/getTree`

### Step 3: get the node BP skeleton

Choose one of these:

- `GET /bp/document/getBpMarkdown?groupId=...`
- `GET /bp/task/v2/getSimpleTree?groupId=...`

Use BP Markdown to quickly understand the full node BP.
Use task tree when you need exact task IDs for downstream fetches.

### Step 4: get detailed goal and result data

Preferred:

- `GET /bp/task/v2/getGoalAndKeyResult?id=...`
- `GET /bp/task/v2/getKeyResult?id=...`

Reason:

- goal detail gives the goal and all nested key results and actions
- key result detail exposes `measureStandard`
- result-level detail is the main evaluation basis for the report

### Step 5: fetch related report ids from BP

- `POST /bp/task/relation/pageAllReports`

Recommended request shape:

- `taskId`
- `pageIndex`
- `pageSize`
- `sortBy: relation_time`
- `sortOrder: desc`

Important fields in the updated response:

- `bizId`: report id
- `type` or `typeDesc`: report type

The updated BP API is now used only as the BP-to-report-id bridge. Do not assume it still returns report title, body, or author.

### Step 6: fetch work-report details by `reportId`

Use the work-collaboration APIs after Step 5:

- `GET /work-report/report/info?reportId=...`
- `GET /work-report/report/getReportNodeDetail?reportId=...`

Use them for:

- report title
- report body
- report create time
- author
- replies
- node processing opinions

This is now the required detail-fetch chain for month report drafting.

Do not treat all related reports as equal evidence.
You must compare the report author against the current BP node's people.

The BP report-link API supports sorting by:

- `relation_time`
- `business_time`

For monthly reports, use:

- `sortBy: business_time`
- month attribution mode: `report_time`

Current fixed rule:

- only use `汇报日期`
- do not use `关联时间` as the default month-attribution rule
- do not use LLM inference on正文月份 as the default month-attribution rule

## Drafting priority rules

When multiple evidence types are available, use this priority:

1. key result `measureStandard`
2. goal and key result status
3. reports directly linked to goals or key results and written by the current responsible owner or assignee
4. reports linked to actions and written by the current responsible owner or assignee
5. reports written by others but linked to the same BP task
6. action metadata itself

This keeps the report focused on achievement judgment, not on process narration.

But keep the distinction explicit:

- `判断主轴`: `目标 -> 关键成果 -> 衡量标准`
- `证据抓手`: `目标汇报 + 成果汇报 + 举措汇报`

In practice, action-linked reports are often the richest place to find:

- concrete progress
- meeting outcomes
- decisions
- blockers
- next actions

## How each BP object should influence writing

### Goal

Use for:

- section 2 target statement
- section 1 high-level progress framing

Do not use goal text alone as proof of completion.

### Key result + measure standard

Use for:

- section 2 current state and deviation judgment
- section 3 result judgment
- section 5 issue and deviation identification
- section 6 risk assessment

This is the most important layer for report quality.

### Action

Use for:

- section 4 key initiatives
- root-cause explanation in section 5
- next-step arrangement in section 7
- concrete month facts when the main operating narrative is recorded at the action layer

Do not let section 4 dominate the whole report.

### Related reports

Use to:

- extract month-specific facts
- confirm progress, blockers, and decisions
- quote the latest operating narrative

Prefer manual reports first. Use AI reports as supplementary summaries, not as the sole evidence.
Within manual reports, prefer reports written by the current task's responsible owner or assignee.
If someone else wrote the report or linked the report to this BP, treat it as cross-reference evidence with lower priority.

## Author-priority rule

When using related reports, classify evidence in this order:

1. `primary`: written by the current goal or result owner, or the current action assignee
2. `secondary`: written by people directly collaborating on the same task
3. `auxiliary`: written by others but linked to the task
4. `summary_only`: AI-generated report

Monthly report conclusions should be based mainly on `primary` evidence.
If only `secondary` or `auxiliary` evidence exists, state that the judgment confidence is lower.

## Special constraints from the BP business rules

- Goals describe result states, not actions.
- Key results are the acceptance criteria for goals.
- Every key result should have a measurable standard.
- Actions belong under key results and should remain secondary in report evaluation.
- Reporting rhythm is constrained bottom-up: `举措汇报周期 <= 关键成果汇报周期 <= 目标汇报周期`.

## Practical report-writing rule

For every key BP line in the report, try to answer these questions in order:

1. What goal state is this line serving
2. Which key result proves or disproves progress
3. What is the measure standard
4. What month evidence from owner or assignee reports supports the judgment
5. Which actions explain the progress or deviation
