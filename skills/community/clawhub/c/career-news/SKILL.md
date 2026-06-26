---
name: Career News
description: |
  Daily profession-targeted news from X (Twitter), Google News, Grok, and global media.
  Supports bilingual (zh/en), multi-profession subscriptions, keyword filters, and scheduled morning push.
  Users can subscribe to news from multiple professions beyond their primary one.
keywords:
  - news
  - career
  - profession
  - daily
  - x
  - google
  - grok
  - industry
  - multi-profession
  - subscription
  - morning-brief
  - 职业新闻
  - 早报
  - 行业动态
  - 多职业订阅
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# Career News

Aggregates the most relevant industry news for professionals every morning from **X (Twitter), Google News, Grok, and global media**. Each user receives a concise, high-value brief tailored to their profession(s).

Users can subscribe to news from **multiple professions** — a developer who also wants investor and marketing news gets three separate briefs every morning.

## Supported Professions

| Slug | Chinese | English |
|------|---------|---------|
| `doctor` | 医生/医疗从业者 | Doctor / Healthcare |
| `lawyer` | 律师/法律从业者 | Lawyer / Legal |
| `engineer` | 工程师（泛） | Engineer |
| `developer` | 软件开发者 | Software Developer |
| `designer` | 设计师 | Designer |
| `product-manager` | 产品经理 | Product Manager |
| `investor` | 投资人/金融从业者 | Investor / Finance |
| `teacher` | 教师/教育从业者 | Teacher / Educator |
| `journalist` | 记者/媒体从业者 | Journalist / Media |
| `entrepreneur` | 创业者 | Entrepreneur |
| `researcher` | 研究员/学者 | Researcher |
| `marketing` | 市场营销 | Marketing |
| `hr` | 人力资源 | HR |
| `sales` | 销售 | Sales |

## Scripts

| Script | Function |
|--------|----------|
| `scripts/morning-push.js` | Daily 7:00 AM push — generates one brief per profession per user |
| `scripts/news-query.js` | Instant query for any profession (or all of a user's subscriptions) |
| `scripts/register.js` | Register / view / list users |
| `scripts/manage-professions.js` | Add / remove / list extra profession subscriptions |
| `scripts/push-toggle.js` | Enable / disable push for a user |

## Usage

```bash
# Register a user
node scripts/register.js alice --profession developer --lang zh
node scripts/register.js bob --profession investor --lang en

# Manage multi-profession subscriptions
node scripts/manage-professions.js --userId alice --add investor
node scripts/manage-professions.js --userId alice --add marketing
node scripts/manage-professions.js --userId alice --list
node scripts/manage-professions.js --userId alice --remove marketing
node scripts/manage-professions.js --userId alice --clear        # remove all extras
node scripts/manage-professions.js --suggest alice               # AI suggests new subscriptions

# Instant query
node scripts/news-query.js developer
node scripts/news-query.js investor --lang en --region us
node scripts/news-query.js --userId alice                        # query all of alice's professions
node scripts/news-query.js --userId alice --all-professions

# Trigger push manually
node scripts/morning-push.js
node scripts/morning-push.js --user alice
node scripts/morning-push.js --profession doctor   # override profession

# Toggle push
node scripts/push-toggle.js --userId alice         # toggle on/off
node scripts/push-toggle.js                        # show cron command
```

## Cron Setup

```bash
openclaw cron add "0 7 * * *" "cd /path/to/career-news && node scripts/morning-push.js"
```

## Multi-Profession Subscription

Each user has one **primary profession** and any number of **extra profession subscriptions**:

- Morning push generates **one brief per profession**, primary first
- `manage-professions.js --suggest` asks the AI to recommend complementary professions based on career overlaps, knowledge amplification, and adjacent fields
- Extra subscriptions are preserved when re-registering

Example — a developer who adds investor and marketing:
```
╔══ alice · 今日 3 个职业早报 · 2026年4月4日 ══╗
[Career News | developer ✦ primary | ...]
────────────────────────────────────────────────────────────
[Career News | investor ★ extra subscription | ...]
────────────────────────────────────────────────────────────
[Career News | marketing ★ extra subscription | ...]
╚══ End of alice's 3 briefs. ══╝
```

## News Source Strategy

Push prompts instruct the agent to search in this order:

1. **X (Twitter)** — latest high-engagement posts matching profession keywords
2. **Google News** — past 24 hours in this profession's field
3. **Grok** — AI-synthesized summary of today's top developments
4. **Global media** — Bloomberg, Reuters, TechCrunch, Nature, etc. matched to profession

## User Data Schema

`data/users/<userId>.json`:
```json
{
  "userId": "alice",
  "profession": "developer",
  "extraProfessions": ["investor", "marketing"],
  "language": "zh",
  "region": "cn",
  "keywords": ["AI", "开源"],
  "pushEnabled": true,
  "createdAt": "2026-04-04T00:00:00.000Z",
  "updatedAt": "2026-04-04T00:00:00.000Z"
}
```

---

*Version: 1.1.0 · Updated: 2026-04-04*
