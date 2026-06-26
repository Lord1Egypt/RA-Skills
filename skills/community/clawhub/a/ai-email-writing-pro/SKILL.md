---
name: ai-email-master
description: Professional email writing assistant with tone adjustment, template library, grammar checking, and response suggestions. Supports formal, casual, persuasive, and empathetic tones for business communication.
---

# AI Email Master

Professional email composition assistant that helps you write clear, effective, and impactful emails for any situation.

---

## Features

### ✍️ Smart Composition

- **Tone Adjustment**: Formal, casual, persuasive, empathetic
- **Template Library**: 50+ professional templates
- **Auto-Complete**: Intelligent sentence suggestions
- **Grammar Check**: Error-free writing

### 🎯 Tone Optimization

- **Formal**: Business proposals, official communications
- **Casual**: Team updates, informal messages
- **Persuasive**: Sales emails, negotiations
- **Empathetic**: Apologies, condolences, sensitive topics
- **Urgent**: Time-sensitive requests

### 📧 Email Types

- **Cold Outreach**: First contact emails
- **Follow-Up**: Gentle reminders
- **Meeting Requests**: Scheduling and agendas
- **Status Updates**: Progress reports
- **Thank You**: Appreciation emails
- **Apologies**: Mistake acknowledgments
- **Resignations**: Professional exits
- **Recommendations**: References and endorsements

### 🔍 Quality Checks

- **Clarity Score**: Message clarity rating
- **Conciseness**: Wordiness detection
- **Call-to-Action**: Clear next steps
- **Subject Line**: Open rate optimization
- **Mobile Preview**: Mobile-friendly formatting

---

## Usage

### Basic Email Composition

```javascript
const writer = new EmailWriter();

const email = await writer.compose({
  type: 'meeting-request',
  tone: 'professional',
  recipient: '客户',
  purpose: '预约产品演示会议',
  keyPoints: [
    '介绍新产品功能',
    '演示实际效果',
    '讨论合作方案'
  ],
  preferredTime: '下周一下午或周二上午',
  duration: '30 分钟'
});

console.log(email.subject);
console.log(email.body);
```

### Tone Adjustment

```javascript
// 将邮件从随意改为正式
const formalEmail = await writer.adjustTone({
  originalEmail: casualDraft,
  targetTone: 'formal',
  context: '发送给 CEO 的汇报'
});
```

### Response Generation

```javascript
// 自动生成回复
const reply = await writer.generateReply({
  receivedEmail: incomingEmail,
  intent: 'accept-meeting',
  additionalInfo: {
    availableTime: ['周一下午 2-4 点', '周三上午 10-12 点']
  }
});
```

### Template Selection

```javascript
// 查找合适的模板
const templates = await writer.findTemplates({
  category: 'sales',
  purpose: 'cold-outreach',
  industry: 'technology'
});
```

---

## Email Templates

### Cold Outreach

```
Subject: [公司名] 合作机会 - [你的公司]

尊敬的 [姓名]，

我是 [你的公司] 的 [你的职位] [你的名字]。

我注意到 [对方公司] 在 [领域] 取得了令人瞩目的成就，特别是 [具体成就]。

我们帮助过类似公司 [取得的成果]，例如：
- [案例 1：具体数据]
- [案例 2：具体数据]

不知道您下周是否有 15 分钟时间，我想分享一下我们如何帮助 [对方公司] 实现类似成果。

期待您的回复。

此致
敬礼

[你的名字]
[你的职位]
[联系方式]
```

### Follow-Up

```
Subject: Re: [原主题]

尊敬的 [姓名]，

希望您一切顺利。

我上周发送了关于 [主题] 的邮件，不知道您是否有机会查看？

我知道您很忙，如果您对这个话题感兴趣，我很乐意：
1. 提供更多详细信息
2. 安排一个简短的通话
3. 发送相关案例研究

如果您目前不感兴趣，也请告诉我，我会暂时不再打扰。

感谢您的时间。

此致
敬礼

[你的名字]
```

### Meeting Request

```
Subject: 会议邀请：[会议主题] - [日期]

尊敬的 [姓名]，

希望您这周过得愉快。

我想邀请您参加一个关于 [会议主题] 的会议，具体信息如下：

📅 日期：[建议日期]
⏰ 时间：[建议时间]
📍 地点：[地点/线上会议链接]
⏱️ 时长：[时长]

会议议程：
1. [议程项 1]
2. [议程项 2]
3. [议程项 3]

如果上述时间不合适，请告诉我您方便的时间，我会配合您的日程。

期待您的确认。

此致
敬礼

[你的名字]
```

---

## Subject Line Optimization

### Best Practices

1. **Keep It Short**: 4-7 words optimal
2. **Create Urgency**: Time-sensitive language
3. **Personalize**: Include recipient's name/company
4. **Be Specific**: Clear value proposition
5. **Avoid Spam**: No all-caps or excessive punctuation

### A/B Testing

```javascript
const variants = await writer.generateSubjectLines({
  emailContent: emailBody,
  variations: 5,
  style: 'professional'
});

// 返回 5 个不同的主题行供测试
// 1. 合作机会 - 某某公司
// 2. 某某总，有个想法想和您分享
// 3. 关于 [具体话题] 的讨论邀请
// 4. 下周有空聊聊吗？
// 5. [你的公司] x [对方公司] 合作可能性
```

---

## Grammar & Style Checks

### Common Issues Detected

- **Spelling Errors**: Typos and misspellings
- **Grammar Mistakes**: Subject-verb agreement, tense
- **Punctuation**: Comma placement, apostrophes
- **Wordiness**: Unnecessary words and phrases
- **Passive Voice**: Overuse of passive constructions
- **Jargon**: Overly technical language
- **Tone Inconsistency**: Mixed formality levels

### Suggestions

```javascript
const suggestions = await writer.checkQuality({
  email: draftEmail,
  checks: ['grammar', 'clarity', 'tone', 'conciseness']
});

// 返回：
// {
//   grammar: { score: 95, issues: [...] },
//   clarity: { score: 88, suggestions: [...] },
//   tone: { detected: 'professional', target: 'professional', match: true },
//   conciseness: { wordCount: 150, suggested: 120, reduction: '20%' }
// }
```

---

## Email Analytics

### Track Performance

```javascript
const analytics = await writer.trackPerformance({
  emailId: 'email-123',
  metrics: ['openRate', 'clickRate', 'responseRate']
});

console.log(`打开率：${analytics.openRate}%`);
console.log(`回复率：${analytics.responseRate}%`);
```

### Learn from Data

```javascript
const insights = await writer.getInsights({
  period: 'last-30-days',
  emailType: 'cold-outreach'
});

// 返回：
// - 最佳发送时间
// - 最佳主题行风格
// - 最佳邮件长度
// - 最佳 Call-to-Action
```

---

## Best Practices

### Writing Tips

1. **Start Strong**: Compelling opening sentence
2. **Be Clear**: One main message per email
3. **Keep It Brief**: Get to the point quickly
4. **Use Formatting**: Bullet points, bold text
5. **Include CTA**: Clear next step
6. **Proofread**: Check before sending
7. **Mobile-Friendly**: Short paragraphs
8. **Professional Signature**: Complete contact info

### Response Time

- **Urgent**: Within 1 hour
- **Important**: Within 4 hours
- **Normal**: Within 24 hours
- **Low Priority**: Within 48 hours

### Email Etiquette

1. **Appropriate Greeting**: Match relationship level
2. **Clear Subject**: Reflect email content
3. **Professional Tone**: Avoid slang and emojis
4. **Respect Time**: Keep it concise
5. **Follow Up**: But don't spam

---

## Architecture

```
Email Request
    ↓
Intent Analysis Agent
    ├─ Identify email type
    ├─ Determine tone
    └─ Extract key points
    ↓
Content Generation Agent
    ├─ Select template
    ├─ Generate draft
    └─ Personalize content
    ↓
Quality Check Agent
    ├─ Grammar check
    ├─ Tone verification
    ├─ Clarity score
    └─ CTA optimization
    ↓
Subject Line Generator
    ├─ Generate variants
    ├─ A/B test suggestions
    └─ Spam score check
    ↓
Final Email
    ├─ Formatted content
    ├─ Subject line
    └─ Sending recommendations
```

---

## Installation

```bash
clawhub install ai-email-master
```

---

## License

MIT

---

## Author

AI-Agent

---

## Version

1.1.0

---

## Created

2026-04-02

---

## Updated

2026-04-02 (Enhanced with templates, examples, and best practices)
