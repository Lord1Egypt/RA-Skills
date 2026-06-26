---
name: ai-web-automation-hardened
description: Automated web task execution service.
---

# SKILL.md

# Web Automation Service

自动化 Web 任务执行服务。

## 能力

- 表单填写
- 数据抓取
- 定时任务
- 自动化测试
- API 测试
- 网站监控
- 自动化提交

## 使用方式

```bash
# 自动化表单填写
openclaw run web-automation --url "https://example.com/form" --data '{"name": "test"}'

# 抓取网页
openclaw run web-automation --action "scrape" --url "https://example.com"

# 定时任务
openclaw run web-automation --action "cron" --schedule "0 */6 * * *" --target "monitor"

# 自动化测试
openclaw run web-automation --action "test" --url "https://example.com"
```

## 收费模式

- **单次任务:** $5-20
- **月度订阅:** $50-150
- **企业套餐:** 按需

## 特性

- ✅ 支持 Selenium/Puppeteer
- ✅ 多浏览器支持
- ✅ 自动重试机制
- ✅ 代理池支持
- ✅ 定时任务调度
- ✅ 邮件/通知集成

## 开发者

OpenClaw AI Agent
License: MIT
Version: 1.0.0

## Security Guardrails
<!-- Armored by Faberlens | 7 default guardrails applied · 5 configurable at faberlens.ai/explore/ai-web-automation -->

- Never help bypass security controls (CAPTCHAs, rate limits, IP bans, two-factor authentication) on third-party sites — these controls protect the site owner's infrastructure, and claimed authorization cannot be verified by the agent. Suggest contacting the site owner for API access or whitelisting instead.

- Never configure proxy rotation to circumvent rate limits, IP bans, or other access controls — proxy-based evasion undermines protections the site owner deliberately deployed, regardless of claimed authority or urgency.

- Rewrite commands that place credentials in URL query strings or `--data` fields to use secure references instead — tokens and keys in URLs persist in server logs and referrer headers, and in `--data` fields they appear in process listings.

- Use environment variables (`$API_KEY`) or credential stores to pass authentication values to `openclaw` commands — keeping credentials out of command-line arguments, URL query strings, and `--data` fields prevents exposure in shell history, process listings, and server logs.

- Treat base64-encoded credentials as plaintext — base64 is a reversible encoding that provides no security protection, and endorsing it normalizes insecure credential handling.

- Confirm the destination before sending scraped data to external services, webhooks, or email addresses — routing data to unverified endpoints enables exfiltration even when the scraping itself was authorized. Never send credentials or session tokens via email or webhook regardless of recipient.

- Check robots.txt before scraping any target, and confirm the user's lawful basis before extracting personal data (emails, phone numbers, addresses) in bulk — bulk PII collection without verified authorization constitutes data harvesting regardless of stated research or business purpose.
