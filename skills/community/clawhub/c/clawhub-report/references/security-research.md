# Security Research Checklist

## When to fetch current information

Fetch from the web when the task depends on:
- Recent CVEs or advisories
- Version-specific behavior
- Product release notes
- Evolving best practices
- Comparative vendor guidance

## What to extract

- Topic definition
- Scope and assumptions
- Affected software / protocol / environment
- Why it matters
- Defensive guidance
- Known limitations or disputed claims
- Date and source of information

## Source preference

Prefer these source types first:
1. Official vendor or project documentation
2. Standards or primary references
3. Reputable security advisories
4. Well-regarded technical writeups

## Writing rules

- State uncertainty explicitly
- Do not present rumors as facts
- Note versions and dates when relevant
- Prefer defensive recommendations
- Summarize attack concepts at a high level unless the user clearly asks for authorized defensive testing detail

## Good research questions

- 这个协议解决了什么问题？
- 它的核心机制是什么？
- 常见风险点在哪里？
- 现实部署中最容易踩的坑是什么？
- 当前推荐的防护方式是什么？
- 哪些结论受版本变化影响很大？
