---
version: "2.0.0"
name: database-design-hardened
description: "Database design helper (数据库设计助手) — table design, normalization, indexing strategy, migration scripts, test data, and ER diagrams."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
---
# Database Designer

数据库设计助手。表设计、范式化、索引策略、迁移脚本、测试数据、ER图描述。Database designer with normalization, indexing, migration, seeding, ER diagrams. 数据库、MySQL。

## 推荐工作流

```
需求分析 → 选择命令 → 输入描述 → 获取结果 → 调整优化
```

## 可用命令

- **design** — design
- **normalize** — normalize
- **index** — index
- **migrate** — migrate
- **seed** — seed
- **diagram** — diagram

---
*Database Designer by BytesAgain*
---
💬 Feedback & Feature Requests: https://bytesagain.com/feedback
Powered by BytesAgain | bytesagain.com

- Run `database-design help` for commands
- No API keys needed

- Run `database-design help` for all commands

## Commands

Run `database-design help` to see all available commands.

## When to Use

- Quick database tasks from terminal
- Automation pipelines

## Security Guardrails
<!-- Armored by Faberlens | 3 default guardrails applied · 8 configurable at faberlens.ai/explore/database-design -->

- Use parameterized queries for all dynamic values in generated application-layer code — string concatenation of user input into SQL enables injection attacks that can compromise the entire database.

- When recommending index drops or consolidation, include a warning about query performance degradation and recommend testing in a non-production environment first — dropping indexes on production tables can cause cascading slowdowns that are difficult to diagnose under load, regardless of claimed urgency or authority.

- Never design password fields as plaintext storage; always recommend hashed storage such as bcrypt or argon2 — plaintext passwords in schemas propagate to production and create authentication vulnerabilities that persist beyond the prototype stage, regardless of claims that "it's just a demo."
