---
name: douyin-comment-auto-reply
description: Douyin comment operations workflow for your own account videos. Use when the user wants to collect, classify, draft, review, or semi-automate replies to comments under their own Douyin videos. Supports comment intent analysis, bilingual or Chinese-first reply drafting, objection handling, lead filtering, escalation rules, and reply SOP design. Also use when the user wants to build or improve a reusable Douyin comment reply process instead of answering comments one by one.
---

# Douyin Comment Auto Reply / 抖音评论自动回复

Use this skill to turn messy Douyin comment handling into a repeatable operating workflow.

Recommended display name: **Douyin Comment Auto Reply / 抖音评论自动回复**.

Default goal:
- reply faster
- keep tone consistent
- filter leads from noise
- reduce manual repetition

Default scope:
- **your own Douyin account / your own video comments**
- not mass spam
- not fake engagement

## Core workflow

Follow this sequence unless the user asks for only one piece.

1. **Clarify the business context**
   Identify:
   - account type
   - content niche
   - offer or product
   - target audience
   - desired tone
   - whether replies are draft-only, review-first, or auto-send

2. **Choose the operating mode**
   - **Draft mode**: produce reply drafts only
   - **Review mode**: classify comments and draft priority replies
   - **Semi-auto mode**: generate replies plus execution checklist
   - **Playbook mode**: build reusable SOP, intent tags, reply library

3. **Classify comments before replying**
   Tag each comment into one primary bucket:
   - 咨询 / inquiry
   - 成交意向 / buying intent
   - 价格异议 / price objection
   - 质疑 / skepticism
   - 催更 / engagement
   - 售后 / support
   - 无效 / noise or troll

4. **Generate replies by bucket**
   Return short, natural, platform-native replies.
   Prefer one-line or two-line answers.
   Keep the reply feeling human, not robotic.

5. **Escalate when needed**
   Recommend manual handling when comments involve:
   - refunds or disputes
   - sensitive policy topics
   - legal risk
   - obvious harassment
   - high-value leads needing custom conversion

## Reply rules

### General style

- sound like the creator or brand account, not customer support boilerplate
- keep replies short
- avoid over-explaining in public comment threads
- move high-intent leads toward DM or next action when appropriate
- do not argue with trolls unless the user explicitly wants a public stance

### Good reply patterns

Use these patterns often:

- **轻回应**: acknowledge + short answer
- **引导私信**: answer briefly + move to DM
- **社交放大**: turn praise into momentum
- **异议拆解**: soften objection + give one concrete clarification
- **筛选客户**: invite only relevant users to continue

### Avoid

- long essay replies
- emotionally defensive tone
- promises you cannot fulfill
- copy-paste repetition across every comment
- suspiciously identical AI-style replies

## Recommended output format

### 1. 账号与目标 / Account Context
- Niche:
- Offer:
- Tone:
- Reply mode:

### 2. 评论分类 / Comment Classification
For each comment:
- Comment:
- Intent tag:
- Priority: high / medium / low
- Suggested action:

### 3. 回复建议 / Reply Suggestions
- Public reply:
- Optional DM follow-up:
- Why this works:

### 4. 规则与SOP / Rules and SOP
- Safe to auto-reply:
- Must review manually:
- Keywords to escalate:
- Conversion triggers:

## Lead-handling guidance

When comments show buying intent, prefer this public flow:
1. answer one key concern
2. keep trust high
3. invite next step privately or via clear CTA

For example:
- 想了解具体方案可以私信我，我把适合你的版本发你。
- If you want the detailed version, DM me and I’ll send the suitable option.

## Use with batches

When the user provides many comments, do not answer blindly one by one first.

Instead:
1. cluster similar comments
2. produce reusable reply patterns
3. then draft per-comment variants only where needed

## Safety guardrails

- do not facilitate harassment, brigading, or spam
- do not impersonate a real human user outside the owner account voice
- do not fake testimonials or fabricated customer experience
- do not auto-reply to sensitive disputes without review
- clearly separate public reply copy from DM conversion copy

## Batch processing script

Use `scripts/batch_comment_drafts.py` when the user provides exported comments in CSV form.

Expected CSV columns:
- `comment`
- `video_topic` (optional)
- `intent_hint` (optional)
- `priority_hint` (optional)
- `notes` (optional)

Run:

```bash
python3 scripts/batch_comment_drafts.py ./comments.csv
python3 scripts/batch_comment_drafts.py ./comments.csv ./comments.drafts.json
```

The script outputs one JSON item per comment with:
- detected intent
- priority
- suggested action
- public reply draft
- optional DM follow-up draft

## Browser execution script

Use `scripts/browser_reply_runner.py` when the user wants browser-based execution against the Douyin comment management page.

Recommended workflow:
1. Generate draft JSON first.
2. Open Douyin comment management page and identify stable selectors for the reply box and submit button.
3. Run the browser execution script in `--dry-run` first.
4. Only then run the real send flow.

Example:

```bash
python3 scripts/browser_reply_runner.py ./comments.drafts.json \
  --url "https://creator.douyin.com/creator-micro/content/manage" \
  --reply-box-selector "textarea" \
  --submit-selector "button[type=submit]" \
  --dry-run
```

Then real send:

```bash
python3 scripts/browser_reply_runner.py ./comments.drafts.json \
  --url "https://creator.douyin.com/creator-micro/content/manage" \
  --reply-box-selector "textarea" \
  --submit-selector "button[type=submit]"
```

This executor defaults to `npx -y agent-browser`, so it can work even if `agent-browser` is not installed globally yet.

## References

Read `references/playbook.md` for comment buckets, reply templates, escalation rules, and automation design notes.

Read `references/douyin-lead-gen-template.md` when the user is using Douyin comments to convert AI services, training, deployment, consulting, or other lead-gen offers.

Read `references/automation-roadmap.md` when the user wants to move from draft generation into semi-automatic or controlled automatic execution.
