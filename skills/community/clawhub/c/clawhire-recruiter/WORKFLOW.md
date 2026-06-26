# Workflows

**IMPORTANT: You are a proxy, not the interviewer.**

When collecting job info or chatting about hiring needs, you do NOT generate questions yourself. Instead, you forward your owner's messages to the ClawHire server (`/api/v1/chat/intake`), and the server returns AI-generated responses in `content_list`. Your job is to relay those responses back to your owner word-for-word, then forward their reply back to the server. Think of yourself as a messenger between your owner and the ClawHire AI — do not add, remove, or rephrase the server's messages.

---

## 1. Post a new job (main flow)

When your owner mentions hiring, follow these steps.

### Step 1 — Start the intake conversation

```
POST /api/v1/chat/intake
{ "user_input": "<what your owner said>" }
```

The backend derives the session ID from the account — don't send one.

Response:
```json
{
  "content_list": ["好的！  请问贵公司全称是什么？"],
  "agent_type": "a2b",
  "jd_state": { "company_name": "", "job_title": "", "responsibilities": "", ... },
  "phase": "collecting",
  "missing_fields": ["company_name", "job_title", "responsibilities", "skill_requirements", "work_city", "salary"]
}
```

**Say exactly what `content_list` contains to your owner.** Each item is a separate message bubble.

### Step 2 — Keep going

Every time your owner replies:

```
POST /api/v1/chat/intake
{ "user_input": "<their reply>" }
```

Relay each item in `content_list` as a separate message. Watch:
- `phase` — `"collecting"` = still asking, `"confirming"` = has everything, `"published"` = done
- `missing_fields` — what's still needed
- `jd_state` — the structured JD being built

### Step 3 — When phase becomes "confirming"

The AI will present a summary. Show it to your owner and wait for confirmation.

### Step 4 — Publish to ClawHire

When `phase` becomes `"published"` or `action` is `"published"`, post the job using `jd_state` fields directly:

```
POST /api/v1/jobs
{
  "title": "<jd_state.job_title>",
  "company_name": "<jd_state.company_name>",
  "city": "<jd_state.work_city>",
  "salary": "<jd_state.salary>",
  "responsibilities": "<jd_state.responsibilities>",
  "skill_requirements": "<jd_state.skill_requirements>",
  "company_business": "<jd_state.company_business>",
  "educational_requirements": "<jd_state.educational_requirements>",
  "experience_requirements": "<jd_state.experience_requirements>",
  "other_requirements": "<jd_state.other_requirements>",
  "headcount": <jd_state.headcount or 1>,
  "work_schedule": "<jd_state.work_schedule>",
  "benefits": "<jd_state.benefits>",
  "delivery_method": "<jd_state.delivery_method>",
  "description_raw": "<jd_state.responsibilities>"
}
```

Note: some fields may be arrays — join them with newlines before sending.

Tell your owner: "✅ 已发布。有匹配时我会通知你。"

### Step 5 — Check matches

```
GET /api/v1/jobs/<job_id>/matches
```

Show S and A level matches:
```
🎯 Java高级开发 — 2个匹配

1. S级 92分 — Java 5年, 深圳 (AI评估)
   优势: Java技术栈完美匹配
2. A级 85分 — Java 3年, 广州 (AI评估)
   差距: 经验略低(minor)

要我发起对话吗？
```

---

## 2. List jobs

```
GET /api/v1/jobs?status=active&page=1&per_page=20
```

## 3. Update a job

```
PATCH /api/v1/jobs/<id>
{ "status": "paused" }
```

## 4. Delete a job

Confirm with owner first:
```
DELETE /api/v1/jobs/<id>
```

## 5. Check notifications (do this first every session)

**Always check this when your owner starts a new session.** Give them a brief summary of what happened.

```
GET /api/v1/notifications?unread=true
```

Aggregate by type and present a brief summary — do NOT list every notification individually:
```
📬 动态概览:
- 5 个新匹配候选人
- 3 位候选人主动申请了你的岗位
- 12 条新消息（请到网页「对话」页查看详情）
- 1 个候选人被拒绝
```

**Conversation details are NOT your job.** Tell your owner to go to the 「对话」 tab on the website to read and reply to messages. You only report the counts.

Mark all as read:
```
POST /api/v1/notifications/read-all
```

---

## 6. Search candidates

```
GET /api/v1/candidates/search?skills=Java&city=深圳&min_exp=3&page=1&per_page=20
```

Search is case-insensitive. Only returns activated candidates. Sensitive info (name, phone) is hidden.

## 7. Account info

```
GET /api/v1/account
```
