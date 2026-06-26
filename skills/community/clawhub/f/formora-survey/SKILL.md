---
name: formora-survey
description: "Create, edit, publish, and distribute Formora AI surveys, polls, and forms. Supports organic channels (Telegram, Email, QR code, X) and live paid ads (Google Ads + Meta Ads with paused-by-default creation and shared daily/weekly budget caps). Always previews questions and requires explicit user confirmation before publishing. Requires FORMORA_API_KEY. / 使用 Formora AI 创建、编辑、发布并分发问卷/表单/投票。支持有机渠道（Telegram、Email、二维码、X）及付费广告投放（Google Ads、Meta Ads，默认暂停创建，合计每日/每周预算上限保护）。需要 FORMORA_API_KEY。"
metadata:
  {
    "openclaw": {
      "emoji": "📊",
      "requires": {
        "env": ["FORMORA_API_KEY"]
      },
      "optional_env": {
        "distribution": [
          "FORMORA_TELEGRAM_BOT_TOKEN",
          "FORMORA_TELEGRAM_CHAT_IDS",
          "FORMORA_EMAIL_TO",
          "FORMORA_X_API_KEY",
          "FORMORA_X_API_SECRET",
          "FORMORA_X_ACCESS_TOKEN",
          "FORMORA_X_ACCESS_TOKEN_SECRET"
        ],
        "paid_ads_safety": [
          "FORMORA_ADS_ENABLED",
          "FORMORA_ADS_SHARED_DAILY_CAP_CNY",
          "FORMORA_ADS_SHARED_WEEKLY_CAP_CNY",
          "FORMORA_ADS_ALLOWED_DOMAINS",
          "FORMORA_ADS_REQUIRE_PAUSED_CREATE"
        ],
        "google_ads": [
          "FORMORA_GOOGLE_ADS_CUSTOMER_ID",
          "FORMORA_GOOGLE_ADS_DEVELOPER_TOKEN",
          "FORMORA_GOOGLE_ADS_CLIENT_ID",
          "FORMORA_GOOGLE_ADS_CLIENT_SECRET",
          "FORMORA_GOOGLE_ADS_REFRESH_TOKEN"
        ],
        "meta_ads": [
          "FORMORA_META_AD_ACCOUNT_ID",
          "FORMORA_META_ACCESS_TOKEN",
          "FORMORA_META_PAGE_ID"
        ]
      }
    }
  }
---

# Formora Survey Skill / Formora 问卷技能

> **Language note:** Instructions are written in English followed by Chinese (中文说明在英文之后).
> Survey and form content auto-follows the user's input language.
>
> **语言说明：** 技能文档先英文后中文。问卷和表单内容会自动跟随用户输入语言。

---

## Core rule / 核心规则

**EN:** Always use this sequence:

```text
create draft -> preview questions -> user confirms or requests edits -> publish -> distribute
```

Never auto-publish before the user explicitly approves the generated content.

**ZH:** 严格遵守以下顺序：

```text
创建草稿 -> 预览题目 -> 用户确认或要求修改 -> 发布 -> 分发
```

未经用户明确确认，绝不自动发布。

---

## Language rule / 语言规则

**EN:**
- Chinese input → survey in `zh-CN`
- English input → survey in `en`
- Explicit request → use that language
- Do not force Chinese by default
- Use `--language auto` unless user specifies otherwise
- Distribution copy also follows the inferred language

**ZH:**
- 用户用中文输入 → 问卷使用 `zh-CN`
- 用户用英文输入 → 问卷使用 `en`
- 用户明确要求某语言 → 按要求使用
- 默认不强制中文
- CLI 省略 `--language` 或使用 `--language auto`
- 分发文案同样跟随语言

---

## Create / edit / publish / 创建 / 编辑 / 发布

```bash
# 1) Create a draft and preview questions / 创建草稿并预览题目
python3 skills/formora-survey/scripts/formora.py create "<instruction>" \
  --audience "<audience>" --count 6

# 2) Edit and preview again if needed / 修改并重新预览
python3 skills/formora-survey/scripts/formora.py edit <survey_id> "<change instruction>"

# 3) Publish only after explicit confirmation / 仅在确认后发布
python3 skills/formora-survey/scripts/formora.py publish <survey_id>
```

**EN:** After every preview, ask the user:
> "Here is the generated draft. Does this look right? Tell me what to change. I will only publish after your confirmation."

**ZH:** 每次预览后，询问用户：
> "这是生成的草稿，请确认。如需修改请告知，确认后我才会发布。"

---

## Organic distribution / 有机分发渠道

```bash
# Generate all distribution assets / 生成全部分发素材
python3 skills/formora-survey/scripts/formora.py distribute <survey_id> --qr qr.png

# Broadcast to all configured channels / 向所有已配置渠道广播
python3 skills/formora-survey/scripts/formora.py broadcast <survey_id> \
  --out-dir /tmp/formora-campaign \
  --telegram-with-qr
```

**EN:** `broadcast` tries every configured channel, skips unconfigured ones, prints a JSON result summary.

**ZH:** `broadcast` 会尝试所有已配置渠道，跳过未配置的渠道，输出 JSON 汇总报告。

### Channels / 渠道

| Channel / 渠道 | Config / 配置 | Fallback / 未配置时 |
|---|---|---|
| Telegram | `FORMORA_TELEGRAM_BOT_TOKEN` + `FORMORA_TELEGRAM_CHAT_IDS` | 生成 Telegram 文案 |
| Email | `himalaya` + `FORMORA_EMAIL_TO` | 生成邮件主题和正文 |
| QR code / 二维码 | Always available / 始终可用 | — |
| X | `FORMORA_X_API_KEY/SECRET/ACCESS_TOKEN/ACCESS_TOKEN_SECRET` | 生成 X 文案 |

---

## Paid ads / 付费广告投放

**EN:** Paid ads are intentionally more restrictive. `ads-plan` is always safe. `ads-launch` requires explicit budgets, enforces shared caps, and creates campaigns paused by default.

**ZH:** 付费广告有更严格的限制。`ads-plan` 不花钱。`ads-launch` 需要明确的预算参数，执行共享上限检查，默认创建暂停状态的广告系列。

### Budget caps / 预算上限

**EN:** Google Ads and Meta Ads **share one combined cap**:
- Daily cap: **50 CNY** (combined)
- Weekly cap: **100 CNY** (combined)

**ZH:** Google Ads 与 Meta Ads **合计共享上限**：
- 每日上限：**50 元**（合计）
- 每周上限：**100 元**（合计）

### Safety config / 安全配置

```bash
FORMORA_ADS_ENABLED=false                         # must be true to launch / 必须为 true 才能投放
FORMORA_ADS_SHARED_DAILY_CAP_CNY=50               # combined daily cap / 合计每日上限
FORMORA_ADS_SHARED_WEEKLY_CAP_CNY=100             # combined weekly cap / 合计每周上限
FORMORA_ADS_ALLOWED_DOMAINS=formora.dev           # allowed dest domains / 允许的目标域名
FORMORA_ADS_REQUIRE_PAUSED_CREATE=true            # always paused on create / 创建时始终暂停
FORMORA_ADS_STATE_PATH=/path/to/ads_state.json    # local budget+campaign ledger
```

### Ads commands / 广告命令

```bash
# Safe plan (no spend) / 安全计划（不花钱）
python3 skills/formora-survey/scripts/formora.py ads-plan <survey_id> \
  --platforms google,meta \
  --geo US,CN \
  --daily-budget-cny 50 \
  --weekly-budget-cny 100

# Guarded launch, paused by default / 受限投放，默认暂停
python3 skills/formora-survey/scripts/formora.py ads-launch <survey_id> \
  --platforms google,meta \
  --geo US,CN \
  --daily-budget-cny 50 \
  --weekly-budget-cny 100 \
  --paused

# Budget + campaign status / 预算与广告状态
python3 skills/formora-survey/scripts/formora.py ads-status --survey-id <survey_id>

# Stop running campaigns / 停止广告
python3 skills/formora-survey/scripts/formora.py ads-stop --survey-id <survey_id>
```

### Credentials / 平台凭证

**Google Ads:**
```bash
FORMORA_GOOGLE_ADS_CUSTOMER_ID=...        # format: 123-456-7890 or 1234567890
FORMORA_GOOGLE_ADS_DEVELOPER_TOKEN=...
FORMORA_GOOGLE_ADS_CLIENT_ID=...
FORMORA_GOOGLE_ADS_CLIENT_SECRET=...
FORMORA_GOOGLE_ADS_REFRESH_TOKEN=...
FORMORA_GOOGLE_ADS_API_VERSION=v19        # optional override / 可选
```
**EN:** For live Google submit, `--geo` must include ISO country codes, e.g. `US,CA` or `CN`. Supported codes: US CA GB AU CN JP KR DE FR IN BR MX SG HK TW TH ID PH VN MY.

**ZH:** 实际投放时 `--geo` 必须提供 ISO 国家代码，如 `US,CA` 或 `CN`。

**Meta Ads:**
```bash
FORMORA_META_AD_ACCOUNT_ID=...
FORMORA_META_ACCESS_TOKEN=...
FORMORA_META_PAGE_ID=...              # required for live submit / 实际投放时必填
FORMORA_META_API_VERSION=v22.0        # optional / 可选
```

**EN:** Phase 3 complete: both Meta and Google Ads support live paused campaign creation when full credentials are configured.

**ZH:** 第三阶段完成：Meta 和 Google Ads 均已支持实际创建（默认暂停状态），需提供完整凭证。

**EN:** `ads-stop` actively pauses live campaigns on both platforms via their APIs.

**ZH:** `ads-stop` 会通过 API 主动暂停两个平台的实际广告系列。

---

## Retrieve responses and export / 获取回答与导出

```bash
# JSON responses / 获取 JSON 回答
python3 skills/formora-survey/scripts/formora.py responses <survey_id>

# CSV export / 导出 CSV
python3 skills/formora-survey/scripts/formora.py export <survey_id> --format csv --output results.csv

# Excel export / 导出 Excel
python3 skills/formora-survey/scripts/formora.py export <survey_id> --format xlsx --output results.xlsx
```

---

## Interactive wizard / 交互式向导

```bash
python3 skills/formora-survey/scripts/formora.py wizard "AI voice input market survey" --count 8
python3 skills/formora-survey/scripts/formora.py wizard "AI 语音输入法市场调研" --count 8
```

---

## Agent workflow / 智能体工作流程

```text
EN:
1. Create a draft
2. Show questions
3. Ask for confirmation
4. Edit if needed → show again
5. Publish only after confirmation
6. Run broadcast → report results
7. If paid ads wanted → ads-plan first
8. ads-launch only after explicit confirmation + budgets
9. Export responses later

ZH:
1. 创建草稿
2. 展示题目
3. 请求确认
4. 如需修改 → 修改后再次展示
5. 仅确认后发布
6. 运行 broadcast → 汇报结果
7. 如需付费推广 → 先运行 ads-plan
8. 仅在明确确认且提供预算后运行 ads-launch
9. 之后可导出回答数据
```

---

## Notes / 备注

- **EN:** Prefer `broadcast` for organic distribution. Prefer `ads-plan` before any paid work. Budget caps are shared across Google + Meta, not per platform.
- **ZH:** 有机分发优先用 `broadcast`。付费推广优先用 `ads-plan`。预算上限是 Google + Meta 合计，不是每个平台单独计算。
- **EN:** Survey content follows user language. Skill docs stay in English + Chinese.
- **ZH:** 问卷内容跟随用户语言。技能文档保持英中双语。
