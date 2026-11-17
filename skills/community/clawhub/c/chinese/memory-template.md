# Working File Templates — Chinese

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/chinese/config.yaml` | Key by key, read-modify-write |
| Who they write to and at what register, which channels they write on, environment facts, pain points, box index, due dates | `~/Clawic/data/chinese/memory.md` | Rewritten in place; stays small |
| Terms, product and person names rendered in Chinese; items kept in English; corrections from native readers; slang retired as stale | `## Glossary` in `memory.md` until it outgrows it, then `~/Clawic/data/chinese/glossary.md` | One row per term |
| A channel's long-form voice guide — register, opener and closer, emoji density, paragraph shape, worked examples | `~/Clawic/data/chinese/styles/<channel>.md` | Born as its own file the first time a channel's rules pass one line |
| Pieces delivered: date, channel, audience, what it was, how it landed | `~/Clawic/data/chinese/pieces/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read — templates that worked (请假条, 辞职信, 邀请函, 自我介绍, 敬酒词), Chinese naming decisions, reviews of someone else's text, speech and presentation scripts, headline banks, slang calibration snapshots, pronunciation or pinyin guides, 术语表 for one paper or product | `~/Clawic/data/chinese/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| A recipient, native reviewer, client, editor or 甲方 contact | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill's contacts in one file |
| A Chinese-language effort tracked as work in progress — a 公众号 launch, a market entry, a book, a thesis | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| **Anything durable this table does not name** | `~/Clawic/data/chinese/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Three questions decide anything not listed, in order: would another skill want to read it (→ a shared box); is it a text read whole when its subject comes up (→ `artifacts/`); is it one more row of something accumulating (→ a `memory.md` section until the threshold).

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A term, product name or person's name got a Chinese rendering for the first time | Its row in `### Terms` |
| Something must stay in English or in Latin letters (a brand, an acronym the team uses) | `### Keep In English` |
| A native reader, reviewer or the user corrected a rendering, a particle, a title or a register | `### Corrections`, with the accepted form and who said so |
| A slang term was judged stale, or one was adopted | `### Retired Slang`, with the year it peaked |
| The address form or register for a person was settled | `## Recipients`, keyed by their contacts key |
| A channel's voice was settled | `## Channels`; anything longer than a line goes to `styles/<channel>.md` |
| A piece was delivered — a post, an email, a document, a speech | A row in `pieces/<year>.md`, with how it landed if that is known |
| A template, a naming decision, a review of someone's text, or a script came out of the session | `artifacts/` |
| Something about the setup cost effort to find — a platform that strips emoji or limits a word, a font missing a character, an audience older than assumed, an account type's limits, an IME quirk | `## Environment` |
| Something landed badly — wrong register, a misread joke, a filtered post | `## Pain Points`, with the cause |
| A recipient, reviewer or client was named | The shared contacts box |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except style guides, the pieces log, artifacts and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, promoted one level (`### Terms` inside `memory.md` becomes `## Terms` in `glossary.md`), so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

The glossary has one extra trigger: **a second variant splits it immediately**, whatever the entry count, because a term table mixing 简体 mainland and 繁體 Taiwan renderings cannot be read while writing in either one. Destination `glossaries/<variant>.md` (`mainland.md`, `taiwan.md`), keeping the same headings.

Style guides, artifacts and the pieces log are the exception to counting: a channel voice guide, a template or a naming decision is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:WECHAT_APP_SECRET` · `keychain:xiaohongshu-login` · `1password:Work/Weibo/ops` · `bitwarden:Personal/WeChat` · `file:~/.config/wechat/session`

When the user pastes something to save — a platform API config, a group's invite text with a login in it, an account handover note — replace each secret value before writing and leave the pointer visible: `app_secret: <env:WECHAT_APP_SECRET>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: names, Chinese renderings of names, titles (王总, 李工), public account names and handles, group chat names, city and 省 names, post URLs, follower counts, word counts, prices with their currency, invoice numbers. **Secrets, strip them**: platform app secrets and access tokens, account passwords, verification codes, 支付 keys, ID numbers (身份证号), full bank card numbers, private phone numbers the user has not asked to keep, anything inside a pasted config or `.env`.

One rule that is not about credentials: **a piece of writing often carries someone else's private business** — a resignation letter names a grievance, a 请假条 names an illness. Keep the template and the register decision, not the personal detail; if a full text must be kept as a reference, strip the names and the reason and say so.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [glossary.md](#glossarymd) · [styles/](#styles) · [pieces/](#pieces) · [artifacts/](#artifacts) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/chinese/` if it does not exist.

```yaml
variant: mainland
script: from-variant
formality: auto
address_form: auto
slang_appetite: light
pinyin_gloss: none
default_channel: wechat
latin_spacing: true
crude_ok: false
platform_filter_aware: true
emoji_density: sparse

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  weekday: 周六            # not 星期六, not 礼拜六
  money: 元                # written 元, spoken 块
  date: 2026年7月26日
  paragraph: blank-line    # not 首行缩进两字
voice:
  self_reference: 我        # 小编 only on the 公众号
  fragments: welcome
risk_posture:
  direct_disagreement: "soften with a superior, plain with peers"
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Chinese Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Glossary (34 terms) → `glossary.md`; read before writing any product or team copy
- 小红书 voice → `styles/xiaohongshu.md`; read before any 小红书 note
- 公众号 voice → `styles/gongzhonghao.md`; read before any long-form post
- Pieces 2026 (28) → `pieces/2026.md`; read when asked what was sent to whom, or before reusing a piece
- 请假条 template → `artifacts/template-qingjiatiao.md`; read whenever leave has to be requested
- Product name decision → `artifacts/naming-product-zh.md`; read before any Chinese marketing copy

## Due
| What | Every | Last run | Next due |
|---|---|---|---|
| Re-calibrate the slang list against what the audience actually uses | 6 months | 2026-03-02 | 2026-09-02 |
| Native review of the channel style boxes | quarter | 2026-05-10 | 2026-08-10 |
| Glossary consolidation: one rendering per term | quarter | 2026-04-18 | 2026-07-18 |
| Re-check platform wording rules after a policy change | on change | 2026-06-01 | on change |

## Profile
Writing as: 产品经理 at a Shenzhen SaaS company, not a native speaker, reads fluently.
Audience: mainland colleagues 25-40, plus a Taiwanese client contact.
Variant: 简体 mainland for everything except the Taiwan client thread.

## Recipients
| Contact key | Relationship | Address | Register | Notes |
|---|---|---|---|---|
| wang@example.com | 老板, 15 years senior | 您 | 正式 | 王总, never the given name; he writes 你 downward, that does not invite reciprocity |
| xiaoli@example.com | peer, same team | 你 | 日常 | 小李; opened with 哈哈哈 first, so match length |
| chen@example.tw | Taiwan client | 您 | 正式 | 繁體, 陳經理, 貴公司 in writing |

## Channels
| Channel | Register | Address | Emoji | Notes |
|---|---|---|---|---|
| WeChat 1:1 | 日常 | 你 | sparse | no final 。, no bolding |
| Work group | 客气 | 你 / @name | none | @ + 收到 is the ack, nothing longer |
| 小红书 | 日常 | 姐妹们 | native | full guide in `styles/xiaohongshu.md` |

## Glossary
### Terms
| English / source | Chinese | Variant | Part of speech | Context / why | Set on |
|---|---|---|---|---|---|
| workspace | 工作区 | mainland | noun | never 工作空间; matches the UI label | 2026-03-11 |
| onboarding | 新手引导 | mainland | noun | 入职 only when it means an employee joining | 2026-04-02 |

### Keep In English
Acme · Acme Cloud · PPT · KPI · SaaS · error codes `ACM-###`

### Corrections
| Wrong | Right | Who said so | Why | Date |
|---|---|---|---|---|
| 王总经理您好 | 王总您好 | 小李 | 总 already carries the title; stacking both reads as a form letter | 2026-03-20 |
| 呵呵 | 哈哈哈 | 小李 | 呵呵 reads as contempt on the mainland | 2026-03-20 |

### Retired Slang
| Term | Peaked | Verdict | Date |
|---|---|---|---|
| 绝绝子 | 2021 | retired — reads as forced on this audience | 2026-03-02 |
| 内卷 | 2020 | keep — crossed into ordinary vocabulary | 2026-03-02 |

## Environment
The 公众号 editor strips consecutive blank lines and re-renders ASCII quotes as full-width. The work group is on
WeChat Work, where 表情包 do not sync to the desktop client. The Taiwan client's mail system renders 简体 as tofu
in the subject line only.

## Pain Points
2026-02: a 通知 went out with 吧 in it and read as unserious; the register was borrowed from a chat message.
Formal documents now go through the Register Ladder explicitly.

## How They Work
Wants the Chinese and nothing else, then a one-line note on anything risky. Reads the explanation only if the
Chinese surprises them.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. `on change` is a valid cadence: it fires on the named event, not on a date. The slang row is the one that matters most here, because that list decays whether or not anyone looks at it.
- **`## Recipients`**: identity is the **contacts key**, so the person is not duplicated — their name, role and channel live in the shared contacts box and only the Chinese-specific columns live here. One row per person, never per message. A row that needs a paragraph is a `styles/` file waiting to be created.
- **`## Channels`**: one row per channel, and the row is a summary of the style box, never a replacement for it.
- **`### Corrections`** is the highest-value section in the file: a native correction that is not written down gets re-earned by making the same mistake in front of the same person. Always record who said so — a correction from the actual reader outranks a general rule.
- **`### Retired Slang`** keeps the verdict *and* the peak year, because "retired" without a date is unreviewable when the same term comes back as ironic usage.
- **`## Environment`** holds facts that change future decisions, in prose. Incidents go to `## Pain Points`.

| Status | Meaning |
|---|---|
| `ongoing` | Still learning their audience, register and vocabulary |
| `complete` | Variant, register per recipient and channel voices all settled |

## glossary.md

Created by the split procedure above, at `~/Clawic/data/chinese/glossary.md`, or immediately as `glossaries/<variant>.md` when a second variant appears. Keeps the four headings it had inside `memory.md`, promoted one level: `## Terms`, `## Keep In English`, `## Corrections`, `## Retired Slang`.

- **Identity is the source term plus its part of speech.** The same English word in two parts of speech is two rows, because a noun and a verb rarely share a rendering.
- Read the file before adding. If the term is there, do not add a second row: either the new context justifies a part-of-speech row, or the existing row is wrong and gets corrected in place with a new `Set on` date.
- A rendering that changes never disappears — it moves to `### Corrections` with the new form, so old text can be found and fixed.
- Person and product names are glossary rows too, and they are the ones that must never drift: a colleague whose name was written 大卫 in March and 戴维 in July has been renamed by accident.
- Past ~200 terms the file stops being readable in one pass; split by domain (`glossaries/mainland-product.md`, `-legal.md`) and leave the variant file as the index with the same headings.

## styles/

One file per channel, at `~/Clawic/data/chinese/styles/<channel>.md`, created the first time a channel's rules outgrow a single line in `## Channels`. Read whole, before writing anything for that channel.

```markdown
# Style — 小红书
*Read before any 小红书 note. Updated 2026-06-02.*

Register: 日常, 姐妹们 as the address, first person 我.
Title: 20 characters or fewer, one emoji, the pain point in the first six characters.
Body: one to three sentences per paragraph, blank line between; emoji as bullets, not decoration.
Slang: light — 干货, 避雷, 踩坑 yes; 绝绝子 retired (see memory).
Closing: one question to the reader, then 5-8 tags, most specific first.
Worked example: 打工人早八救命神器☕️ / 每天多睡20分钟的通勤咖啡方案
Do not: 首先其次, bolded terms, 希望对大家有帮助.
```

If the user supplies their own style guide or brand book, save it here under the same name, record the source and date at the top, and do not rewrite it in your words.

## pieces/

```markdown
# Pieces — 2026

| Date | Channel | Audience | What | Length | Register | How it landed |
|---|---|---|---|---|---|---|
| 2026-07-14 | 公众号 | subscribers, mainland | 产品更新说明 | 1,200 字 | 客气 | 阅读量 3.1k, two comments asked for a shorter version |
| 2026-07-21 | WeChat | 王总 | 项目延期说明 | 4 sentences | 正式 | accepted, no pushback |
```

- `Length` is in 字 for Chinese text, so two rows are comparable; a spoken script records its minutes instead (`3 min`) in the same cell.
- `How it landed` is the column that earns this file: without it the log is a diary, with it the next piece for the same audience starts from evidence.
- Cut by year. A year past ~150 rows splits by quarter (`pieces/2026-q3.md`), leaving `2026.md` as an index table (`Date | Channel | What | → file`).

## artifacts/

One file per thing, at `~/Clawic/data/chinese/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **a template that worked** (`template-<what>.md` — 请假条, 辞职信, 邀请函, 感谢信, 自我介绍, 敬酒词, 述职报告), **a Chinese naming decision** (person, product, company), **a review of someone else's text**, **a speech or presentation script**, **a headline bank**, **a slang calibration snapshot**, **a pinyin or pronunciation guide** for something to be read aloud, **a 术语表** for one paper or product. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Template — 请假条
*Read whenever leave has to be requested. Written 2026-05-12, accepted by 王总 unchanged.*

尊敬的王总：
    您好。因<原因，一句>，需请<假别>_天，时间为<起>至<止>。期间工作已交接给<姓名>，
    紧急事项可随时联系我。恳请批准。
    此致
敬礼
                                                        申请人：<姓名>
                                                        <YYYY年M月D日>

Notes: 首行缩进两字 is expected in this document type. 病假 attaches the 证明 and says so; 事假 states
the reason in one clause and does not elaborate — elaborating reads as excuse-making.
```

```markdown
# Naming decision — product name in Chinese
*Read before any Chinese marketing or store copy. 2026-05-30.*

Decision: keep the Latin brand, add a four-character descriptive Chinese subtitle. No phonetic transliteration.
Rejected: 艾克米 — generic transliteration, and one native reader heard it as 挨克.
Checked: no unintended reading in Cantonese; the four characters do not form an existing 成语.
Open: trademark clearance in the market (see the project file).
```

If the user tracks the effort as a project, the decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the reasoning staying here and referenced by name.

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that knows people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|---|---|---|---|---|---|---|
| 王建国 | wang@example.com | 老板, 产品线负责人 | WeChat | approves everything customer-facing | 2026-07-21 | — |
```

- **Identity is `Key`**: the email in lowercase; if there is none, the handle; if neither, `<kebab-name>` plus a stable disambiguator. The key is a column of the row, never implicit.
- Read the file before adding. If the key is already there, update that row in place — never a second row for the same person. Only rows you created are yours to change; leave other skills' rows alone.
- `Preferred channel` is the type of channel (WeChat, email, 钉钉), not the address.
- Record the person's Chinese name in `Name` and, if they also use a Latin name, put it in `Context` — a colleague addressed by two different names in two threads is the same failure as a drifting glossary term.
- **Scale cut**: one row per person while there are ≤15, or until one no longer fits its row. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index with the `File` pointer. If you arrive and the folder already looks like that, follow it.
- **Foreign columns win.** If `contacts.md` exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Rates or fees belong here only as a note with the currency (`800 CNY/篇`), never a bank detail or a portal password.
- Removing someone: delete the row, delete their `## Recipients` row, and note the date in `## Pain Points` or `## Profile`, whichever explains why. A contact list that only grows stops being one.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project, from the first one. Used when the Chinese-language work is something the user tracks — a 公众号 launch, entering the mainland market, a thesis, a book.

```markdown
# gongzhonghao-launch
status: active
goal: weekly 公众号 posts, 5k subscribers by Q4
milestones: voice guide agreed 2026-05-10 · first 10 posts 08-01 · native review 08-15
decisions: 简体 mainland only · 小编 as self-reference on this channel, 我 everywhere else (see chinese artifacts)
```

- Identity is the project slug, which is the filename. Read before writing; update the existing file in place.
- Closing it is `status: done | cancelled — <date>` inside the file, never deleting it: it is the record of what was delivered. Past ~20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- Keep the language detail in this skill's boxes and leave only the decision line here. Duplicating a decision in two places is how two skills start contradicting each other.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`, promoted one level.

`glossary.md` — `## Terms`, `## Keep In English`, `## Corrections`, `## Retired Slang`. The corrections are the reason this file earns its keep: without them the same wrong title or the same dead meme is re-proposed and re-rejected by the same reader.

`recipients.md` — `## Recipients` and `## Channels`, once the user writes to more than a handful of people or on more than a handful of channels. Same columns, same contacts keys.
