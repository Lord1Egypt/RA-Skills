---
name: ai-course-agent
description: Auto-generates AI education courses from natural language requests in Chinese. Detects patterns like "帮我生成6年级数学分数乘除法的课程" and calls Edustem API to create and return a course link. Uses SkillPay for usage-based billing (1 token per course).
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "env":
          [
            {
              "key": "EDUSTEM_USERNAME",
              "description": "Edustem API username (email)",
              "required": true,
              "secret": true
            },
            {
              "key": "EDUSTEM_PASSWORD",
              "description": "Edustem API password",
              "required": true,
              "secret": true
            }
          ]
      }
  }
---

# AI Course Agent

OpenClaw Skill for auto-generating AI education courses. Detects natural language course generation requests and calls the Edustem API to create ready-to-use course content.

## 💳 Billing & Pricing

This skill uses **SkillPay** for usage-based billing:

- **Rate:** 1 token per course generation
- **Pricing:** 1 USDT = 1000 tokens
- **Minimum deposit:** 8 USDT (8000 tokens = 8000 courses)
- **Payment:** USDT cryptocurrency via SkillPay

When your balance runs out, the skill will return a payment link for top-up.

## Quick Start

```typescript
import { isCourseLessonRequest, processUserMessage } from 'ai-course-agent';

// When user sends a message:
const userId = req.user.sub; // Get user ID from your auth system

if (isCourseLessonRequest(userInput)) {
  const response = await processUserMessage(userInput, userId);
  
  // Success:
  // "✅ 成功为6年级数学《分数乘除法》生成课程！\n\n📚 课程链接: https://..."
  
  // Insufficient balance:
  // "❌ 余额不足 (当前: 0 tokens)\n\n💳 请充值后继续使用: https://skillpay.me/..."
}
```

## Configuration

Set environment variables before use:

### Edustem API (Required)

```bash
export EDUSTEM_USERNAME="your-email@example.com"
export EDUSTEM_PASSWORD="your-password"
```

### SkillPay Billing

**No configuration needed.** SkillPay credentials are hardcoded in the skill and belong to the skill author. Payments are automatically deducted from your SkillPay balance.

## Supported Input Patterns

```
帮我生成6年级数学分数乘除法的课程
帮我创建一个七年级语文从百草园到三味书屋的课程
帮我制作9年级英语日常会话的课程
生成8年级科学地球和宇宙的课程
```

Supports both Arabic (6年级) and Chinese (六年级) numerals for grade levels.

## Supported Subjects

数学 · 语文 · 英语 · 科学 · 历史 · 地理 · 物理 · 化学 · 生物

## Output Format

```
✅ 成功为6年级数学《分数乘除法》生成课程！

📚 课程链接: https://your-api-host/ai-lesson/{lesson_ref}
```

## API Flow

0. `handleBilling(userId)` — Charge user via SkillPay (1 token)
1. `login()` — Authenticate and get JWT token
2. `createLessonPlan()` — Create lesson plan with metadata
3. `acceptLessonPlan()` — Confirm and trigger course generation
4. Return course URL (or payment link if balance insufficient)

## Exports

```typescript
// Main integration functions
isCourseLessonRequest(message: string): boolean
processUserMessage(userInput: string, userId: string): Promise<string>

// Core functions
generateCourse(request: CourseRequest, userId: string): Promise<GeneratedCourseResponse>
parseCourseRequest(userInput: string): CourseRequest | null

// SkillPay Billing
handleBilling(userId: string): Promise<BillingResult>
chargeUser(userId: string, amount?: number): Promise<ChargeResult>
getBalance(userId: string): Promise<number>
getPaymentLink(userId: string, amount?: number): Promise<string>

// Edustem API (lower level)
login(username, password): Promise<string>
createLessonPlan(token, payload): Promise<CreateLessonPlanResponse>
acceptLessonPlan(token, lessonRef): Promise<AcceptLessonPlanResponse>
generateLessonUrl(lessonRef): string
```

## Tech Stack

TypeScript · Node.js · axios · form-data
