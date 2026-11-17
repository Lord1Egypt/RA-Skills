---
name: abs-business-system
display_name: "ABS · AI 企业精益经营系统"
display_name_en: "ABS · AI Business System"
description: >-
  Use ABS (AI Business System) to answer and act on lean / operational-excellence work with a curated knowledge
  base built on in-depth study of DBS (the Danaher Business System). Trigger when the user asks about DBS or how
  to apply methods or tools such as 5S, standard work, takt and staffing,
  SMED / changeover, kaizen events, problem solving (PSP, 5 Why, root cause), daily management (SQDIP boards,
  andon, tiered meetings), policy deployment (hoshin, X-matrix, bowler), value stream mapping, TPM / OEE, pull /
  kanban, VOC, sales force, talent development or M&A integration; or wants to search ABS, get an answer with
  sources from ABS, study an ABS course, make an execution plan with a schedule (e.g. "plan a kaizen week",
  "arrange lean training for middle managers"), or diagnose operations data, a document or a shop-floor photo.
  中文：问 DBS（丹纳赫业务系统）、精益与经营体系的方法和工具（5S、标准作业、快速换型、改善周、问题解决、日常管理、方针展开、价值流、TPM、拉动看板等），
  或要查 ABS、问 ABS、学 ABS 课程、做规划、做业务诊断时使用。Search works without an account; the rest needs an ABS access token.
description_zh: >-
  用 ABS（AI 企业精益经营系统）的知识库与工具处理精益与经营管理的事，知识库建立在对丹纳赫业务系统（DBS）的深入研究之上：查方法和工具（5S、标准作业、节拍与配员、快速换型、改善周、
  问题解决与根因、日常管理与安灯、方针展开与保龄球图、价值流、TPM 与 OEE、拉动与看板、客户之声、销售队伍、人才发展、并购整合），
  带出处回答问题，学习 ABS 课程，一句话做出带时间规划的规划书，对生产数据、文档或现场照片做业务诊断。检索不用登录；看整张工具卡、问答、学课程、规划与诊断需要 ABS 访问令牌。
description_en: >-
  Use ABS (AI Business System) for lean and operational-excellence work: look up methods and tools (5S, standard
  work, takt and staffing, SMED, kaizen events, problem solving and root cause, daily management and andon, policy
  deployment and bowlers, value streams, TPM and OEE, pull and kanban, VOC, sales force, talent development, M&A
  integration), answer questions with sources, study ABS courses, turn one sentence into a scheduled execution plan,
  and diagnose operations data, documents or shop-floor photos. The knowledge base is built on in-depth study of
  the Danaher Business System (DBS). Search works without an account; the rest requires an ABS access token.
version: 1.2.1
author: ABS · AI Business System
---

# ABS · AI Business System

ABS is an operating system for running a business the lean way: a curated knowledge base of tool cards,
terms, forms, courses and rules, plus planning and diagnosis built on it. This skill lets you use it from here.
Answers come from the ABS knowledge base, not from general knowledge — that is the point of calling it.

ABS is an independent product, not affiliated with, sponsored or endorsed by Danaher.
ABS 为独立产品，与丹纳赫无隶属、赞助或背书关系。

All commands run the bundled script: `python3 scripts/abs.py <command> …` (path relative to this skill's folder;
Python 3.8+, no packages needed). Add `--json` to any command for the raw response.

## First use

**`search` works right away, with no account or token** — run it first for any question in scope and answer
from what it returns. The other commands (`card`, `ask`, `courses`, `course`, `plan`, `diagnose`, `page`) need
the user's ABS access token:

1. Run `python3 scripts/abs.py whoami` to see whether a token is connected.
2. If there is none (or it was rejected) and the user needs more than search, ask them:
   “Please create an access token in ABS → **Personal Settings → Access tokens**, copy it, and paste it here.”
   中文：「请在 ABS 的**个人设置 → 访问令牌**里生成一个令牌，复制后发给我。」
3. Run `python3 scripts/abs.py login <token>`. It checks the token and saves it in the user's config file
   (readable only by the user). **Never repeat the token back in the conversation.**

Without a token, still help: search (several phrasings if the first finds little), then answer from the titles,
excerpts, basis labels and links it returned. Say that the excerpts are short and that the whole tool card,
cited answers, plans and diagnoses need a token — do not stop at asking for one.

The site address is already set to the ABS site this skill was downloaded from. Only for a private deployment
pass `--base-url https://…` to `login`.

## When to use it

| The user wants to… | Command |
|---|---|
| Know how a method or tool works, what the rules or formulas are, where to start | `search`, then `card <id>` for the full tool card |
| Check where a number or rule comes from | `card <id>` (sources, rule basis, pages), then `page <pdf> <n>` for the original page |
| Get an answer grounded in ABS materials, with sources | `ask "<question>"` |
| Study: which course fits, what a lesson covers, practise a lesson | `courses`, `course <id>` |
| Plan something: a kaizen week, a training program, a transformation, hiring a key role … | `plan "<what they want to achieve>"` |
| Assess a situation: production records, a report, a shop-floor photo, a described problem | `diagnose "<question>" [--file PATH]` |

`search` returns a short snippet around the match — enough to choose what to open, not the full text. Open the
card (or the source page) for the real content. With a token, the first 100 searches a day are free and each one
after that costs 1 credit; without a token, searches are capped per network address per day. Either way, search
with intent instead of sweeping the library.

Do **not** use it for unrelated tasks (general coding, travel, chit-chat) or when the user asks for your own
opinion without ABS. More examples: `references/tasks.md`.

## Commands

```bash
python3 scripts/abs.py whoami
python3 scripts/abs.py search "SMED 换型时间怎么压" --limit 8
python3 scripts/abs.py card smed
python3 scripts/abs.py page DBS教材34_DBS系统导入.pdf 102
python3 scripts/abs.py ask "How do I set the takt time for a new cell?"
python3 scripts/abs.py courses
python3 scripts/abs.py course tutorial-22-smed
python3 scripts/abs.py plan "下周开一场改善周，提升 L1 线的一次合格率" --start 2026-10-12
python3 scripts/abs.py plan-get DRF-20261012-0001
python3 scripts/abs.py plan-list
python3 scripts/abs.py diagnose "Why do we keep missing daily output?" --file line1-hourly.xlsx
```

Language follows the text you pass (Chinese in → Chinese out; English in → English out). Override with
`--lang zh|en`, e.g. when the user writes in English about a Chinese document. `card`, `courses`, `course` and
`plan-list` take no text to go by and default to English: pass `--lang zh` when the user writes Chinese.

## How to answer

- Build the answer on what ABS returned. Keep its citations (`[1]`, `[Source 1]`, `[来源1]`) and list the sources
  with their links at the end. If ABS has nothing relevant, say so instead of filling in from memory.
- **Label what you use.** ABS tags rules and sources with their basis, and so should you:
  - 教材口径 / textbook — stated in the source course material (a page can be fetched to check it);
  - 行业标准 / industry standard — not in the textbook, or taken from a non-Danaher source;
  - ABS 设计决策 / ABS design decision — ABS's own judgement, not the textbook's;
  - 待客户校准 / to be calibrated — the method is given but the number must be set per customer;
  - 非丹纳赫外部件 / non-Danaher external source — material from another company.
  Anything ABS did not return is your own knowledge: mark it as yours, never cite ABS for it.
- **To verify a number or rule**, read `card <id>`: the card text and the rule notes explain corrections (for
  example why a total of 36 in the source is a typo), and the card lists its sources and the pages you can fetch;
  then `page <pdf> <n>` saves that one original page as an image. Single pages only, about 40 per minute.
- `plan` returns a plan built from the ABS knowledge base, in Markdown (phases, steps, schedule, forms, sources)
  with a link. Its **Coverage and gaps** section says what ABS covered, what the knowledge base has but this plan
  leaves out (it can be planned from ABS separately), what is **not in the knowledge base** (plan those separately
  and say they are not from ABS) and which parts are defaults (e.g. a default number of weeks). A **Date checks**
  section lists milestones that were moved because they fell before today or on a public holiday, and a **Review**
  section lists what the server-side review changed (week themes only) and what a person should check.
  Keep those statements in your answer. The plan is saved as a **draft**: tell the user to review it in ABS and submit
  there — submitting is what creates projects and tasks. Show the key parts rather than pasting everything.
- `diagnose` sends the question and the file to ABS and its AI model. Ask before sending anything confidential.
  Add `--save` to keep it in the user's diagnosis records.
- Errors: `401` → the token is invalid, revoked or expired: ask the user for a new one and `login` again
  (search also works with no token at all).
  `403` → the account's role cannot do this (read-only accounts cannot plan). `429` → too many calls; wait and retry.
  `402` → the account is out of ABS credits for this step: tell the user, do not retry in a loop.
  `503` → the ABS AI model is temporarily unavailable; `search`, `card` and `courses` still work.

## Privacy

The token acts as the user: same permissions, same visibility, same expiry as their ABS account, and it only
works on the ABS agent API. The user can revoke it at any time in Personal Settings → Access tokens.
