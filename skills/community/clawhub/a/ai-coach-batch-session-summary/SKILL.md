---
name: ai-coach-batch-session-summary
description: >-
  录音转写洞察：先 parse-user-intent 反问确认时间与维度，再 fetch 拉数；默认近 1 个月 + 十维；默认报告页面。
  触发：对象词（含教练/coach）+ 动作词，或完整口令，或显式 intent=ai-coach-batch-session-summary。
---

# AI Coach Batch Session Summary

## 目标

拉取 **legion-hardware** 的 ASR 转写并生成报告。**仅依据 `asrText`**，禁止使用 `aiJiaolianResultJson` / `aiSummaryContent` 作为结论依据。

---

## 工作流程（必须按序，禁止跳步）

```text
1. parse-user-intent.mjs     → 解析时间 / 维度 / 交付形态
2. needClarification=true    → 反问用户，结束（禁止执行 fetch）
3. 用户补充或 skipClarification / confirmed* → 再执行 fetch-asr-recordings.mjs
4. 按 reportPlan + themeRelated + outputFormat 生成报告
```

**禁止只跑 `fetch-asr-recordings.mjs` 而不先意图解析**（fetch 内置相同解析，若需反问会直接 `ok:false` 且不拉数）。

### 脚本调用

```bash
# 步骤 1：意图（不拉数）
echo '{"user":"u","model":"openclaw:u123","userMessage":"帮我总结录音"}' | \
  node "{baseDir}/scripts/parse-user-intent.mjs"

# 步骤 2：确认后拉数（token 仅来自 Header / LEGION_AUTH_TOKEN）
export LEGION_AUTH_TOKEN="<JWT>"
echo '{"user":"u","model":"openclaw:u123","userMessage":"总结最近 5 天录音","skipClarification":true}' | \
  node "{baseDir}/scripts/fetch-asr-recordings.mjs"
```

### 默认值（反问后仍不明确，或用户说「按默认」）

| 项 | 默认 | 报告说明 |
|----|------|----------|
| 时间 | 近 **1** 个月 | 「未确认具体时间，已按默认最近 1 个月统计」 |
| 维度 | **十维拓客** | 「因未提取到明确的分析维度信息，已使用默认十维拓客统计框架处理」 |

---

## 反问沟通

`parse-user-intent` / `fetch` 在以下情况 **`needClarification: true`**：

| 信号 | 反问要点 |
|------|----------|
| `timeRange.confidence` = `ambiguous` | 几天 / 几周 / 几个月 |
| `timeRange.confidence` = `missing` | 统计窗口；不答则默认 1 个月 |
| `analysisFocus.confidence` = `ambiguous` | 拓客 / 话术 / 教练 / 客户需求 / 或默认十维 |
| `analysisFocus.confidence` = `missing` | 分析方向；不答则默认十维 |

**跳过反问：**

- 用户话术中「就按默认 / 你看着办 / 用默认」
- body：`skipClarification: true`（网关在用户回复后设置）
- body：`confirmedTime` / `confirmedDimension`（见下）

### 多轮合并 `userMessage`

网关将 **首轮 + 追问回复** 写入同一 body：

```json
{
  "userMessage": "帮我总结录音",
  "followUpMessage": "最近 5 天，按拓客复盘",
  "skipClarification": true
}
```

或拼接为单字段 `userMessage`。脚本会合并 `userMessage` + `query` + `followUpMessage`。

### 网关确认字段（可选）

| 字段 | 示例 | 作用 |
|------|------|------|
| `skipClarification` | `true` | 不再反问，按解析结果或默认拉数 |
| `confirmedTime` | `"default"` 或 `{ "startTime":"...","endTime":"..." }` | 锁定时间窗 |
| `confirmedDimension` | `"default_ten"` / `"ten"` / `"AI 教练"` / `"股票趋势"` | 锁定维度或专题 |

---

## 触发词速查

**激活（其一）：** 对象词 + 动作词；[完整口令](#完整口令)；`intent=ai-coach-batch-session-summary`。

**动作词：** 总结、汇总、归纳、梳理、概括、小结、复盘、盘点、整合、整理、摘要、报告、结论（及英文同义，须配对象词）。

**对象词：**

| 类别 | 中文 | 英文 |
|------|------|------|
| 录音 / 转写 | 录音、转写、ASR | recording, transcript, ASR |
| 拓客 | 拓客、走访、地推 | outreach, field sales |
| 话术 / 客户 | 话术、客户拜访 | pitch, script, customer visit |
| **教练** | 教练、AI 教练、教练反馈、教练点评 | coach, coaching, AI coach, coach feedback |
| 系统 | legion-hardware | legion, hardware |

### 完整口令

- 总结最近 5 天录音
- 十维拓客报告
- 总结一下教练反馈
- AI coach recap for last month

**不触发：** 仅「总结一下」无对象词；**仅**调用 `POST /api/recordings/ai-jiaolian` 且无话术总结类动作词（走 AI 教练单次能力，不走本 skill）。

---

## 入站参数（OpenClaw / 网关）

```json
{
  "user": "OpenClaw 用户标识（必填，映射为 hardware userId）",
  "model": "openclaw:{user}{orgId} 或 openclaw:{user}person",
  "userMessage": "用户原话（必填，可在 metadata）",
  "followUpMessage": "可选，第二轮补充",
  "skipClarification": false,
  "confirmedTime": "default",
  "confirmedDimension": "default_ten",
  "orgId": "可选；网关已从 model 解析时可直传"
}
```

Header：`Authorization: Bearer {JWT}`（**禁止** body.token）

### userId / orgId 取值（`resolve-openclaw-identity.mjs`）

与 tfd-api `AiService` 的 model 组装一致：

| model 形态 | 含义 | hardware 调用 |
|------------|------|-----------------|
| `openclaw:{user}{orgId}` | 组织上下文 | `userId=user`，`orgId` 为去掉前缀 `openclaw:{user}` 后的后缀 |
| `openclaw:{user}person` | 个人上下文 | `userId=user`，**不传 orgId**（或为空） |

规则：

1. **userId** = 请求体字段 **`user`**（兼容 `userId`）。
2. **model 以 `person` 结尾**（不区分大小写）→ 个人模式，**不传 orgId**。
3. **model 非 person** → `orgId = model` 去掉前缀 `openclaw:` + `user` 后的剩余部分。
4. 若 body 已带非空 **`orgId`**（如网关 metadata）→ 优先使用，不再从 model 解析。
5. 若 body 显式 `orgId: ""` → 视为个人模式。

示例（`user=abc`）：

| model | orgId（查询） |
|-------|----------------|
| `openclaw:abc123` | `123` |
| `openclaw:abcperson` | 不传（个人） |
| `openclaw:abc` | 不传（后缀为空） |

---

## 时间规则（`parse-time-range.mjs`）

| 表述 | confidence | 行为 |
|------|------------|------|
| 最近 5 天 / 近 2 个月 | explicit | 按解析查询 |
| 最近 / 近期（无数字） | ambiguous | 先反问 |
| 无时间 | missing | 先反问 |
| 反问后仍无 | default | 近 **1** 个月 |

时区 `Asia/Shanghai`；上限：月 ≤12，天 ≤366。

---

## 维度与报告分支

| 条件 | 输出 |
|------|------|
| 无显式专题（走十维） | 十维拓客报告 + 默认维度说明（若适用） |
| 用户明确「十维 / 默认十维」 | 十维（无需「未提取维度」说明） |
| 显式专题且 `themeRelated=true` | 仅 `## 用户关注：{主题}` |
| 显式专题且 `themeRelated=false` | **仅**：`## 分析结果` → **无相关内容**（禁止十维、禁止编造） |

`themeRelated` 由脚本用 **主题核心词** 匹配 `asrText`（已避免单独「KYC」「趋势」误命中）。

### 样本量

| recordCount | 处理 |
|-------------|------|
| `0` | 十维骨架或专题内写明「样本为空」 |
| `< 5` | 标注「小样本，结论仅供参考」 |
| `> 80`（默认） | 见 stdout `recordsHint`，分析时优先近期并抽样 |

---

## 数据拉取与部署

| 项 | 说明 |
|----|------|
| 默认 baseUrl | `http://192.168.109.50:8900`（`LEGION_HARDWARE_BASE_URL` 可覆盖） |
| 接口 | `GET` 或 `POST` `/api/recordings/asr-completed` + `startTime`/`endTime` |
| **部署** | 须 **新 jar**（POST 支持 body 内时间）；旧版 POST 仅 3 个月固定窗，自定义时间会失效 |

fetch 成功时 stdout 含：`query`、`analysisFocus`、`themeRelated`、`reportPlan`、`outputFormat`、`records[]`。

---

## 交付形态（`outputFormat`）

| mode | 行为 |
|------|------|
| `page`（默认） | 按 `templates/insight-report-page.md` 生成**完整报告页**（Markdown/HTML） |
| `text` | 用户要求「只要文字/不要页面」 |
| `custom` | 用户要求导出/邮件等，**从其要求** |

---

## 十维拓客（默认维度）

1. 拓客场景 2. 触达人群 3. 开口获客话术 4. 客户需求 5. 客户拒绝原因  
6. 有效意向分类 7. 产品匹配 8. 成交阻碍痛点 9. 跟进动作 10. 拓客成效数据  

每维：关键发现 / 典型摘录 / 量化指标 / 优化建议。

---

## 错误与安全

- 缺 `user` / `Authorization` → 不调 hardware；个人模式可无 `orgId`
- `needClarification` 时禁止编造数据
- 勿暴露 token、内网 IP/端口
- `user` / 解析出的 `orgId` 宜与业务身份一致（建议网关校验）

## 检查清单

- [ ] 已跑 `parse-user-intent`；`needClarification` 时已反问且未 fetch
- [ ] 默认时间/维度说明已写入报告（若适用）
- [ ] `themeUnrelated` 时仅输出「无相关内容」
- [ ] 交付形态符合 `outputFormat`
- [ ] 未使用 body.token
- [ ] `user` / `model` 已按规则解析；`person` 模式未传 orgId
