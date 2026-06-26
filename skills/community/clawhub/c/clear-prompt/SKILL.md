# Clear Prompt Engineering

A skill that transforms vague prompts into precise, actionable instructions using 5 core principles.

## When to Use

Use this skill when the user's message is ambiguous, too broad, or lacks necessary context. Apply it proactively before responding to help users craft better prompts.

## 5 Core Principles

1. **明确任务目标**: Say what to do directly, no ambiguity
2. **补充场景背景**: Provide usage context and prerequisites
3. **明确输出要求**: Specify format, length, and purpose
4. **提供关键信息**: Attach necessary data and details
5. **排除无关选项**: State what NOT to do (reduces ambiguity)

## Template

Structure every prompt as:
```
【场景背景】+【已有信息】+【任务目标】+【输出要求】
```

## Response Behavior

When you receive a vague prompt, instead of guessing:
1. Identify which principles are missing
2. Provide a before/after example showing the improvement
3. Suggest a refined version the user can confirm

## Quick Templates

### Config tasks
"I'm on 【OS】, already have 【credential】, please give me CLI commands to 【action】, ready to copy-paste"

### Publish tasks  
"I want to publish 【skill type】 to 【platform/org】, named 【name】, give me complete steps + prerequisites"

### Debugging
"Running 【command】 got error 【error message】, already have 【conditions】, excluding 【known issues】, help troubleshoot"

### Writing
"Write 【doc type】, highlighting 【key strengths】, must be 【style】, under 【length】 words"

## Usage

This skill activates automatically when detecting vague input. No manual trigger needed.
