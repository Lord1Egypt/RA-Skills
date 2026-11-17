# AI Tells — Removing the Machine Fingerprint

The summary table is in SKILL.md. This is the sweep, in the order that finds the most damage per pass, plus the rewrites.

**Contents:** [Run It In This Order](#run-it-in-this-order) · [Pass 1 — Structure](#pass-1--structure) · [Pass 2 — Frame Phrases](#pass-2--frame-phrases) · [Pass 3 — Rhythm](#pass-3--rhythm) · [Pass 4 — Particles and Fragments](#pass-4--particles-and-fragments) · [Pass 5 — Word Temperature](#pass-5--word-temperature) · [Pass 6 — Format](#pass-6--format) · [Worked Rewrite](#worked-rewrite) · [Tells That Are Not Tells](#tells-that-are-not-tells) · [What Gets Written Down](#what-gets-written-down)

## Run It In This Order

Structure first, vocabulary last. Polishing words in a machine-shaped text produces a well-dressed machine.

| Pass | Looking for | Cost of skipping |
|---|---|---|
| 1 Structure | 首先/其次/最后, numbered scaffolding, a summary paragraph | The text reads as an essay regardless of its words |
| 2 Frame phrases | 值得注意的是, 随着…的发展, 在…方面 | Each one is individually deletable and collectively fatal |
| 3 Rhythm | Uniform sentence and paragraph length | The most subtle tell and the hardest to fake |
| 4 Particles | Zero 语气词 in casual text | The most reliable single signal (SKILL.md Rule 4) |
| 5 Word temperature | Dictionary word where a specific one exists | Flat, not wrong |
| 6 Format | Bold, headings, emoji bullets where the channel has none | Marks the text as pasted from a chat window |

## Pass 1 — Structure

| Delete | Replace with |
|---|---|
| 首先…其次…再次…最后 | Nothing, or 先…然后… once, or just the sentences in order |
| 总之 / 综上所述 / 总的来说 | Nothing. If a conclusion is needed it goes first (`business.md`) |
| A closing paragraph that restates the opening | Delete outright |
| 以下几点 / 分为三个方面 announced before the points | The points |
| Symmetric sections of equal weight | Let one section be three times longer because it deserves to be |

The underlying error is that the model writes an *exposition* when the situation calls for a *message*. A WeChat message, a 小红书 note and a 汇报 are none of them essays; only 知乎 and academic writing want visible structure (`social-media.md`, `academic.md`).

## Pass 2 — Frame Phrases

| Frame | Why it reads machine | Rewrite |
|---|---|---|
| 值得注意的是 | Hedged authority with no speaker | 注意 + the thing, or the thing alone |
| 需要指出的是 | Same | Same |
| 随着…的发展 | Translated English scene-setting | Start at the fact |
| 在…方面 / 在…情况下 | Prepositional frame Chinese does not need | Topic-comment: 成本这块，… |
| 对…进行… | Rule 6 (`grammar.md`) | The verb |
| 通过…的方式 | Three characters doing one character's work | 用 / 靠 / by naming the method |
| 起到了…的作用 | Nominalised verb | The verb: 帮了大忙 |
| 具有重要的意义 | Says nothing | Delete, or say what it changes |
| 让我们一起来看看 | Lecture voice | Delete |
| 希望以上内容对您有所帮助 | Support-ticket boilerplate | 有问题再问我, or nothing |
| 作为一名… | Self-introduction nobody requested | Delete |
| 不仅…而且… as the default connector | Textbook parallelism | Two sentences |

## Pass 3 — Rhythm

Natural Chinese varies violently in sentence length. Machine Chinese does not.

- Count characters in consecutive sentences. If five in a row land within a narrow band, break the pattern deliberately: put a four-character fragment next to a forty-character sentence.
- Paragraph length is the same test at the next level up. A message where every paragraph is three lines was generated, not written.
- Leave one sentence unfinished or fragmentary where the register allows it (`chat.md`, `social-media.md`). Fragments are native and the model avoids them.
- Repetition is native: 真的真的很好, 特别特别累. The model deduplicates and loses the emphasis.

## Pass 4 — Particles and Fragments

- Casual text, roughly one 语气词 every three or four short sentences; the particle goes where the feeling is, never on every line (SKILL.md Rule 4).
- Formal text takes none — adding 吧 to a 通知 is the opposite failure and just as visible (`register.md`).
- 就, 才, 都, 还, 也 as tone adverbs are the quieter half of this: 我就说嘛, 都这个点了, 还挺好的. Machine Chinese drops them because they are grammatically optional and pragmatically mandatory.
- Interjections open real messages: 诶, 哎, 嗯, 那个, 话说, 对了. One at the top of a casual message does more than any vocabulary change.

## Pass 5 — Word Temperature

The Word Choice table in SKILL.md is the short version. The rule behind it: **the model picks the word with the widest coverage; a native picks the word with the narrowest fit.** 很好 covers everything, which is why it says nothing.

Additional swaps that specifically mark machine origin:

| Flat | Native |
|---|---|
| 进行沟通 | 聊 / 说一下 / 对一下 |
| 存在问题 | 有问题 / 出问题了 |
| 予以解决 | 解决 / 处理掉 |
| 较为重要 | 挺重要 / 很关键 |
| 目前来看 | 现在看 / 看着 |
| 相关人员 | 谁谁谁, by name |
| 该问题 | 这个问题 / 这事儿 |
| 众所周知 | Delete |

## Pass 6 — Format

- No markdown in chat (`chat.md`). No bold in a WeChat message; the client does not render it and the asterisks arrive literally.
- No emoji as list bullets outside 小红书 and similar (`social-media.md`).
- No headings in a message shorter than a page.
- Half-width punctuation and ASCII quotes are a machine tell as much as a typography error (`punctuation.md`).
- Numbered lists with `1.` in formal Chinese documents where 一、 is expected (`documents.md`).

## Worked Rewrite

Machine draft, meant as a WeChat message to a colleague:

> 你好，关于明天的会议安排，我想和你进行一下沟通。首先，会议时间定在下午三点。其次，会议地点在三楼会议室。最后，希望你能够提前准备相关材料。如有任何问题，请随时与我联系。谢谢。

Diagnosis: essay scaffolding (Pass 1), 进行沟通 and 相关材料 (Passes 2 and 5), four sentences of identical length (Pass 3), zero particles (Pass 4), formal closing on a peer message (Pass 6, `register.md`).

Rewrite:

> 明天的会开三点，三楼会议室
> 你那边的材料能先准备下吗
> 有问题随时说

Three messages instead of one paragraph, no final 。, the ask in its own line, and the closing replaced by something a person would type. Length dropped by more than half and nothing was lost — which is the usual result, and is itself a check: if the de-machined version is not shorter, the pass was cosmetic.

## Tells That Are Not Tells

Things that look like machine output and are not, so they do not get "fixed":

- **Formal 书面语 in a 公文 or a 论文.** 兹, 予以, 现将…通知如下 are correct there and only there (`documents.md`, `academic.md`).
- **Structure on 知乎.** Numbered arguments are the platform's native form (`social-media.md`).
- **四字格 in a speech.** Parallel four-character phrases are genuine oratory rhythm when spoken aloud (`speaking.md`); they only read as filler on the page.
- **Repetitive politeness in service register.** 好的好的, 没问题没问题 from a shop or a seller is real, and flattening it makes the text colder, not more human.
- **English acronyms in mainland office writing.** PPT, KPI, OKR are what people say (`regions.md`).

## What Gets Written Down

- **A tell a native reader flagged in the user's text** → `### Corrections`, with the phrase and the accepted rewrite. The reader's own list beats this page.
- **A phrase the user habitually reaches for that reads machine-made** → `### Corrections` too, so the same edit is not re-made every session.
- **A piece that was called out as AI-written** → `## Pain Points` with the passage, because the specific tell that got noticed is worth more than the general list.
