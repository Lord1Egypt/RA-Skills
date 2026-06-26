---
name: creator-scraper-cv
description: |
  Creativault creator data collection and outreach skill. Search and collect creator/influencer
  data from TikTok, YouTube, Instagram, and Twitter. Send outreach emails to discovered creators with
  automatic conversation management, batch sending, and follow-up tracking.
  Supports multi-dimensional search, similar/lookalike creator discovery, batch collection by
  links/usernames/keywords, task tracking, data export (xlsx/csv/html), and email outreach
  (single/batch send, templates, smart timing, metrics).
  Use when: creator search, influencer scraping, KOL search, KOL analytics,
  social media data extraction, TikTok scraper, YouTube scraper, Instagram scraper, Twitter scraper,
  influencer discovery, similar creators, lookalike, outreach, email outreach,
  send email to creator, batch email, follow-up, 达人采集, KOL 搜索, 网红数据,
  达人分析, 达人搜索, 相似达人, 社交媒体数据, 建联, 发邮件, 批量发送.
compatibility: Node.js 20.6+
metadata:
  author: creativault
  version: "1.8.0"
---

# Creativault Creator Ecosystem

## 生态总览

| 领域 | 子 Skill | 能力描述 |
|------|----------|----------|
| discovery | creator-search | 三平台达人多维度实时搜索 |
| discovery | creator-lookalike | 种子达人相似匹配与跨平台发现 |
| collection | creator-collection | 批量异步采集与多格式导出 |
| outreach | creator-outreach | 邮件建联全流程（代发、跟进、待办） |
| workflow | workflow | 剧本式工作流编排与 AI 自主调度 |

## 路由索引

| 子 Skill | 中文关键词 | 英文关键词 | 路径 |
|----------|-----------|-----------|------|
| creator-search | 达人搜索, KOL搜索, 找达人 | creator search, influencer discovery, search creators | discovery/creator-search/SKILL.md |
| creator-lookalike | 相似达人, 类似达人 | similar creators, lookalike, find similar | discovery/creator-lookalike/SKILL.md |
| creator-collection | 批量采集, 数据导出, 离线采集 | batch collection, data export, keyword collection | collection/creator-collection/SKILL.md |
| creator-outreach | 建联, 发邮件, 批量发送 | email outreach, send email, outreach | outreach/creator-outreach/SKILL.md |
| workflow | 工作流, 流程编排, 批量建联流程 | workflow orchestration, campaign flow, batch outreach flow | workflow/SKILL.md |

**路由规则**：AI Agent 根据用户意图匹配上表关键词，加载对应子 skill。无法匹配时展示本表供用户选择。

## Prerequisites

Optional update variables:

- `CV_SKILL_UPDATE_MANIFEST_URL` - Remote manifest URL for skill update checks.
- `CV_SKILL_AUTO_UPDATE=true` - Allow automatic update when the API reports this skill is outdated.

Manual check:

```bash
node scripts/skill_update.mjs --check
```

Confirmed update:

```bash
node scripts/skill_update.mjs --yes
```

Generate release manifest:

```bash
node scripts/generate_manifest.mjs --note "Describe this release"
```

Set the following environment variables:

- `CV_API_KEY` — Creativault Open API Key (obtain from admin dashboard)
- `CV_USER_IDENTITY` — Operator email address
- `CV_API_BASE_URL` (optional) — API base URL, defaults to `http://api.creativault.vip`

**Linux / macOS**:

```bash
export CV_API_KEY=cv_live_your_key_here
export CV_USER_IDENTITY=your_email@example.com
```

**Windows PowerShell**:

```powershell
$env:CV_API_KEY = "cv_live_your_key_here"
$env:CV_USER_IDENTITY = "your_email@example.com"
```

## Error Handling

| Code | Description | Action |
|------|-------------|--------|
| 40001 | Invalid parameters | Check parameter format |
| 40101 | Invalid API Key | Check CV_API_KEY |
| 40102 | API Key expired | Contact admin |
| 40201 | Insufficient credits | Top up or upgrade |
| 40301 | No permission | Check API Key scopes |
| 42901 | Rate limit exceeded | Auto-retry after Retry-After |
| 42902 | Daily quota exhausted | Wait until UTC 00:00 |
| 50001 | Server error | Report request_id to support |

## 积分余额判断规则

**只有 OpenAPI 明确返回错误码 `40201` 时，才能提示用户“积分不足”。**

- `meta.quota_remaining` 表示当天剩余 API 请求次数，不是积分余额。即使该值为 `0`、`8` 或其他较小数字，也禁止解释为“剩余积分”或提示充值。
- `meta.credits_remaining` 才表示真实 OpenAPI 积分余额；字段缺失或值为 `-1` 时，不要自行估算余额。
- `meta.credits_consumed` 只表示本次请求消耗的积分。
- 请求成功时，不要因为任何 quota 数值主动发布“积分余额不足提醒”。
- 只有收到 `40201` 后，才停止后续付费调用并提示用户充值或调整任务规模。

## 版本更新提示规则

当 API 响应 `meta` 中 `skill_update_available: true` 时，需要提示用户更新：

> ⚠️ **Skill 有新版本可用**
> 当前版本：{skill_current_version} → 最新版本：{skill_latest_version}
> 更新命令：`node scripts/skill_update.mjs --yes`
> 新版本可能包含字段修正、行业映射优化或新平台支持，建议尽快更新。

规则：
- `skill_update_available: true` 且 `skill_update_required: false` → 建议更新（非强制），展示提示但不阻断操作
- `skill_update_required: true` → 强制更新提示，告知用户当前版本低于最低支持版本，继续使用可能导致参数不兼容或结果异常
- `skill_update_available: false` → 不提示，已是最新
- 所有 `skill_*` 字段为 null → 不提示（Postman 等非 skill 客户端调用）

## References

- [API Reference](references/api-reference.md)
- [Platform Parameters](references/platform-params.md)
- [Industry Categories](references/industry-categories.md)
- [Country Codes](references/country-codes.md)
- [Language Codes](references/language-codes.md)
- [Error Codes](references/error-codes.md)
