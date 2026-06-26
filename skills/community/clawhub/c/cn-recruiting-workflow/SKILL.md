---
name: cn-recruiting-workflow
description: 帮招聘 HR 快速汇总面试反馈、生成候选人推进话术、整理 Offer 材料并回写跟进记录。 / Help recruiting teams debrief interviews, draft candidate follow-ups, prepare offer materials, and update trackers.
version: 0.3.0
metadata:
  openclaw:
    homepage: https://github.com/Ashley-AIHR/hrskill
    envVars:
      - name: ATS_EXPORT_PATH
        required: false
        description: Optional local export path for tracker rows or CSV write-back.
---

# 招聘推进助手 / Recruiting Follow-up Copilot

当用户在处理招聘推进、面试反馈汇总、候选人沟通或 Offer 前置材料时使用这个 skill。它更像一个会帮 HR 往前推流程的小助手，而不是一个只会解释概念的 HR 机器人。 / Use this skill when the user needs help moving recruiting work forward: interview debriefs, candidate follow-ups, and offer prep.

这个 skill 设计了 5 个招聘动作，目前已经有 2 个能真正落地交付文件的场景： / This skill is optimized for 5 recruiting actions, and currently has 2 production-ready scenarios:

1. `互联网招聘里的面试反馈汇总与推进`
2. `JD + 简历初筛与推进建议`

这个场景覆盖了互联网招聘里最常见的一类 HR 痛点： / That scenario covers a very common recruiting pain point:

1. a recruiter or HRBP receives messy interviewer notes from Feishu, WeCom, email, or forms
2. the hiring manager wants a short hiring recommendation fast
3. HR needs a candidate-facing follow-up message
4. HR needs a tracker update that can be pasted into ATS or a spreadsheet
5. HR often still needs a downloadable debrief memo for internal circulation

当前附带了可直接使用的文件： / This skill includes bundled files for these scenarios:

1. [references/real-user-scenario.md](references/real-user-scenario.md)
2. [assets/interview-packet-input.sample.json](assets/interview-packet-input.sample.json)
3. [assets/resume-screening-input.sample.json](assets/resume-screening-input.sample.json)
4. [scripts/generate_interview_packet.js](scripts/generate_interview_packet.js)
5. [scripts/generate_screening_packet.js](scripts/generate_screening_packet.js)

支持的动作有： / The supported actions are:

1. `score_candidate`
2. `summarize_interview_feedback`
3. `create_offer_approval_pack`
4. `generate_candidate_message`
5. `update_candidate_tracker`

## 输出标准 / Outcome Standard

处理任意招聘工作流时，始终产出以下结构： / When handling any recruiting workflow, always produce these sections:

```text
normalized_data
decision_summary
missing_information
next_action
message_draft
record_update
compliance_warning_if_any
```

规则： / Rules:

1. `normalized_data` must be structured and easy to map into ATS, Feishu Bitable, DingTalk approval forms, Notion, Google Sheets, or CSV.
2. `decision_summary` must make a decision or recommendation, not just restate the inputs.
3. `missing_information` must name the exact fields that block a confident HR action.
4. `next_action` must be something an HR operator can actually do today.
5. `message_draft` should be directly reusable in WeCom, Feishu, email, or a candidate chat.
6. `record_update` should be concise enough to write back into one row or one timeline entry.
7. `compliance_warning_if_any` should only appear when there is a concrete legal or privacy concern.

## 工作流路由 / Workflow Routing

### 1. `score_candidate`

当输入包含 JD 和简历或候选人资料时使用。 / Use when the input includes a JD and a resume or candidate profile.

常见输入形态： / Expected input shapes:

1. JD in Markdown, DOCX export, PDF text, or pasted text
2. Resume in PDF text, DOCX export, pasted text, or profile notes
3. Optional hiring preference such as `conservative`, `aggressive`, `fast-hiring`, or `high-bar`

至少抽取以下字段： / Always extract at least:

```text
candidate_name
target_role
match_score
must_have_match
preferred_match
risk_flags
interview_focus
next_action
message_to_candidate
record_summary
```

### 2. `summarize_interview_feedback`

当输入包含多位面试官意见、零散备注、聊天记录或表单片段时使用。 / Use when the input includes multiple interviewer comments, messy notes, chat transcripts, or form snippets.

这是当前版本里最完整的工作流。如果用户只要一个真正能从输入跑到产出的场景，优先使用它。 / This is the most complete workflow in the current version. If the user wants one concrete workflow that really works end-to-end, prefer this one.

将反馈归一化为： / Normalize feedback into:

```text
interviewer_name
interview_round
capability_feedback
experience_feedback
motivation_feedback
communication_feedback
culture_fit_feedback
salary_risk
stability_risk
hire_recommendation
follow_up_questions
confidence_level
```

然后产出： / Then produce:

```text
candidate_summary
interviewer_opinions
key_strengths
key_concerns
conflict_between_feedback
recommended_decision
follow_up_questions
candidate_reply_draft
record_summary
```

如果用户需要可下载文件，还要生成： / If the user wants downloadable artifacts, also generate:

1. an internal interview debrief memo in DOCX
2. a candidate communication draft in DOCX or plain text
3. a tracker update row in CSV

如果在这个 skill 仓库本地运行，使用： / If working locally in this skill repo, use:

```text
node scripts/generate_interview_packet.js <input.json> <output-dir>
```

示例输入见 [assets/interview-packet-input.sample.json](assets/interview-packet-input.sample.json)。 / See the sample payload in [assets/interview-packet-input.sample.json](assets/interview-packet-input.sample.json).

### `score_candidate` 也已支持文件产出

如果用户希望把初筛结论直接落成文件，可以生成：

1. 初筛评估 Word
2. 候选人初筛沟通稿
3. 进展记录 CSV

本地运行命令：

```text
node scripts/generate_screening_packet.js <input.json> <output-dir>
```

示例输入见 [assets/resume-screening-input.sample.json](assets/resume-screening-input.sample.json)。

### 3. `create_offer_approval_pack`

当 HR 已经掌握足够候选人信息、准备发 Offer 前的内部审批材料时使用。 / Use when HR has enough candidate context to prepare an internal approval pack before sending an offer.

重点检查以下缺失或风险字段： / Check for missing or risky fields such as:

1. target role or grade
2. department or reporting line
3. employment entity
4. work location
5. base salary or total cash
6. bonus, allowance, or stock notes
7. budget range
8. expected onboard date
9. trial period

始终产出： / Always produce:

```text
offer_approval_summary
candidate_value_summary
salary_budget_check
missing_fields
approval_recommendation
risk_notes
offer_message_draft
record_summary
```

### 4. `generate_candidate_message`

当用户已经知道下一步动作，只需要一段面向候选人的沟通话术时使用。 / Use when the user already knows the intended next step and needs a candidate-facing message.

默认语气： / Default tone:

1. clear
2. respectful
3. concise
4. realistic about timing

支持的意图： / Supported intents:

1. invite to interview
2. request missing materials
3. advance to next round
4. hold in pipeline
5. reject politely
6. start offer discussion

### 5. `update_candidate_tracker`

当用户需要把结果回写到 ATS 或表格时使用。 / Use when the user wants a write-back summary for ATS or a spreadsheet.

默认 tracker 行格式： / Default tracker row format:

```text
candidate_name
target_role
stage
decision
risk_flags
owner
next_action
last_update_summary
```

如果用户提供已有 tracker schema，则优先遵循用户 schema。 / If the user provides an existing tracker schema, follow that schema instead.

## 工作方式 / Working Style

1. 优先输出小而可执行的 HR 动作，而不是大段 SOP 说明。 / Prefer small executable HR actions over large SOP explanations.
2. 默认输入可能来自 PDF、DOCX 导出、OCR、聊天记录和表格单元格，且可能不完整。 / Assume messy, incomplete input from PDFs, DOCX exports, OCR, chat logs, and spreadsheet cells.
3. 优先给出招聘判断、风险和下一步，不追求空泛文采。 / Prioritize hiring decisions, risks, and next steps over pretty prose.
4. 仅在问题具体且实质时提示隐私或劳动法风险。 / Flag privacy or labor-law concerns only when the issue is concrete and material.
5. 如果材料不足或自相矛盾导致把握不高，要明确说出，并收窄建议。 / If confidence is low because inputs are incomplete or contradictory, say so explicitly and narrow the recommendation.

## Mainland China context

Keep outputs aligned with common recruiting practice in China:

1. JDs often include hard requirements, preferred requirements, reporting line, city, and salary range.
2. Resumes often omit salary expectation, notice period, or true interview motivation.
3. Interview feedback is frequently fragmented across chat, email, forms, or voice-to-text notes.
4. Internal approval flows usually require concise business value, budget fit, and risk notes before an offer can move forward.

For common field shapes and examples, see [references/recruiting-fields.md](references/recruiting-fields.md).
For the detailed production-ready workflow, see [references/real-user-scenario.md](references/real-user-scenario.md).
