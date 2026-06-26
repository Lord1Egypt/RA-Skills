---
name: china-insurance-advisor
description: Thin proxy skill for the remote 中国保险顾问 web chat at whylingxi.cn. Use when the user asks for insurance planning, product recommendation, product comparison, insurance budget allocation, or insurance Q&A. Forward the user's request to the remote insurance advisor, keep multi-turn continuity through session_id, and return its reply with minimal transformation.
---

# China Insurance Advisor

Use this skill as a thin proxy to the remote insurance advisor web chat.

## What this skill does

- Send the user's insurance question to `https://whylingxi.cn/chat`
- Reuse the upstream conversation through returned `session_id`
- Return the upstream reply with minimal editing

## Use this skill for

- 买什么保险
- 配置保险方案
- 对比保险产品
- 按预算做保障规划
- 保险知识问答
- 医疗险、重疾险、意外险、寿险、年金险、养老规划相关问题

## Do not use this skill for

- Non-insurance topics
- Guaranteeing underwriting, claims, or收益结果
- Replacing the remote agent with local product improvisation

## Execution

Single turn:

```bash
python3 skills/china-insurance-advisor/scripts/query_insurance_agent.py --message "<user request>"
```

Multi-turn conversation:

```bash
python3 skills/china-insurance-advisor/scripts/query_insurance_agent.py --session-id demo-user-1 --message "我想给自己配保险"
python3 skills/china-insurance-advisor/scripts/query_insurance_agent.py --session-id demo-user-1 --message "预算10万，从健康到养老都规划一下"
```

Use `--reset-session` to start a fresh upstream conversation.

## Output rules

- Prefer direct passthrough
- Do not summarize unless the user asks
- Preserve upstream tables, product names, prices, and links
- If the remote agent already included risk notes, do not add duplicate notes

## Failure handling

If the remote service fails or times out:

- Tell the user the remote insurance advisor is temporarily unavailable
- Do not fabricate product names, prices, or planning results

## References

- Read `references/integration-notes.md` only when you need endpoint details
