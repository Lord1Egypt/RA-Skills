# Translate to Chinese

When `config.digestLanguage` is `"zh"` or `"bilingual"`, translate the digest
from English to Chinese following these rules.

## What to Translate

- **Translate**: section headers, descriptions, release notes, prose
- **Do NOT translate**:
  - Repo names (`owner/repo`) — keep as-is
  - Usernames (`@alice`, `alice`) — keep as-is
  - Language tags (`[Python]`, `[Rust]`) — keep as-is
  - URLs — keep as-is
  - Technical terms that are common in Chinese developer communities
    (PR, commit, fork, star, issue, release, CLI, API, SDK)
  - Repo tags, version numbers (`v2.0.0`)

## Style

- Casual Chinese, the way a Chinese developer would talk about code
  ("给 XX 加了个功能", not "为 XX 增添了功能")
- Keep sentences short — this is a scannable digest, not prose
- "star" → "star" (don't translate to "标星" or "收藏"; devs say "star")
- "fork" → "fork"
- "followed" (in the context of GitHub follow) → "关注"
- "trending" → "trending" or "热门" — either works, stay consistent within one digest

## Bilingual Mode

If `config.digestLanguage` is `"bilingual"`:
- Section headers: English header, then Chinese header on the next line
- Repo descriptions: English first, then Chinese on the next line (indented)
- Do not duplicate repo names, URLs, language tags, or star counts

## Header Translation Reference

| English | Chinese |
|---|---|
| GitHub Digest — [Date] | GitHub 速递 — [日期] |
| From People You Follow | 你关注的人 |
| Trending | Trending |
| Notable New Projects | 新兴项目 |
| starred | star 了 |
| created | 新建了 |
| open-sourced | 开源了 |
| released | 发布了 |
| created N days ago | N 天前创建 |
| Reply to adjust ... | 回复可调整频率、内容源、语言或摘要风格。 |
