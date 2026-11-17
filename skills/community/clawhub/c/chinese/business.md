# Business — Email, Workplace, and Client Chinese

**Before writing to a colleague, a client or a 甲方 contact**, read their `## Recipients` row in `~/Clawic/data/chinese/memory.md` and any `artifacts/` template its `## Boxes` index names for this document type. A 请假条 or a 汇报 skeleton that was accepted once should never be rebuilt from scratch.

**Contents:** [Email Skeleton](#email-skeleton) · [Openers and Closings](#openers-and-closings) · [汇报 — Reporting Upward](#汇报--reporting-upward) · [通知 — Internal Announcements](#通知--internal-announcements) · [Client and 甲方 Language](#client-and-甲方-language) · [Saying No, Late, or Not Yet](#saying-no-late-or-not-yet) · [Meetings](#meetings) · [Workplace Vocabulary That Signals Fluency](#workplace-vocabulary-that-signals-fluency) · [What Gets Written Down](#what-gets-written-down)

## Email Skeleton

Chinese business email is shorter than its English equivalent and front-loads the conclusion. The skeleton is fixed; the body is not.

```
称呼：      王总，您好：            ← title + 您好, then a colon, on its own line
正文：      结论 → 依据 → 请求      ← the ask arrives in the first two lines, not the last
附件：      附件为…                 ← named, because clients open the mail on a phone
结束语：    此致                    ← own line, 缩进两字 (or run on after the last sentence)
            敬礼                    ← next line, 顶格: flush left, never indented (`documents.md`)
署名：      张伟                    ← name
            2026年7月26日           ← date, Chinese format
```

- The subject line carries the action and the deadline: 【报价】Acme项目报价单（需7月30日前确认）. Bracketed tags at the front are standard and are how the reader triages.
- 首行缩进两字 (two-character first-line indent) is expected in formal Chinese documents and increasingly dropped in email in favour of blank lines between paragraphs. Follow `conventions.paragraph` in `config.yaml`; be consistent within the document.
- No greeting paragraph. 希望您一切都好 is a translated English opener and reads as filler.

## Openers and Closings

| Slot | Formal | Neutral | Note |
|---|---|---|---|
| 称呼 | 尊敬的王总： | 王总，您好： | 尊敬的 is for external, senior, or ceremonial |
| First line | 您好。关于…，现汇报如下： | 您好，关于X，结论是… | State the topic in the first six characters |
| Apology for the interruption | 冒昧打扰，还请见谅 | 打扰了 | Once per email at most |
| Chasing | 不知此事是否方便推进？ | 想跟您确认下进度 | Never 请尽快回复 to someone senior |
| Closing formula | 此致 / 敬礼 | 顺颂商祺 (business) · 顺颂时祺 (general) · 祝好 (light) | One only; stacking them is a form-letter tell |
| Sign-off | Full name + date | Given name or 姓名 | The date is part of the formal closing, not decoration |

Do not use: 谢谢你的来信 (calque of "thank you for your email"), 期待您的回复 (calque of "looking forward to hearing from you" — Chinese uses 静候佳音 formally or nothing at all), 请查收 as a whole message body without saying what is attached, or 以上，谢谢 to a superior (以上 alone is a Japanese-influenced register that reads as curt on the mainland).

## 汇报 — Reporting Upward

**结论先行.** The first sentence is the conclusion or the ask. A Chinese manager reading on a phone will not scroll to find it, and burying it reads as evasion — which is worse than bad news.

Standard shape, in this order:

1. **结论** — one sentence. 项目可以按原计划上线 / 需要延期一周。
2. **依据** — two or three lines of evidence, numbers first.
3. **风险** — what could still break, named, with the mitigation.
4. **需要的支持** — the exact ask: who, what, by when. A 汇报 with no ask reads as a status broadcast, and a status broadcast that hides an ask reads as manipulation.

Numbers in a 汇报 use 万/亿 grouping and carry their unit and period (`numbers-and-names.md`): 本月新增用户 3.2万，环比增长 12%.

Never report a problem without the 方案. 出了个问题，您看怎么办 hands the work upward; 出了个问题，我建议 A 方案，需要您拍板 hands upward only the decision.

## 通知 — Internal Announcements

Fixed skeleton, no particles, no 我:

```
关于X的通知

各位同事：
    因<原因>，现将<事项>通知如下：
    一、<时间/范围>
    二、<要求>
    请相互转告。

                                            <部门>
                                            <YYYY年M月D日>
```

- 请相互转告 or 特此通知 closes it. 谢谢大家 does not — a 通知 is not a request.
- Numbered items use 一、二、三、 with the 顿号 built in, never `1.` in Chinese formal text (`punctuation.md`).
- A 通知 announces a decision. If the reader can decline, it is a 邀请 or a 征求意见, and calling it a 通知 will be resented.

## Client and 甲方 Language

- 甲方 is the commissioning party, 乙方 the supplier. In conversation they are used metonymically — 甲方又改需求了 is a complaint any Chinese professional understands instantly.
- 对接人 is the named counterpart on the other side; asking 咱们这边对接人是谁 is the normal way to find out who to talk to.
- 贵公司 / 贵司 for the other company, 我司 / 我们 for your own. 贵司 in email is standard and not stiff.
- 需求 covers requirement, request and scope. 需求变更 is scope change; naming it that in writing is how a schedule slip becomes defensible later.
- Prices: 含税 or 不含税 must be stated, always. 报价 without 含税 status invites a re-negotiation.
- 走流程 (go through the process), 走合同 (get it contracted), 打款 (pay), 回款 (collect payment), 开票 (issue a fapiao) — using the verb the client uses is what marks the writer as inside the industry rather than translating into it.

## Saying No, Late, or Not Yet

Direct refusal in a business thread costs face on both sides. The ladder, weakest to strongest (full treatment in `etiquette.md`):

| Phrase | Actually means |
|---|---|
| 我们再看看 / 我先了解一下 | No, softly |
| 这个可能有点难 | No, with a reason available on request |
| 恐怕不太方便 | No, and do not push |
| 目前的排期确实排不开 | No, with a resource reason that leaves the door open |
| 这个我们做不了 | No, final — reserved for when the soft forms have failed |

For a delay: name the new date in the first sentence, then the cause, then what is being done. 因为…所以可能会晚一点 with no date is the version that destroys trust.

For bad news to a client: 情况同步一下 as the subject, conclusion first, then 我们的处理方案, then 造成的影响. 深表歉意 belongs at the end, once — a paragraph of apology reads as an attempt to substitute apology for a fix.

## Meetings

- 会议纪要 (minutes) are the deliverable, not the notes. Shape: 时间/地点/参会人 → 结论 → 待办（谁、什么、什么时候）→ 待确认事项. The 待办 table with owners and dates is the only part anyone re-reads.
- 拉个会 / 约个会 (schedule a meeting), 对一下 (align), 过一遍 (walk through), 拍板 (make the final call), 复盘 (retrospective), 同步 (bring up to date), 跟进 (follow up), 闭环 (close the loop).
- 复盘 is culturally loaded: it is a blameless review in some companies and a search for a responsible party in others. Ask which before writing one.
- Invitations state the 议题 and the expected 时长. A meeting invitation with no agenda gets declined politely and resented quietly.

## Workplace Vocabulary That Signals Fluency

| Concept | Native term | Note |
|---|---|---|
| Overtime | 加班 | 996 and 大小周 name specific schedules |
| Performance review | 绩效 / 考核 | 打绩效 is the act of rating |
| Headcount | 编制 / HC | HC is used untranslated in mainland tech |
| Promotion round | 晋升 / 答辩 | 答辩 is the defence presentation |
| Onboarding an employee | 入职 | 新手引导 is product onboarding, never people |
| Leaving | 离职 · 提离职 (announcing) · 交接 (handover) | 裸辞 means quitting with nothing lined up |
| Escalate | 升级 / 拉上领导 | 拉上领导 is blunt; use it deliberately |
| Blocker | 卡住了 / 卡点 | 卡在X那边 names where without naming a person as at fault |
| Slide deck | PPT | Untranslated on the mainland; 簡報 in Taiwan (`regions.md`) |
| Alignment meeting | 对齐 / 拉齐 | 对齐 has spread from tech into general office use |

## What Gets Written Down

- **A document skeleton that was accepted unchanged** — a 请假条, a 汇报 shape a manager liked, an email format a client answers → `artifacts/template-<what>.md` with the date and who accepted it, and its `## Boxes` line in the same turn. Templates are the highest-reuse artifact this domain produces.
- **A title, address form or register decision for a colleague or client** → their `## Recipients` row, keyed by contacts key; the person themselves goes in the shared contacts box.
- **Industry or company vocabulary the user's workplace actually uses** — the verb for paying, the name of the promotion round, whether 复盘 is blameless → `### Terms` in the glossary. Getting the in-house word right is a stronger fluency signal than grammar.
- **An email or a 汇报 that landed badly** → `## Pain Points` with the cause, and the piece itself as a row in `pieces/<year>.md` with how it landed.
