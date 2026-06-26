# Configuration Reference (EXTEND.md)

## All Supported Keys

### Global keys

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `default_theme` | string | `default` | Visual theme for article |
| `default_color` | string | — | Accent color |
| `default_publish_method` | `api` \| `browser` | `api` | Publishing method |
| `default_author` | string | — | Article author field |
| `need_open_comment` | `0` \| `1` | `1` | Enable comments |
| `only_fans_can_comment` | `0` \| `1` | `0` | Restrict comments to followers |
| `chrome_profile_path` | path | auto | Chrome profile directory |
| `default_humanize` | `light` \| `medium` \| `strong` | `medium` | Humanization strength |
| `default_tone` | tone string | inferred | Default article tone |
| `default_column` | string | — | Column/series label |
| `default_profile_block` | multiline string | — | Public-account intro block |
| `default_tail_keywords` | string list | — | Default long-tail keyword pool |
| `default_article_length` | integer | `2000` | Target article length (Chinese chars) |
| `confirm_before_publish` | boolean | `true` | Show pre-publish confirmation |
| `default_cta_type` | `technical` \| `market` \| `science` \| `generic` | inferred | CTA style |
| `domain_ai_tone_signals` | string list | built-in list | Phrases to suppress in AI-tone pass |
| `protected_terms` | string list | built-in list | Industry terms to preserve exactly |

### Per-account keys (inside `accounts:`)

All global keys above, plus:

| Key | Type | Description |
|-----|------|-------------|
| `name` | string | Display name of the account |
| `alias` | string | Short ID used in CLI and env vars |
| `default` | boolean | Pre-select this account in multi-account mode |
| `app_id` | string | WeChat AppID (or use env var) |
| `app_secret` | string | WeChat AppSecret (or use env var) |

---

## Full Annotated EXTEND.md Example

```yaml
# EXTEND.md — amiao-post-to-wechat configuration
# Replace all placeholder values with your actual account information.
# This file should NOT be committed to public repositories if it contains app_secret.

# ─── Global defaults ────────────────────────────────────────────────────────

default_theme: default
default_color: blue
default_publish_method: api
default_author: 你的账号名
need_open_comment: 1
only_fans_can_comment: 0
default_humanize: medium
default_tone: 专业评论
default_article_length: 2000
confirm_before_publish: true
default_cta_type: technical

# Public-account profile block appended at end of every article.
# Be specific: include name, content direction, reader value, 1-2 identity details.
default_profile_block: |
  这里填写你的公众号介绍：账号名称 + 主要内容方向 + 读者能获得的价值 +
  1 到 2 个让账号显得真实具体的身份或行业细节。

# Long-tail keywords appended at end of every article.
# Use topic-relevant natural Chinese phrases, not generic SEO fragments.
default_tail_keywords:
  - 行业内容优化
  - 微信图文发布
  - 不锈钢行情分析

# Domain-specific AI-tone phrases to suppress (replaces built-in list).
domain_ai_tone_signals:
  - 在全球不锈钢市场持续波动的背景下
  - 综合多方因素分析
  - 值得业内人士关注的是
  - 从当前行业发展趋势来看

# Industry terms to preserve exactly — never paraphrase or simplify.
protected_terms:
  - 双相钢
  - 316L
  - BA面
  - 盐雾测试时长
  - δ铁素体含量

# ─── Authors ─────────────────────────────────────────────────────────────────

authors:
  primary: 你的账号名

# ─── Accounts ────────────────────────────────────────────────────────────────

accounts:
  - name: 主账号
    alias: main-account       # env var prefix: WECHAT_MAIN_ACCOUNT_APP_ID
    default: true
    default_publish_method: api
    default_author: 主账号名
    need_open_comment: 1
    only_fans_can_comment: 0
    default_humanize: medium
    default_tone: 专业评论
    default_article_length: 2000
    confirm_before_publish: true
    default_cta_type: technical
    default_profile_block: |
      主账号专属介绍文字。
    default_tail_keywords:
      - 专属长尾词1
      - 专属长尾词2
    domain_ai_tone_signals:
      - 账号专属屏蔽词
    protected_terms:
      - 账号专属保护词

  - name: 快讯子账号
    alias: brief-account      # env var prefix: WECHAT_BRIEF_ACCOUNT_APP_ID
    default_publish_method: browser
    default_author: 快讯账号名
    need_open_comment: 1
    only_fans_can_comment: 0
    default_humanize: light
    default_tone: 行业快评
    default_article_length: 800
    confirm_before_publish: true
    default_cta_type: market
```

---

## Credential Storage (API method)

Preferred: environment variables with alias-prefixed keys.

Alias normalization: uppercase + hyphens → underscores.
Example: alias `main-account` → `WECHAT_MAIN_ACCOUNT_APP_ID`

```env
# amiao/.env  or  ~/amiao/.env
WECHAT_MAIN_ACCOUNT_APP_ID=your_app_id
WECHAT_MAIN_ACCOUNT_APP_SECRET=your_app_secret

# Single-account fallback
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
```

Do not store `app_secret` directly in EXTEND.md if that file may be shared or committed.

---

## Value Priority (for all settings)

```
CLI arguments
  > frontmatter / HTML meta
    > EXTEND.md account-level
      > EXTEND.md global-level
        > skill built-in defaults
```
