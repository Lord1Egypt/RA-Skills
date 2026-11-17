---
name: ai-coach-batch-session-summary
description: >-
  批量分析录音转写，生成多维度拓客分析报告。触发词：录音分析、
  总结、音频总结、拜访记录总结。
  当用户提到「分析录音」「看看录音数据」「最近的录音」「通话记录」且意图是批量统计/分析时触发。
  注意：单独出现「录音」「拜访」时需结合上下文判断，若用户只是查看单条录音详情则不触发本技能。
disable-model-invocation: false
---

# AI Coach · 批量会话 ASR 洞察报告

## 目标

1. **直接调用宿主「当前会话」查询**（OpenClaw：`session_status`，`sessionKey="current"`），从返回的 `sessionKey` / `agentId` 解析 **agentid**（规则与 [fetch-legionclaw-invite-code](../fetch-legionclaw-invite-code/SKILL.md) 一致）。
2. 调用录音服务 **`POST /api/recordings/asr-completed`**，以 **`userId` = agentid** 拉取已完成 ASR 的录音列表。
3. 按 **十维拓客**（或用户自定义维度）统计转写文本，生成与 [`asr_insight_template.html`](asr_insight_template.html) 同结构的 **HTML 洞察报告** 。
4. 将生成的 HTML **上传文件服务**，向用户返回 **公网可下载链接**（勿暴露 `/tmp/...` 等本地路径）。**优先**按 [openclaw-file-share](../openclaw-file-share/SKILL.md) 完成上传与回复改写；仅当该技能**未加载或不可用**时，改用下文「[交付 HTML 给用户](#交付-html-给用户文件上传)」中的兜底流程。无论哪条路径，**不得**只返回本地路径。

## 触发词设计与确认机制

### 触发决策流程

```
用户消息
  │
  ├─ 命中「高置信度」触发词 ──→ 直接执行，无需确认
  │
  ├─ 命中「中置信度」触发词 ──→ 向用户确认意图后再执行
  │
  └─ 命中「不触发」场景 ──→ 不触发本技能
```

### 高置信度触发（直接执行，无需确认）

用户消息中包含以下**组合关键词**时，直接触发：

| 触发词组合 | 用户可能说法 |
|-----------|-------------|
| 录音 + (分析\|总结) + 报告 | 「录音分析报告」「生成录音分析报告」 |
| 教练 + (会话\|录音) + (总结\|分析) | 「批量总结会话」「批量会话报告」 |
| 通话记录 + (分析\|总结) | 「分析一下通话记录」 |
| 拜访记录 + (总结\|分析) | 「总结最近的拜访记录」 |
| 录音转写 + 报告 | 「生成录音转写报告」 |

**口语化表达**（也直接触发）：

| 触发模式 | 用户可能说法 |
|---------|-------------|
| 帮我 + 分析/总结 + 录音/拜访/通话 | 「帮我分析录音」「帮我总结一下拜访」 |
| 生成 + 录音/拜访 + 报告 | 「生成录音报告」「弄个拜访报告」 |
| 看看 + 最近 + 录音/拜访/通话 + 情况 | 「看看最近录音情况」「看看拜访怎么样」 |
| 录音/拜访/通话 + 数据/情况 + 怎么样 | 「录音数据怎么样」「拜访情况如何」 |

### 中置信度触发（必须先确认再执行）

用户消息**仅包含**以下关键词、且**不含高置信度组合词**时，Agent **必须先向用户确认意图**，得到明确肯定后才执行本技能：

| 触发词 | 用户可能说法 | 确认话术 |
|--------|-------------|---------|
| 录音 | 「看看录音」「录音怎么样」 | 「您是想对近期录音做批量分析，还是查看某条录音的详情？」 |
| 拜访 | 「看看拜访情况」「拜访记录」 | 「您是想生成拜访录音的批量分析报告，还是查看某次拜访的详情？」 |
| 通话 | 「看看通话情况」 | 「您是想分析通话记录的整体情况，还是查看某条通话的详情？」 |
| 教练 | 「教练数据」「教练报告」 | 「您是想查看 AI 教练的批量录音分析结果，还是其他功能？」 |
| 最近的录音 | 「最近的录音怎么样」 | 「您是想对近期所有录音做批量分析，还是查看某一条？」 |

**口语化/模糊表达**（也需确认）：

| 用户可能说法 | 确认话术 |
|-------------|---------|
| 「帮我弄一下录音」 | 「您是想生成录音分析报告吗？」 |
| 「看看最近的数据」 | 「您是想分析最近的录音数据吗？」 |
| 「总结一下」 | 「您是想总结最近的录音/拜访情况吗？」 |
| 「搞个报告」 | 「您是想生成录音分析报告吗？」 |

**确认流程**：

1. Agent 识别到中置信度触发词
2. Agent 使用上表中的确认话术（或语义等价的自然表述）向用户提问
3. 用户明确回复「是批量分析」「做洞察报告」等肯定意图 → 执行本技能
4. 用户回复「看某一条」「播放」「详情」等 → **不触发**本技能，引导至对应功能
5. 用户未回复或意图仍模糊 → **不执行**，等待用户进一步说明

### 不触发场景

| 场景 | 用户说法示例 | Agent 处理 |
|------|-------------|-----------|
| 查看单条录音详情 | 「播放录音」「下载这条录音」「看看那条录音」 | 不触发，引导至录音详情功能 |
| 录音设备问题 | 「录音笔怎么用」「设备连接失败」 | 不触发，引导至设备帮助 |
| 手动上传录音 | 「上传录音文件」 | 不触发，引导至上传功能 |
| 纯闲聊 | 「今天天气不错」 | 不触发 |

### 语音转文字同音容错（Agent 必做）

用户输入可能来自**语音转文字（ASR）**，存在同音字/近音字错误。Agent 在匹配触发词时**必须做语义容错**，按以下映射表还原用户真实意图：

| 正确关键词 | 常见 ASR 错误（同音/近音） | 容错处理 |
|-----------|--------------------------|---------|
| 录音 | 路音、禄音、录映、录应 | 视为「录音」 |
| 分析 | 分西、份析、粉析、分细 | 视为「分析」 |
| 报告 | 抱告、暴告、豹告 | 视为「报告」 |
| 拜访 | 拜访、拜防、拜饭、拜范 | 视为「拜访」 |
| 总结 | 总接、总节、总洁 | 视为「总结」 |
| 通话 | 通化、通画、通花 | 视为「通话」 |
| 记录 | 记路、记绿、计录 | 视为「记录」 |
| 转写 | 专写、砖写、转些 | 视为「转写」 |
| 批量 | 皮量、批亮、皮批 | 视为「批量」 |
| 数据 | 树据、数具、树据 | 视为「数据」 |
| 报告 | 抱告、暴告 | 视为「报告」 |
| 会话 | 会化、会画、回话 | 视为「会话」 |

**容错原则**：

1. **语义优先**：当用户消息中出现上表中的 ASR 错误，但整体语义可判断为「录音分析/报告」意图时，按正确关键词处理
2. **上下文推断**：即使个别字识别错误，只要句子结构包含「动词 + 对象」模式（如「帮我分西路音」→「帮我分析录音」），应正确识别
3. **不确定时确认**：如果 ASR 错误导致语义模糊无法判断，按中置信度流程向用户确认
4. **不要纠正用户**：在回复中**不要**指出用户的错别字，直接按正确语义执行即可

## LegionClaw 运行约定

- **会话形态**：`agent:<agentid>:<渠道>:<用户 id>`；渠道为空时为三段 `agent:<agentid>:<用户 id>`（无 `::`）。**`userId` 请求体仅填第 2 段 agentid**。
- **执行位置**：`curl` 与生成脚本须在 **LegionClaw 任务运行环境**执行；环境需能访问录音服务（见下文接口）。对用户说明网络问题时用「录音服务」等泛称，**勿**在面向用户的报错中写内网 IP/端口（技能内保留地址供 Agent 调用）。
- **成功判定**：HTTP 2xx 且响应 JSON **`code === 0`**（数值零）且 **`msg` 含 success 语义**；业务数据在 **`data.records`**。
- **零条录音**：`data.records` 为空数组或长度为 **0** 时，**停止后续流程**——**不**生成 HTML、**不**调用 openclaw-file-share / 兜底上传；直接向用户说明统计窗口内无已完成 ASR 的录音，并建议核对 agentid 或调整时间范围。

### 数据真实性约束（严禁违反）

**所有统计数据必须且只能来自本次 API 调用返回的 `data.records`**，严禁以下行为：

| 禁止行为 | 说明 |
|----------|------|
| 使用历史数据 | 不得使用之前会话、之前请求返回的数据 |
| 使用缓存数据 | 不得复用本地缓存文件或内存中的旧数据 |
| 使用测试数据 | 不得使用示例数据、Mock 数据、测试用例数据 |
| 捏造数据 | 不得编造、虚构任何录音内容、转写文本、统计数据 |
| 补充数据 | 不得在 API 返回数据之外添加任何额外内容 |

**每次触发技能必须**：
1. 重新调用 `session_status` 获取 agentid
2. 重新调用 `/api/recordings/asr-completed` 获取录音数据
3. 仅使用本次 API 响应中的 `data.records` 进行分析和统计

**违反后果**：生成的报告将包含虚假数据，误导用户决策，属于严重错误。

### 请求体参数

| 字段 | 必填 | 格式 | 说明 |
|------|------|------|------|
| `userId` | **是** | 字符串 | 取会话标识解析出的 **agentid**（第 2 段） |
| `startTime` | 条件必填 | **`YYYY-MM-DD`** | 统计窗口起始日（含），由用户话术换算；见下文 |
| `endTime` | 条件必填 | **`YYYY-MM-DD`** | 统计窗口结束日（含），通常取**当天**；示例 `2026-05-21` |

- 用户**未明确**查询时间范围：**固定按「近一个月」** 换算并传入 `startTime` / `endTime`（`endTime` = 今天，`startTime` = 今天 − 30 天）。**不要**只传 `userId` 省略时间字段。
- 用户**明确说了**范围（如「近三天」「上周」「4 月 1 日到 4 月 30 日」）：按话术换算为 **`YYYY-MM-DD`**（带 `-`）后传入；**禁止**传 `YYYYMMDD` 无横线格式或中文原文。
- 每次请求应同时包含 **`userId`、`startTime`、`endTime`** 三个字段（除非接口文档后续另有约定）。

```json
{
  "userId": "<agentid>",
  "startTime": "2026-04-21",
  "endTime": "2026-05-21"
}
```

### 从用户话术换算时间（Agent 必做）

在运行环境用**当天日期**作 `endTime`（除非用户明确指定结束日，如「到 5 月 1 日」）。`startTime` = 结束日往前推对应天数或按自然周/月边界计算。

| 用户说法（示例） | startTime | endTime |
|------------------|-----------|---------|
| **未说明时间（默认）** | 今天 − 30 天 | 今天 |
| 近三天 / 最近 3 天 | 今天 − 3 天 | 今天 |
| 近一周 / 最近 7 天 | 今天 − 7 天 | 今天 |
| 近一个月 / 最近 30 天 | 今天 − 30 天 | 今天 |
| 近三个月 | 今天 − 90 天 | 今天 |
| 本月 | 本月 1 日 | 今天 |
| 上周 | 上周一 | 上周日 |
| 指定区间「4 月 1 日到 4 月 30 日」 | `2026-04-01` | `2026-04-30` |

**macOS**（`date -v`）示例——近一个月：

```bash
END_TIME=$(date +%Y-%m-%d)
START_TIME=$(date -v-30d +%Y-%m-%d)
```

**Linux**（`date -d`）示例——近三天：

```bash
END_TIME=$(date +%Y-%m-%d)
START_TIME=$(date -d '3 days ago' +%Y-%m-%d)
```

传参与对用户说明均使用 **`YYYY-MM-DD`**（如 `2026-04-21` 至 `2026-05-21`）。

### 成功响应（示例结构）

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "userId": "<agentid>",
    "orgId": null,
    "startTime": "2026-02-21T10:55:33.284902311",
    "endTime": "2026-05-21T10:55:33.284902311",
    "records": [
      {
        "recordTime": "2026-05-13T10:00:00",
        "transcript": "…ASR 全文…"
      }
    ]
  }
}
```

**`records` 元素字段**（按优先级取转写与时间）：

| 用途 | 尝试字段名 |
|------|------------|
| 转写正文 | `transcript`、`asrText`、`asr_text`、`text`、`content`、`dialogue`、`asrContent` |
| 录音日期 | `recordTime`、`createdAt`、`startTime`、`recordingTime`、`date`、`recordDate`（取 ISO 日期前 10 位 `YYYY-MM-DD`） |

`data.startTime` / `data.endTime` 表示接口统计窗口，用于页眉「统计窗口」文案。

### 失败处理

- **HTTP 非 2xx** 或非 JSON：提示无法访问录音服务，勿回显完整 URL。
- **`code` 非 0**：优先用 `msg` 做简短友好说明；无则固定文案「获取录音数据失败，请联系管理员。」
- **会话标识无效**：重新调用 **`session_status`（`sessionKey="current"`）** 解析 agentid，勿把第 3 段（无渠道时的用户 id）当作 agentid。

## agentId 自动获取（必做 · 直接查当前会话）

**用户未提供 agentid 时，必须先调用宿主「当前会话」查询agentid，再拉数。** 不得在未调用 **步骤 1** 前回复「无法获取 agentId / 请提供会话标识」。对话上下文里的字段**不算**；须以 **session 工具返回值** 为准。

### 禁止行为

| 禁止 | 正确做法 |
|------|----------|
| 首句就向用户索要 agentid 或整串 `agent:...` | **先**调 `session_status`（`sessionKey="current"`）或平台等价「当前会话查询」 |
| 未调会话工具就声称「当前对话没有 agentId」 | 对话里没有是正常的；用 **当前会话查询** 拿 获取当前会话的agentid  |
| 把会话串第 3 段用户 id 当成 agentid | 仅第 2 段，或工具返回的 `agentId` 字段 |
| 向用户展示完整会话串 | 只说明「已根据当前 LegionClaw 会话解析 agentid」 |

### 获取步骤（按序执行）

**步骤 0 — 用户消息已带 agentid**

- 用户明确给出 32 位 agentid（或「agentid 是 xxx」）→ 直接采用，可跳过步骤 1。

**步骤 1 — 当前会话查询（主路径，必须执行）**

在 **LegionClaw / OpenClaw 宿主**上调用内置会话工具（**不要用** `exec` 猜环境变量代替）：

| 项 | 值 |
|----|-----|
| 工具 | `session_status` |
| 参数 | `sessionKey`: **`"current"`**（表示**当前正在对话的会话**） |

**Agent 操作说明（照做）：**

1. 调用 **`session_status`**，传入 **`sessionKey="current"`**。
2. 从返回 JSON / 状态卡中读取（字段名以宿主为准，常见如下）：
   - 若有 **`agentId`** 且非空 → **直接作为 `AGENTID`**（首选）。
   - 否则读取 **`sessionKey`** / **`key`**（完整串，形如 `agent:<agentid>:...`）→ 按下文规则解析第 2 段。
3. 校验 `AGENTID` 非空后，再执行 `curl` 拉数；请求体 **`userId` = agentid**，禁止填入整串 `sessionKey`。

**步骤 1b — 仍缺 agentid 时（可选一次）**

若 `session_status` 未返回可用字段，再调用 **`sessions_list`**（可见性默认 `tree`），取**当前会话对应行**的 `agentId` 或 `key`，同样解析。仍禁止先让用户粘贴。

**步骤 2 — 环境变量兜底（仅步骤 1/1b 失败时）**

```bash
AGENTID=$(printf '%s' "$RAW" | awk -F: '$1=="agent" && NF>=2 && length($2)>0 {print $2; exit}')
```

**步骤 3 — 仍为空（仅此情况可索要）**

```markdown
已调用当前会话查询（session_status current），仍无法解析 agentid。
请确认本任务是否绑定当前 LegionClaw 会话，或直接提供 **agentid**（`agent:` 后第二段，32 位）。
```

### 从 sessionKey 解析 agentid（统一规则）

当工具只返回 `sessionKey` / `key` 时：按 `:` 拆分；`$1=="agent"` 且第 2 段非空 → **agentid = 第 2 段**。

| 会话 key 示例 | agentid |
|---------------|---------|
| `agent:b7a19493cabc42e290c3d6c8a6243a7c:web:user001` | `b7a19493cabc42e290c3d6c8a6243a7c` |
| `agent:b7a19493cabc42e290c3d6c8a6243a7c:user001`（三段） | `b7a19493cabc42e290c3d6c8a6243a7c` |

### 执行前自检

- [ ] 已调用 **`session_status` + `sessionKey="current"`**（或等价当前会话 API）
- [ ] 已从返回的 **`agentId`** 或 **`sessionKey` 第 2 段** 得到非空 `AGENTID`
- [ ] 拉数 body 的 `userId` = agentid，不是整串 sessionKey

## 分析维度

三种模式（互斥，按优先级理解用户意图）：

| 模式 | 何时使用 | 生成方式 |
|------|----------|----------|
| **默认十维** | 用户未限定要看哪些维度 | 不传 `--only` / `--dimensions` |
| **用户选子集** | 用户只要其中几个默认维度，如「只看客户需求、跟进动作」 | `--only`，名称与 [DIMENSIONS.md](DIMENSIONS.md) 表内**完全一致**；报告**仅含**所选维度 |
| **全新自定义** | 用户给出默认表以外的维度名或专属关键词 | `--dimensions` 指向 JSON 文件，**替换**整个维度表 |

**子集示例**：用户说「只看客户需求、跟进动作」→ 只分析 2 维，HTML 里只有这 2 行的统计表、图表与卡片，不要带上其余 8 维。

```bash
python3 skills/ai-coach-batch-session-summary/scripts/generate_asr_insight_html.py \
  -i /tmp/asr_completed.json \
  --only 客户需求 --only 跟进动作 \
  -o "$OUT"
```

名称写错时脚本会报错并列出可选维度；Agent 应先对照 [DIMENSIONS.md](DIMENSIONS.md) 纠正，勿静默跳过用户点名的维度。

### 维度分析规则

- 每条 `records` 转写文本中，若命中某维度任一关键词，则该条录音计为该维度 **命中 1 次**（每条录音每维度最多计 1 次）。
- **覆盖率** = 命中录音数 / 总录音数 × 100%（保留 1 位小数）。
- **典型摘录**：取首个命中关键词所在片段（约 120 字内），摘录标签为命中词。
- **图表**：录音按日计数、各维度覆盖率雷达/柱状、命中数 Top 维度按日折线（与参考 HTML 一致）。

## 执行步骤

1. **【必做】** 调用 **`session_status`（`sessionKey="current"`）** 解析 **AGENTID**（见 [agentId 自动获取](#agentid-自动获取必做--直接查当前会话)）；不得跳过。
2. 根据用户对话换算 **`YYYY-MM-DD`**（见上表）：用户**未明确时间则固定近一个月**；否则按用户说法计算 `START_TIME` / `END_TIME`。
3. 拉取录音数据（注意 JSON 转义；**始终带** `startTime`、`endTime`）：

```bash
END_TIME=$(date +%Y-%m-%d)
# 默认近一个月；若用户指定了其它范围，按上表重算 START_TIME
START_TIME=$(date -v-30d +%Y-%m-%d)   # Linux 默认: date -d '30 days ago' +%Y-%m-%d
# 示例：用户说近三天 → START_TIME=$(date -v-3d +%Y-%m-%d)  # Linux: date -d '3 days ago' +%Y-%m-%d

curl -sS -X POST "http://192.168.96.17:8900/api/recordings/asr-completed" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d "{\"userId\":\"${AGENTID}\",\"startTime\":\"${START_TIME}\",\"endTime\":\"${END_TIME}\"}" \
  -o /tmp/asr_completed.json
```

回复用户时，若使用的是默认窗口，应写明「近一个月（yyyy-mm-dd 至 yyyy-mm-dd）」。

4. 校验 `code` 为 0；读取 `data.records`。
5. **若 `records` 条数为 0**：**到此结束**。友好告知用户（见下「零条录音」回复示例），**不要**执行步骤 6～7（不跑 `generate_asr_insight_html.py`、不上传）。
6. 生成 HTML（**仅当** `records` 非空；**推荐**使用本技能脚本）：

```bash
STAMP=$(date +%Y%m%d_%H%M%S)
OUT="/tmp/asr_insight_${STAMP}.html"
python3 skills/ai-coach-batch-session-summary/scripts/generate_asr_insight_html.py \
  -i /tmp/asr_completed.json \
  -o "$OUT"
```

用户**只选默认维度中的若干项**时（与 `--dimensions` 二选一）：

```bash
python3 skills/ai-coach-batch-session-summary/scripts/generate_asr_insight_html.py \
  -i /tmp/asr_completed.json \
  --only 客户需求 --only 跟进动作 \
  -o "$OUT"
```

用户给出**全新维度**（名称/关键词不在默认十维）时：

```bash
python3 skills/ai-coach-batch-session-summary/scripts/generate_asr_insight_html.py \
  -i /tmp/asr_completed.json \
  --dimensions /tmp/custom_dimensions.json \
  -o "$OUT"
```

脚本路径以仓库根为基准；若工作目录在技能目录内，可使用 `scripts/generate_asr_insight_html.py` 相对路径。脚本在 **0 条录音** 时以退出码 **3** 退出且不写输出文件，Agent 应视为正常短路而非执行失败。

7. **上传 `$OUT` 并生成交付链接**（**仅当** 已生成 HTML；**优先** [openclaw-file-share](../openclaw-file-share/SKILL.md)，不可用再按下文「交付 HTML」兜底）。
8. **回复用户**（Markdown）建议包含：
   - 一句话摘要：样本条数、**实际查询的时间范围**（用户原话 + 换算后的起止日期）、**本次分析的维度名称**（若为用户子集须写明）、有命中维度数 / 本次维度总数；
   - HTML 交付链接须 **可点击预览**（格式见下节，**禁止**仅用行内代码包 URL）。

### 向用户展示链接（可点击预览）

LegionClaw / 对话端对 **`https://...` 行内代码** 通常**不能点击、不能预览**。交付时必须用 **Markdown 超链接** + **裸链**。

| 禁止（不可点击） | 必须（可点击） |
|------------------|----------------|
| `` **`https://...`** `` | `[HTML 洞察报告（点击打开）](https://...)` |
| 链接藏在代码块 ``` 内 | 链接单独成行，前后空行 |
| 只写「下载 HTML：」+ 代码样式 URL | 先超链接，再可选一行裸链 |

**标准模板（每个文件各用一次）**：

```markdown
## 完整报告

- [HTML 洞察报告（十维分析 + 图表，点击打开）](https://chat-minio.tongfudun.com/legionclaw/asr_insight_20260521_103000.html)

https://chat-minio.tongfudun.com/legionclaw/asr_insight_20260521_103000.html
```

- 第一行：**`[描述](URL)`** — 用户点描述即可打开（多数客户端支持预览 HTML）。
- 第二行：**裸 URL**（无反引号、无加粗）— 供自动识别为链接；与上行 URL **必须完全相同**。
- 若另有 Markdown 总结等附件，同样用 `[Markdown 沟通总结](URL)`，**不要**用行内代码包 URL。

**回复示例（默认十维）**：

```markdown
已根据最近统计窗口内 **4** 条 ASR 转写生成十维拓客洞察报告（6/10 个维度有相关表述）。

## 完整报告

- [HTML 洞察报告（十维分析 + 图表，点击打开）](https://chat-minio.tongfudun.com/legionclaw/asr_insight_20260521_103000.html)

https://chat-minio.tongfudun.com/legionclaw/asr_insight_20260521_103000.html
```

**回复示例（用户仅选 2 维）**：

```markdown
已按您选择的 **客户需求、跟进动作** 两个维度，对最近统计窗口内 **4** 条 ASR 转写生成洞察报告（1/2 个维度有相关表述）。

## 完整报告

- [HTML 洞察报告（点击打开）](https://chat-minio.tongfudun.com/legionclaw/asr_insight_20260521_103000.html)

https://chat-minio.tongfudun.com/legionclaw/asr_insight_20260521_103000.html
```

**回复示例（零条录音，不生成 HTML、不上传）**：

```markdown
在 **2026-04-21 至 2026-05-21**（近一个月）内，未查询到已完成 ASR 的录音（0 条），因此未生成洞察报告。

建议您核对当前账号/agentid 是否正确，或尝试扩大时间范围后再试。
```

## 交付 HTML 给用户（文件上传）

**前置条件**：`data.records` **至少 1 条**。为零条时**不适用**本节，勿上传空报告。

本技能产出的 HTML **必须**以公网下载链接交付用户。

### 优先：openclaw-file-share

**默认且首选**：若运行环境**已提供** [openclaw-file-share](../openclaw-file-share/SKILL.md) 技能，Agent **必须先读取并完整遵循**其上传流程；上传得到 URL 后，**对本技能面向用户的最终回复**仍须按 [向用户展示链接（可点击预览）](#向用户展示链接可点击预览) 写成可点击的 `[描述](URL)` + 裸链（不要仅照搬 file-share 的行内代码 URL 样式）。**不要**跳过 file-share 直接走下方兜底，除非已确认该技能不可用。

对本任务，将 `$OUT`（如 `/tmp/asr_insight_${STAMP}.html`）作为待上传的生成文件即可；`objectName` 建议与本地文件名一致（`asr_insight_${STAMP}.html`），并满足 file-share 对 ASCII、无空格、无未展开 `%` 占位符的要求。

**下载链接**（不解析上传响应体中的 URL，按固定格式拼接）：

`https://chat-minio.tongfudun.com/legionclaw/{objectName}`

### 交付前检查清单

- [ ] 已通过 **当前会话查询**（`session_status` current）得到 **AGENTID**
- [ ] `data.records` 非空（为 0 则已提前结束，不进入本清单）
- [ ] HTML 已生成且 `$OUT` 文件存在
- [ ] **已优先尝试** openclaw-file-share；仅在不可用时才走本节兜底上传
- [ ] `objectName` 为 ASCII、无空格、无未展开 `%` 占位符
- [ ] 已 `POST` 上传且 `bucket=legionclaw`
- [ ] 已用 `https://chat-minio.tongfudun.com/legionclaw/{objectName}` 作为用户可见下载地址
- [ ] 最终回复无本地路径；链接为 **Markdown 超链接 + 裸链**，非行内代码 URL

## 变更接口或版式时

若 URL、请求字段、`records` 结构或默认维度变更，请同步更新本文件、[DIMENSIONS.md](DIMENSIONS.md) 与 `scripts/generate_asr_insight_html.py`。
