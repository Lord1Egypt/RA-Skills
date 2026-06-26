---
name: wos-feishu-literature
description: Use when the user mentions wos, WOS, WoS, or Web of Science and wants topic-based literature search, Shenzhen University library login, paper screening, abstract extraction, and writing results into a Feishu Base/multidimensional table via local lark-cli. Also use when the user wants a reusable WOS-to-Feishu workflow, academic literature collection, SSCI-focused retrieval, or a 中文文献检索到飞书多维表格流程.
---

# WOS Literature To Feishu

Before executing, read [references/playbook.md](references/playbook.md).

## Core Rules

- Trigger this skill whenever the user mentions `wos`, `WOS`, `WoS`, or `Web of Science`.
- Before touching WoS or Feishu, ask the preflight questions from the playbook in one batch. If the required inputs are still missing, stop and wait for the user instead of searching immediately.
- Prefer the Shenzhen University library route first:
  `https://www.lib.szu.edu.cn/er?key=web+of+science`
- Prefer `Web of Science - SSCI` when the user does not specify another database.
- Browser automation for WoS is not fixed to one tool. If the user explicitly says they are using `playwright-cli`, use the `playwright-cli` skill for browser steps and do not silently switch to `opencli-browser`. Only use another browser automation path when the user agrees or the requested path is unavailable.
- Prefer local `lark-cli` for Feishu Base writeback. Do not default to browser-based Feishu data entry.
- If login reaches Shenzhen University unified auth and asks for SMS code, verification code, captcha, or other second-step authentication, stop and wait for the user to complete it before continuing.
- Default SZU username may be prefilled as `2410032057` for this user's local workflow, but keep the password runtime-only and do not persist it into the skill.
- Do not store passwords, verification codes, or other credentials inside the skill, repo, or local files. If the user shares credentials in the current chat, treat them as runtime-only and do not persist them into the skill.
- Do not silently switch to direct Clarivate login while the SZU route is available. Use direct Clarivate institution login only as a fallback.
- Do not write into the wrong Feishu subtable. Confirm the exact Base link and target table handling first.
- If the user has no clear screening rule, use the simple default:
  `高相关 + 高引用 + 近5年代表作 + 摘要完整 + 去重 + 子主题覆盖均衡`

## Execution Order

1. Ask the preflight questions from the playbook.
2. Lock the search scope, target count, and screening rule.
3. Expand the user's Chinese topic into English core concepts, synonyms, adjacent concepts, and object terms before building final queries.
4. Enter WoS through the SZU library route and wait at any verification step.
5. Build query buckets and collect candidate papers.
6. Deduplicate and screen down to the target count.
7. Extract at least `标题 / 年份 / 作者 / Q几区 / 引用数 / 摘要 / 文章链接 / 抓取时间 / 主题标签 / 现在状态`, and actively resolve `Q几区` whenever that field exists in the target schema.
8. Use local `lark-cli` to create or update the Feishu table fields and records.
9. Verify final table name, field structure, sample rows, and record count.

## Important Defaults

- Database default: `WOS Core Collection -> SSCI`
- Document type default: `Article + Review`
- Language default: `English`
- Count default when the user says "先来一批": `50`
- Base field default: `标题 / 年份 / 作者 / Q几区 / 引用数 / 摘要 / 文章链接 / 抓取时间 / 主题标签 / 现在状态`
- `Q几区` default semantics: `JCR Quartile`, and it should be checked by default when that field is present.

## Journal Quartile Rule

- `SSCI几区 / JCR几区 / 中科院分区` is journal-level metadata, not article-level metadata.
- If the target table includes `Q几区`, do not silently skip it during writeback.
- Unless the user explicitly asks for `中科院分区`, interpret `Q几区` as `JCR Q1/Q2/Q3/Q4`.
- Before writing records, either fill `Q1/Q2/Q3/Q4` or explicitly report that quartile verification is still pending.
- Do not treat `Q几区` as optional just because it requires an extra journal-level lookup step.
- Abstract extraction is normally feasible from the WoS full record page and can be written into Feishu Base.

## Default Field Types

- `标题`: `text/plain`
- `年份`: `number`, integer
- `作者`: `text/plain`
- `Q几区`: `select`, single choice, options `Q1/Q2/Q3/Q4`; if the workflow often needs staged completion, add `待查`
- `引用数`: `number`, integer
- `摘要`: `text/plain`
- `文章链接`: `text/url`
- `抓取时间`: `datetime`
- `主题标签`: `text/plain`
- `现在状态`: `select`, single choice, options `已读摘要/已读全文`, blank allowed

## Windows Notes

- On Windows PowerShell, if `lark-cli` resolves to `lark-cli.ps1` and is blocked by execution policy, explicitly call `lark-cli.cmd`.
- If the user chooses `playwright-cli`, prefer `playwright-cli snapshot` for page inspection, and use a persistent profile or the user's existing session strategy only after confirming it with the user.
- When using `--json @file` in PowerShell, quote the value, for example:
  `--json "@.\\feishu\\record_payloads\\001.json"`

