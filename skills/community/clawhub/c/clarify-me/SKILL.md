---
name: clarify-me
description: Analyze user's conversation to identify unclear parts and suggest better questions. Helps users express their problems more clearly.
---

# clarify-me - Conversation Clarification Skill

## Purpose

In conversations between users and LLMs, ambiguity can arise when users don't describe their problems clearly enough, leading to misunderstandings. This skill analyzes the conversation to identify unclear points and provides suggestions to help users ask more precise and effective questions.

## Trigger

User explicitly calls `/clarify-me` or says:
- "clarify-me"
- "帮我整理一下问题"
- "我表达不清楚吗？"
- "怎么更好地提问？"

## How It Works

### 1. Analyze Conversation
Read through the previous conversation history (the last few exchanges).

### 2. Identify Issues
Find problems in user's descriptions:
- Vague terms ("that", "this", "it")
- Missing context (no background, no code, no error message)
- Unclear intent (what exactly they want)
- Assumptions (things AI might not know)

### 3. Provide Suggestions
Output in the same language as the user's question.

## Example

**Conversation:**
- User: "help me fix this code"
- AI: "which code?"
- User: "the one with error"
- AI: "what error?"
- ... (several rounds)
- User: "/clarify-me"

**Analysis Output:**
The output will be in English (same as user's language):

```
🤔 Let me analyze the conversation...

Possible issues:
1. "this code" - which file/function?
2. "the one with error" - can you paste the error message?
3. Missing context - what project is this?

Next time you could ask:
"I'm writing a Python scraper and got
'ConnectionRefusedError: [Errno 111] Connection refused'
error, what could be the cause?"
```

## Output Style

- Friendly and constructive
- Use "🤔" emoji
- Be specific - quote the unclear parts from conversation
- Give concrete suggestions
- Don't make user feel bad - frame it as "here's how to get better answers"

## Configuration

No config file needed. This skill activates when user explicitly calls it.
