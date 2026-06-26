---
name: alpha-copilot-skill
description: Generate a daily priority leaderboard for 5 crypto tokens, with per-token fundamentals, liquidity, and risk summaries plus ready-to-publish drafts for X posts, group updates, and quick briefs. Use this skill when users want an OpenClaw research copilot for daily alpha scanning with SkillPay billing hooks.
---

# Skill: alpha-copilot-skill

## Purpose / 用途
Use this skill to produce a publishable daily research pack from Binance Web3 market signals.
用这个 skill 可以基于 Binance Web3 市场信号生成可直接发布的日报研究包。

It is designed for operators who want one fixed output:
- 今日优先级榜单
- 值得看的 5 个币
- 每个币的基本面/流动性/风险摘要
- 可直接发推文、发群、写快报的文案草稿

## Workflow / 工作流
1. Pull multiple Binance Web3 leaderboard views (`trending`, `top_search`, `alpha`).
2. Merge repeated token hits into one candidate list.
3. Enrich top candidates with token metadata and audit data.
4. Score candidates into a daily priority ranking.
5. Output JSON or Markdown and bill one successful `rank` call through SkillPay.

1. 拉取 Binance Web3 的多个榜单视图（`trending`、`top_search`、`alpha`）。
2. 合并重复上榜的 token，生成候选池。
3. 补充 token 元数据与审计信息。
4. 计算今日优先级评分。
5. 输出 JSON 或 Markdown，并在成功执行 `rank` 后接入 SkillPay 计费。

## Commands / 命令
Run from the skill root:
在 skill 根目录执行：

```bash
python3 scripts/alpha_copilot.py rank --chain bsc --lang zh --user-id demo
python3 scripts/alpha_copilot.py rank --chain base --format markdown --limit 5 --user-id demo
python3 scripts/alpha_copilot.py rank --chain solana --skip-audit --skip-billing
python3 scripts/alpha_copilot.py health
python3 scripts/alpha_copilot.py proxy-check --chain bsc
```

## Output Contract / 输出结构
Each ranked token includes:
每个入选币种包含：
- `symbol`
- `name`
- `contract_address`
- `priority_score`
- `priority_tier`
- `fundamentals_summary`
- `liquidity_summary`
- `risk_summary`
- `tweet_draft`
- `group_draft`
- `brief_draft`

The report also contains `leaderboard`, `top_tokens`, `summary`, and `generated_at_utc`.
整份报告还包含 `leaderboard`、`top_tokens`、`summary` 和 `generated_at_utc`。

## Billing Hook (SkillPay) / 计费接入
- Bill only `rank`.
- Default price comes from `SKILLPAY_PRICE_USDT` and should stay at `0.01`.
- Read API key from `SKILLPAY_APIKEY`.
- Keep `SKILLPAY_BASE_URL` / `SKILLPAY_CHARGE_URL` overrideable so the SkillPay integration can be swapped without changing report logic.
- Do not hard-code secrets.

- 只对 `rank` 计费。
- 默认价格来自 `SKILLPAY_PRICE_USDT`，默认应保持为 `0.01`。
- API key 从 `SKILLPAY_APIKEY` 读取。
- `SKILLPAY_BASE_URL` / `SKILLPAY_CHARGE_URL` 保持可覆盖，避免把 SkillPay 接口写死进业务逻辑。
- 不要硬编码任何密钥。

## Required/Useful Env Vars / 关键环境变量
- `SKILLPAY_APIKEY` (required for paid mode)
- `SKILLPAY_BILLING_MODE` (optional, `skillpay` or `noop`)
- `SKILLPAY_PRICE_USDT` (optional, default `0.01`)
- `SKILLPAY_USER_REF` (optional fallback user id)
- `BINANCE_WEB3_BASE_URL` (optional, default `https://web3.binance.com`)
- `BINANCE_HTTP_TIMEOUT_SEC` (optional, default `12`)
- `ALPHA_COPILOT_PROXY_MODE` (optional, `auto`/`env`/`direct`/`custom`, default `auto`)
- Standard proxy env vars are supported: `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY` and lowercase forms

- `SKILLPAY_APIKEY`（付费模式必需）
- `SKILLPAY_BILLING_MODE`（可选，`skillpay` 或 `noop`）
- `SKILLPAY_PRICE_USDT`（可选，默认 `0.01`）
- `SKILLPAY_USER_REF`（可选，默认用户标识）
- `BINANCE_WEB3_BASE_URL`（可选，默认 `https://web3.binance.com`）
- `BINANCE_HTTP_TIMEOUT_SEC`（可选，默认 `12`）
- `ALPHA_COPILOT_PROXY_MODE`（可选，`auto`/`env`/`direct`/`custom`，默认 `auto`）
- 支持标准代理环境变量：`HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY` 及其小写形式

## Notes / 说明
- This skill is for research and content generation, not auto-trading.
- Keep wording neutral and avoid profit guarantees.
- If audit or metadata enrichment partly fails, still return the report with unavailable fields instead of failing the whole run.
- Recommended proxy strategy:
  - Default `auto`: if the user's terminal has proxy env vars, requests use them; otherwise direct access is used.
  - Use `--proxy-mode direct` for overseas users who do not want inherited proxy settings.
  - Use `--proxy-mode custom --https-proxy ... --http-proxy ...` when the caller wants the skill to use a specific proxy without changing the shell environment.
  - Use `proxy-check` first when a user reports connection errors; it verifies root access, rank API, metadata API, and audit API in the current network mode.
  - `proxy-check` also returns bilingual fields: `summary.message_zh`, `summary.message_en`, `summary.suggestions_zh`, `summary.suggestions_en`.

- 这个 skill 用于研究与内容生成，不是自动交易工具。
- 文案要保持中性，不要承诺收益。
- 如果审计或元数据补充阶段部分失败，也要尽量保留报告结构，并把不可用字段标出来，而不是整份报告直接失败。
- 推荐代理策略：
  - 默认 `auto`：如果用户终端里存在代理环境变量，就自动继承；否则直连。
  - 海外用户可用 `--proxy-mode direct` 强制直连。
  - 如果不想修改 shell 环境，可用 `--proxy-mode custom --https-proxy ... --http-proxy ...` 显式指定代理。
  - 用户反馈联网失败时，优先先跑 `proxy-check`。
  - `proxy-check` 会返回双语字段：`summary.message_zh`、`summary.message_en`、`summary.suggestions_zh`、`summary.suggestions_en`。
