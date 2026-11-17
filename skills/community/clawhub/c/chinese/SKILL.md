---
name: Chinese
slug: chinese
version: 1.0.2
description: Writes and edits Mandarin Chinese that reads as if a native wrote it — casual or formal, mainland or Taiwan. Use when composing anything in Chinese (WeChat message, work email, 小红书 or 公众号 post, resume, 请假条, speech, toast, 通知, contract clause), or when Chinese text sounds stiff, textbook, translated, or AI-generated; when choosing 你 versus 您, 口语 versus 书面语, simplified versus traditional, or mainland versus Taiwan vocabulary; when 的/地/得, 了, 把, 被 or measure words come out wrong; when full-width punctuation, Han-Latin spacing, or 万/亿 number grouping is off; when internet slang, 成语, emoji or 表情包 need calibrating to an audience; when a refusal, apology, compliment or request has to land politely; or when naming a product or a person in Chinese. Not for translating an existing source text (`translate`), Traditional-only writing (`traditional-chinese`), or travelling in China (`china`).
homepage: https://clawic.com/skills/chinese
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🇨🇳
    displayName: Chinese
    os:
    - linux
    - darwin
    - win32
    configPaths:
    - ~/Clawic/data/chinese/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
    - ~/chinese/
    - ~/clawic/chinese/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/chinese/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
      - ~/chinese/
      - ~/clawic/chinese/
---

**Data.** At the start of every session, read `~/Clawic/data/chinese/config.yaml` (what the user declared) and `~/Clawic/data/chinese/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Before writing to a named person or on a named channel, read that person's row in `## Recipients` and the channel's style box `## Boxes` names for it: dropping to 你 after a month of 您, or renaming a term that was settled last release, is a defect even when both forms are grammatical. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a term, product or person's name rendered in Chinese for the first time; a correction from a native reader; a register or address-form decision for a person or a channel; a slang term retired as stale; a piece delivered and how it landed; an environment fact that cost effort to find (a platform that strips emoji, a font missing a character, an audience that skews older than assumed); or something the user will re-read — a template that finally worked, a Chinese naming decision, a review of someone else's text, a speech script. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People and ongoing work go to the shared boxes, not here.** A recipient, a native reviewer, a client or an editor is a row in `~/Clawic/data/contacts/contacts.md`; a Chinese-language effort the user tracks as work in progress — a 公众号 launch, a market entry, a book — is `~/Clawic/data/projects/<project>.md`. Read the box before adding and update the existing entry in place. The register and address form for that person stay here, in `## Recipients`, keyed by their contacts key: the person belongs to everyone, how you address them in Chinese belongs to this skill. Formats and identity keys travel in `memory-template.md`, so this works whether or not the owning skills are installed.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Platform accounts are the temptation: store the pointer and strip the value — `env:WECHAT_APP_SECRET`, `keychain:xiaohongshu-login`, `1password:Work/Weibo/ops`. If data sits at an old location (`~/chinese/` or `~/clawic/chinese/`), move it to `~/Clawic/data/chinese/`, and say in one line that you moved it and from where.

Model-written Chinese is almost always grammatical and almost always wrong at the register: one notch too formal, particle-free, and structured like an English essay wearing Chinese words. The job is to put back what a native adds without thinking — the 语气词, the fragment, the right 量词, the 全角 comma — and to take out what English pushed in: 进行 + verb, 一个 as an article, a 30-character attributive stacked before 的. Produce the Chinese first; explain in English only when asked. Work from defaults immediately: never open with questions about their variant, their audience, or how casual to be. The one exception to silence is script — while `variant` is unset, state which variant and script you are writing in before writing it (Rule 2). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: locale, timezone) → the Configuration table default.

## When To Use

- Writing original Chinese: messages, emails, posts, captions, documents, scripts, marketing copy, product names
- Repairing Chinese that reads wrong — too formal, textbook, translated, or recognisably AI — including text the user did not write
- Deciding the frame before the words: 你 or 您, 口语 or 书面语, simplified or traditional, mainland or Taiwan or Hong Kong vocabulary, how much slang
- Mechanics a non-native gets wrong: 的/地/得, 了, 把/被, measure words, full-width punctuation, 万/亿 numbers, dates, names, titles, addresses
- Pragmatics: refusing without saying no, apologising at the right weight, accepting a compliment, asking a favour, giving face in a group chat
- Act-as by default — this skill writes the Chinese. It advises instead when the user is learning and asks why; then the Chinese still comes first and the explanation follows it
- Not for translating a source text that already exists (`translate` — that job is bound to a source and this one is not), Traditional-only output (`traditional-chinese`), or travelling in China (`china`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "Make this sound less like AI wrote it" | Run the tell sweep before touching style: openers, 四字格 parallelism, uniform paragraphs, zero particles | `ai-tells.md` |
| WeChat message, group chat, reply to a boss | Drop the final 。, match 哈哈哈 length, never open with 在吗 | `chat.md` |
| Work email, 通知, 汇报, addressing a title | 尊敬的X总 → 结论先行 → 此致 敬礼; 王总 not 王总经理 | `business.md` |
| 小红书, 公众号, 微博, 抖音, B站, 知乎 post | Each platform is a different register with a different title mechanic | `social-media.md` |
| Simplified or traditional; mainland, Taiwan, HK, Singapore | Vocabulary diverges more than the glyphs do (Rule 2) | `regions.md` |
| Is this slang still alive? Which slang for this reader? | Date the term, then match the audience's age band (Rule 9) | `slang.md` |
| 的/地/得, 了, 把, 被, 是…的, word order, 量词 | The rule, the test, and the sentence rewritten | `grammar.md` |
| 全角 vs 半角, 《》「」"", ……, ——, spacing around Latin | Full-width always; the half-width comma is the loudest tell (Rule 8) | `punctuation.md` |
| Numbers, money, dates, phone, address, a person's name or title | Group by four; 两 before a measure word; big-to-small addresses | `numbers-and-names.md` |
| A 成语 or 俗语 — is it right, is it too much? | Frequency ceiling plus the twelve most-misused 成语 | `idioms.md` |
| 请假条, 辞职信, 简历, 邀请函, 感谢信, 合同 clause, 公文 | Fixed skeletons; 请示 and 报告 are different documents | `documents.md` |
| 论文, 摘要, 关键词, 术语, 参考文献 | 本文 not 我; 200-300 字 abstract; GB/T 7714 citations | `academic.md` |
| Something to be said aloud: call, voice note, toast, presentation | Spoken Chinese is shorter, more particled, and repeats the topic | `speaking.md` |
| Refusing, apologising, thanking, complimenting, asking a favour | The refusal ladder; 不好意思 vs 对不起 vs 抱歉 | `etiquette.md` |
| Checking someone else's Chinese, or hunting 错别字 and mojibake | IME homophone sweep, then register drift, then encoding | `proofreading.md` |
| Which 你/您 and how casual, for this person or this channel | The Register Ladder below, then record the decision in `## Recipients` | `register.md` |
| Anything else in Chinese | Write it at the register the channel implies, then state the two assumptions you made — audience and formality — so the user can correct one | — |

Coverage map: `register.md` formality and address form · `chat.md` WeChat and messaging · `business.md` workplace and email · `social-media.md` platform voices · `documents.md` formal paperwork · `academic.md` research and technical writing · `speaking.md` spoken scripts · `etiquette.md` politeness and face · `grammar.md` the mechanics that break · `punctuation.md` typography · `numbers-and-names.md` numbers, dates, names, addresses · `idioms.md` 成语 and 俗语 · `slang.md` internet language and its shelf life · `regions.md` variants and scripts · `ai-tells.md` machine fingerprints · `proofreading.md` reviewing existing Chinese.

## Core Rules

1. **Register comes from the relationship and the channel, never from the topic.** Decide before the first character; the Register Ladder below is the table. 您 belongs to elders, officials, customers, and first contact with a stranger who outranks the user; 你 covers everyone else including most colleagues. The asymmetry that matters: moving from 您 to 你 is a warming gesture the senior party offers, while moving from 你 back to 您 reads as cold anger, so a wrong 您 costs less than a wrong 你 only on first contact — after that it costs more. 您 has no standard plural: address a group as 大家 or 各位, never 您们. Record the choice per person in `## Recipients` the first time it is made.
2. **Variant and script are one decision, taken before writing and stated out loud when unset.** A glyph converter is not a variant converter: it produces 繁體字 carrying mainland vocabulary, which a Taiwanese reader spots in one line (視頻 for 影片, 軟件 for 軟體). It also guesses wrong on the one-to-many mappings, where one simplified character maps to several traditional ones — 发 → 發/髮, 干 → 幹/乾/干, 后 → 後/后, 里 → 裡/里, 面 → 麵/面, 只 → 隻/只, 云 → 雲/云, 松 → 鬆/松, 台 → 臺/檯/颱/台. Convert the vocabulary and re-read those characters by hand (`regions.md`).
3. **Numbers group by four, not by three.** 万 = 10⁴, 亿 = 10⁸. Convert by dividing: `value ÷ 10,000` → 万, `value ÷ 100,000,000` → 亿. So 1,200,000 → 120万 and 3,500,000,000 → 35亿; "3.5 billion" written as 三十五亿 is right and as 3.5十亿 is not Chinese. A seven-digit comma-grouped figure in Chinese prose is a translation artefact. Before a measure word the number two is 两 (两个人, 两天), while 二 stays in ordinals and compounds (第二, 十二, 二十). Full table in `numbers-and-names.md`.
4. **Casual Chinese carries a 语气词 roughly every three to four short sentences; zero across a whole message is the machine signature.** Working target, not a measurement — the particle goes where the feeling is, and one on every sentence reads as a cartoon. Each carries a distinct job: 啊/呀 soften, 呢 hand the turn back, 吧 propose or hedge, 嘛 mark the obvious, 啦 close something off, 哦/噢 acknowledge, 呗 shrug. Formal writing takes none of them: a 通知 with 吧 in it is a different failure (`register.md`).
5. **Cut the attributive at about twelve characters before 的.** Chinese stacks every modifier ahead of the noun, so an English relative clause moved across in place forces the reader to hold the whole modifier in memory before learning what it modifies. Working threshold: past ~12 characters, break it into its own clause and let the noun arrive first — 我昨天在楼下咖啡店遇到的那个人 becomes 那个人，我昨天在楼下咖啡店遇到的. 余光中's essays on 欧化中文 are the standard treatment; this is their operational form, and the full table of Europeanised patterns with their rewrites is in `grammar.md`.
6. **Delete 进行/作出/给予/予以 plus a noun and put the verb back.** 进行讨论 → 讨论, 作出决定 → 决定, 给予支持 → 支持, 予以考虑 → 考虑. Each deletion removes two characters and one degree of bureaucratic distance. Same family: 一个 used as an English indefinite article, 们 stacked on a noun already marked plural (三个学生们), 性/化 suffixes on words that do not need them (可行性方案 → 可行的方案), and 被 on anything that is not adverse (被讨论 is un-Chinese; 被表扬 has been naturalised and is fine).
7. **的/地/得 are decided by what follows them, not by how they sound.** Formula: `X的 + 名词` · `X地 + 动词` · `动词/形容词得 + 补语`. Worked: 高兴**的**孩子 (noun follows) · 高兴**地**说 (verb follows) · 说**得**很高兴 (complement follows). This is the single most common 错别字 in native writing too, so an error here does not read as foreign — it reads as careless, which for a 公文 or a resume is worse (`grammar.md`).
8. **Full-width punctuation throughout, and never a space after it.** ，。、；：？！ are full-width; a half-width comma inside Chinese text is the loudest non-native mark there is. 、 separates items inside a list and never joins clauses. Ellipsis is …… (two characters, six dots), the dash is —— (two characters), and titles of books, films and articles take 《》 rather than italics. Quote marks follow the variant: “ ” ‘ ’ on the mainland, 「」『』 in Taiwan and Hong Kong. Spacing between Han and Latin or digits is a house style, not a national standard — `latin_spacing` decides, and whichever way it goes it is applied to every occurrence (`punctuation.md`).
9. **Slang is dated the moment it is used, so only use a term you can date.** If the era it peaked in cannot be named, do not use it. A term that peaked more than roughly three years ago and never became ordinary vocabulary reads as a dead meme, which is worse than plain writing — 然并卵 and 我伙呆 (2015) are now period costume, while 打工人 and 内卷 (2020) crossed into ordinary speech and are safe. Governed by `slang_appetite`; the calibration sample rots, so re-check it on the `## Due` cadence rather than trusting the list (`slang.md`).

## AI Tells In Chinese

The fingerprints that make a Chinese reader screenshot a text as 机翻 or AI. Sweep for these before style: they are structural, so no amount of vocabulary polish removes them.

| Tell | Why it reads machine | Do instead |
|---|---|---|
| 首先…其次…再次…最后 | Essay scaffolding pasted into a message nobody asked to be structured | Say the thing; if order matters, 先…然后… or nothing at all |
| 总之 / 综上所述 / 总的来说 | A summary of four sentences the reader just read | Delete. If a conclusion is needed, put it first (`business.md`) |
| 值得注意的是 / 需要注意的是 | Textbook hedge with no speaker behind it | 注意 + the thing, or just the thing |
| 随着…的发展 / 在…方面 / 在…的情况下 | Translated English prepositional frames | Rebuild as topic-comment: put the topic first, bare |
| 希望以上内容对您有所帮助 | Customer-service boilerplate on a personal message | Nothing, or 有问题再问我 |
| Every paragraph the same length, every sentence balanced | Natural Chinese varies wildly: a three-character line next to a forty-character one | Break the rhythm on purpose; leave one fragment |
| 四字格 stacked three or more in a row | 精益求精、锐意进取、开拓创新 is 公文 filler, not writing | One at most, and only where it earns its place (`idioms.md`) |
| Zero 语气词 in a casual message (Rule 4) | The single most reliable signal | Add where the feeling is, not everywhere |
| Bolded key terms and emoji headings in a chat message | Nobody formats a WeChat message | Plain text; line breaks are the only formatting chat has |
| 我们可以看到 / 让我们一起 | Lecture voice from a first-person plural nobody appointed | Drop the frame, keep the observation |
| Perfect 。 at the end of every chat line | Chat drops the final period; keeping it reads as cold or final (`chat.md`) | End on the last character, or a particle |
| An English idiom carried across literally | 一石二鸟 exists; "touch base" and "circle back" have no Chinese and produce nonsense | Name the action: 再对一下 |
| Anything else that feels off but parses | Read it aloud; the sentence a native would not say aloud is the one to rewrite | `proofreading.md` |

## The Register Ladder

Five rungs. Pick by the relationship, then keep it for the whole text — mid-text drift is more visible than starting one rung wrong.

| Rung | Who / where | Address | Particles | Sample opener |
|---|---|---|---|---|
| 极正式 | 公文, 合同, official notice, court, 学术论文 | 贵方 / 各位 / no second person at all | none | 兹通知如下： |
| 正式 | External email, a client, a professor, an older stranger | 您 | none, or 呢 in a question | 王总您好，打扰了。 |
| 客气 | New colleague, a peer at another company, a shop | 你 with 请/麻烦 | 吧, 呢 | 你好，麻烦问一下 |
| 日常 | Colleagues, friends, group chats, most 小红书 copy | 你 | 啊, 呢, 吧, 嘛 | 在忙吗？想问个事儿 |
| 亲近 | Close friends, family, same-age group chat | 你 plus nicknames | all of them, plus slang | 诶你看这个 |

Defaults when nothing is known: 客气 in writing to a person, 日常 on social copy, 正式 in email. `formality` overrides; a stated preference for one person overrides both and gets a `## Recipients` row.

## Word Choice: Safe → Native

The model reaches for the dictionary word. A native reaches for the specific one. Left column is not wrong — it is *flat*, which is what reads as machine.

| Flat | Native, casual | Native, formal | Note |
|---|---|---|---|
| 很好 | 太好了 / 绝了 / 牛 | 非常好 / 十分理想 | 绝了 and 牛 carry age signal (`slang.md`) |
| 不好 | 太差了 / 拉垮 / 坑 | 不理想 / 有待改进 | 坑 means it wasted your money or time specifically |
| 很多 | 超多 / 一堆 / 一大把 | 大量 / 众多 | 一堆 implies untidy volume |
| 非常 | 超 / 巨 / 特别 / 贼 (northern) | 十分 / 极为 | 贼 marks the writer as northern |
| 我认为 | 我觉得 / 我感觉 | 本文认为 / 笔者认为 | 我认为 in a 论文 is a register error (`academic.md`) |
| 是的 | 对 / 嗯 / 是啊 | 是的 | Bare 是的 in chat reads clipped |
| 谢谢你 | 谢啦 / 多谢 / 麻烦你了 | 感谢您的支持 | 麻烦你了 thanks for effort, not for a gift |
| 对不起 | 不好意思 | 抱歉 / 深表歉意 | Weight ladder in `etiquette.md` |
| 一个人 | 有个人 | 一位 + role | 位 is the polite measure word for people |
| 个 (any noun) | the specific 量词 | the specific 量词 | 一条消息, 一张票, 一部电影, 一台电脑, 一家公司, 一门课, 一顿饭 |
| 进行讨论 | 聊聊 / 说一下 | 讨论 | Rule 6 |
| 现在 | 这会儿 / 眼下 | 目前 / 当前 | 这会儿 is spoken and northern-leaning |
| 因为…所以… | just the two clauses | 由于…因此… | Chinese does not need both halves; keeping both is textbook |
| 我不同意 | 我觉得不太行 / 这个可能有点难 | 恐怕难以认同 | Direct disagreement is a register decision, not a default (`etiquette.md`) |

## Output Gates

Before delivering any Chinese text:

- Variant and script settled and consistent end to end, with no mixed-variant vocabulary and every one-to-many character checked (Rule 2)?
- One register for the whole text, matching the recipient's `## Recipients` row if there is one, and the address form unchanged from previous messages to that person (Rule 1)?
- Punctuation full-width throughout, ellipsis ……, dash ——, titles in 《》, quotes matching the variant, `latin_spacing` applied uniformly (Rule 8)?
- Numbers grouped by 万/亿, 两 before measure words, dates and money in the local shape (Rule 3)?
- Run the AI-tell sweep: opener scaffolding, 值得注意的是, uniform paragraph lengths, stacked 四字格, zero particles in casual text?
- 的/地/得 checked at every occurrence, and every 个 that should be a specific 量词 replaced (Rules 6, 7)?
- Every slang term datable and inside `slang_appetite`, and every 成语 checked for its actual meaning rather than its parts (Rule 9, `idioms.md`)?
- Read once aloud in the target register: is there a sentence a native would not say out loud?
- Did anything durable come out of this — a term or name rendered, a native correction, a register decision, a retired slang term, a delivered piece, a template, an environment fact? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/chinese/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| variant | mainland \| taiwan \| hongkong \| singapore | mainland | Vocabulary set, slang source, punctuation defaults and every example in `regions.md`; while unset, name the assumed variant before writing (Rule 2) |
| script | simplified \| traditional \| from-variant | from-variant | Overrides the script the variant implies, for the case of simplified text for a Taiwanese reader or the reverse |
| formality | casual \| neutral \| formal \| auto | auto | Default rung on the Register Ladder when the channel does not settle it; `auto` reads it from the channel |
| address_form | 你 \| 您 \| auto | auto | Second person used when no `## Recipients` row exists; a row for a person always wins (Rule 1) |
| slang_appetite | none \| light \| current \| heavy | light | How much internet language enters output; `none` for official channels or a 50+ audience, `heavy` only when the user has shown they write that way (`slang.md`) |
| pinyin_gloss | none \| new-words \| all | none | Whether output carries pinyin and an English gloss — set to `new-words` when the user is learning, `none` when they are native |
| default_channel | wechat \| xiaohongshu \| weibo \| gongzhonghao \| douyin \| zhihu \| email \| document \| none | none | Channel assumed when a request does not name one; picks the style box and the platform conventions in `social-media.md` |
| latin_spacing | bool | true | Whether a half-width space separates Han from Latin letters and digits; applied to every occurrence or none (Rule 8) |
| crude_ok | bool | false | Whether 卧槽-tier and 牛逼-tier words may appear at all |
| platform_filter_aware | bool | true | Whether to avoid wording that gets a post limited on mainland platforms and offer the 谐音 alternative instead (`social-media.md`) |
| emoji_density | none \| sparse \| native \| heavy | sparse | Emoji and 表情包 per paragraph in chat and social copy; `native` matches the platform norm, which on 小红书 is far higher than on WeChat |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Voice** — how blunt, how warm, sentence length, whether fragments are welcome, self-reference (我 / 本人 / 笔者 / 小编), signature sign-offs — affects every piece and belongs in a `styles/<channel>.md` box once it outgrows a line
- **Conventions** — quote-mark style, whether 星期六 or 周六 or 礼拜六, 元 or 块, 号 or 日, half-width digits in Chinese text, paragraph indent (首行缩进两字) or blank-line separation — affects `punctuation.md` and `numbers-and-names.md`
- **Platform** — which channels the user writes on, their audience age band and region, account type and its limits, whether a piece is read on a phone — affects `social-media.md` and `emoji_density`
- **Relationships** — the standing address form and register for named people and groups — every stated one becomes a `## Recipients` row rather than a config key
- **Risk posture** — appetite for crude words, politically sensitive topics, direct disagreement, humour that could be misread by a superior — affects `etiquette.md` and `platform_filter_aware`
- **Cadence** — slang re-calibration, native review of the style boxes, glossary consolidation, re-check after a platform changes its rules — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Output register** — Chinese only, Chinese plus back-translation, Chinese plus pinyin, whether alternatives are offered by default, how much of the reasoning to show — affects the shape of every answer

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| 呵呵 as friendly laughter | On the mainland it has meant dismissal or contempt for over a decade; sending it to a colleague reads as an insult | 哈哈 / 哈哈哈, matched in length to theirs (`chat.md`) |
| The 🙂 emoji, or 微笑 from the WeChat set | Read as passive-aggressive by most users under about 40; the older generation still means it warmly, which is exactly why it lands badly | 😄, 😂, or a 表情包 (`chat.md`) |
| Opening a message with 在吗 | Puts the reader on the hook before they know the cost; widely resented | Ask the thing in the first message, with the context |
| A 。 at the end of every chat line | Chat punctuation is minimal; a final period reads as cold, angry, or conversation-ending | End on the last character or a particle; keep 。 for paragraphs |
| Machine-converting simplified to traditional | Vocabulary stays mainland and the one-to-many characters break: the converter emits 頭發 for 头发 and leaves 干杯 as 干杯, where 頭髮 and 乾杯 are the right forms | Convert vocabulary too, then re-read the nine characters in Rule 2 (`regions.md`) |
| 二个, 二点钟 | Before a measure word the number is 两 | 两个, 两点钟 (Rule 3) |
| Overusing 您 with a peer | Reads as sarcasm or as putting distance in on purpose | 你 for peers; 您 only up the ladder or on first contact (Rule 1) |
| 亲 as a friendly opener | It is Taobao seller voice; outside e-commerce it reads as a sales script | The person's name, or nothing |
| Adding 哥/姐 to a name without checking | 哥 attached to some given names collides with a product or a meme — 伟哥 is the brand name of Viagra | Use 姓 + 哥/姐 (王哥), or the title (`numbers-and-names.md`) |
| Stacking 成语 to sound educated | Three in a paragraph reads as 公文 filler or as a student showing off | One per paragraph at most, and only where a plain phrase would be longer (`idioms.md`) |
| Reaching for slang to sound young | A dead meme dates the writer more precisely than plain language ever could | Date the term first (Rule 9) |
| Half-width ,.?! inside Chinese text | The most visible non-native mark, and it survives every style edit | Full-width throughout (Rule 8) |
| 谢谢你的来信 / 期待您的回复 as email frames | Direct calques of English business letters; Chinese email has its own skeleton | 您好 → the point → 此致 敬礼 or 顺颂商祺 (`business.md`) |
| 加油 as the answer to any difficulty | Fine for exams and matches, hollow after bad news | Name the specific thing: 有事随时说 / 需要我做什么 |
| Writing ... instead of …… | Three ASCII dots are a Latin ellipsis; Chinese uses two ellipsis characters | …… (Rule 8) |
| Using 、 to join two clauses | 、 lists items inside one clause and nothing else | ，between clauses, 、inside a list |
| A term, name or register decision that lives only in the chat | Re-decided differently next month, and the reader notices the drift before the user does | Glossary row, `## Recipients` row, or `artifacts/`, in the same turn (`memory-template.md`) |

## Where Experts Disagree

- **儿化 in writing.** Northern writers put it in (这儿, 一会儿, 玩儿) and hear its absence as stiff; southern and Taiwanese readers see it as Beijing affectation. The decidable version is the audience, not taste: write it when the reader is northern or the voice is deliberately Beijing, drop it in anything national or formal.
- **Han-Latin spacing.** No national standard requires a space between Chinese characters and Latin words or digits; the dominant web typography convention adds one. Publishers split. Pick with `latin_spacing` and be uniform — mixed spacing looks like a merge conflict, which is worse than either choice.
- **Loanwords and English acronyms.** Mainland technical and office writing carries English acronyms untranslated (PPT, KPI, OKR, APP); Taiwanese writing translates more of them (簡報); purists in both markets object to all of it. Frontier: acronyms the audience uses at work stay in English, consumer-facing copy translates them.
- **欧化中文.** 余光中 and 思果 treat 进行 + noun, long pre-nominal attributives and 被 overuse as damage to be reversed; descriptive linguists point out that a century of translation has naturalised much of it and that some structures now carry meaning nothing else does. Both agree the stacked attributive is unreadable; the argument is over the rest. Rules 5 and 6 take the prescriptive side because the failure mode here is machine-flavoured text, and that is precisely what the prescriptive rules delete.
- **TA for gender-neutral third person.** Written 他 covers mixed and unknown gender by convention; TA (Latin letters) is common online and in HR writing, and reads as internet register or as awkward in print. Brand decision per channel, never a default the writer picks mid-document.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/chinese (install if the user confirms):
- `translate` — when the job is bound to an existing source text in another language
- `traditional-chinese` — Traditional-only writing for Taiwan and Hong Kong readers
- `china` — travelling in the country these texts are read in
- `writing` — the craft of prose itself, once the language question is settled
- `japanese` — the same problem in the neighbouring language

## Feedback

- If useful, star it: https://clawic.com/skills/chinese
- Latest version: https://clawic.com/skills/chinese

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/chinese.
