---
name: copy-studio
description: 'Use when a community post, comment reply, social caption, landing-page module, deck slide, ad, or email needs to go from a brief to finished, human-sounding copy. Also use when the request is "run my copy workflow", "full copy pipeline", "take this from brief to final", or "brainstorm then write then polish". For a single stage only (just write, just polish, just de-AI, just translate), use that skill directly.'
compatibility: "Orchestrator only — it bundles none of the skills it calls. Install separately: brainstorming, writing-plans, copywriting, copy-editing, humanizer. Optional: a localization skill for Stage 6."
metadata:
  version: "3.0.0"
---

# Copy Studio

One entry point that takes a piece of copy from strategy to final, stopping after each stage for the user to approve.

| Stage | Skill | Output |
|---|---|---|
| 0 Intake | you | copy type, channel, target language, source material |
| 1 Strategy | `brainstorming` | brief: goal, target user, pains, desires, result-oriented value proposition |
| 2 Framework | `writing-plans` | block-by-block outline, each block carrying one pain or desire |
| 3 Draft | `copywriting` | copy in the shape of the type's recipe |
| 4 Polish | `copy-editing` | Seven Sweeps line edit |
| 5 De-AI | `humanizer` | final copy in the source language |
| 6 Localize (conditional) | your localization skill | the channel-language version |

## Three principles

1. **Result-oriented is the spine of every piece:** target user → pain (what they fear, where they're stuck) → desire (what they want) → show the concrete benefit they get. Never a feature list. The copy type only decides the shape; the content always comes from this chain.
2. **The copy is the deliverable.** Gates, framework and image direction all serve the words. Spend the effort on the words first.
3. **The process is general; the recipes are a starting point.** Tune the recipe library and your reference files to your own brand and channels.

## Bring your own references

This skill ships with no brand facts, stats, reward figures or sample copy. Before real work, fill in `references/channel-calibration-template.md` (or your own copy of it):

- **Fact base (§FB)** — the only citable source for stats, capabilities, URLs, pricing and reward figures. Quote it verbatim. Anything missing is `TBD`, never a guess.
- **Channel calibration (§A–§L)** — 2–3 approved real samples per channel you ship to. They teach shape and voice better than any description.

"Cite the fact base" below always means that file. With no fact base yet, every number in a draft is `TBD` and gets raised at the gate.

## Language

- **Working language** — everything said to the user and reviewers (intake, brief, outline, gate menus, reasoning, notes) stays in the language the user is talking in.
- **Deliverable language = the channel's language, locked at Stage 0.** A reply's language follows the post it answers.
- **Third language** (the channel's language differs from the one you draft in): run Stages 1–5 in the source language to get an approved master, then localize at Stage 6. Translation happens only at Stage 6; writing straight into the target language from Stage 1 loses the strategy work and reads as translationese.
- **One channel, one language.** A single comment, post, ad or page is localized into its channel's one language. Multi-language output is only for jobs that span markets (site-wide strings, blog, SEO metadata) or when the user names the languages.
- **Every deliverable gets a working-language note** beside it: what each line does and why, so a reviewer who can't read the target language can still give feedback. The note supports the copy and never edits it.

## Gates (hard rule)

Stop after every stage and wait for the user to pick from the menu.

**The strategy gate has no exceptions, not even for a one-line comment.** The turn that shows the strategy contains no draft, no candidate copy, no finished deliverable. Writing copy before the user approves the direction means deciding the angle for them, which is the worst failure of this skill. If you're about to show strategy and copy in one turn, show only the strategy.

Scale the number of gates to the job; never drop a stage:

- **Big job** (whole page, deck, campaign): multi-turn dialogue for Stages 1 and 2, then a gate after every stage — five in all.
- **Small job** (one card, post, comment, caption, ad): at least two gates, in two separate turns.
  - **Gate 1 · direction** — only the compressed strategy and a one-line structure. No copy. Stop and wait.
  - **Gate 2 · finished copy** — after approval, run 3→4→5 (and 6 if needed) in one pass and present the result, stating "polished + de-AI'd" (and "localized" if it was). A raw draft is never the deliverable.

Gate menu, every time:

> **Stage N complete.** [output]
> ✅ Approved, continue to Stage N+1 · ✏️ Change something (say what) · ⏪ Redo this stage · ⛔ Stop here

On a small job's Gate 1, the first option reads "✅ Approved — deliver the finished copy (polished + de-AI'd)". After Stage 5: if localization is needed, "continue" goes to Stage 6; otherwise Stage 5 is final and the menu doesn't mention Stage 6.

## Constraints when borrowing brainstorming and writing-plans

Both are written for software work. Used as-is they talk architecture, write test tasks, save specs to `docs/superpowers/` and run `git commit`. Borrow only their thinking discipline (one question at a time; a structured outline before writing), and tell them when you invoke them:

- The output is a copy strategy brief / copy outline, kept in the conversation. Save a file only on the user's request, and never under a `superpowers` path.
- No architecture, components, data flow, tests, code blocks, file-path tasks or git commits.
- Stop at the gate; don't chain into the next skill.

## Stage 0 · Intake

One exchange:

- **Copy type** → picks the Stage 3 recipe (see the library). For social, the platform. Types not in the library get their six fields filled live.
- **The asset and goal in one line**, e.g. "an acquisition post for the new template library".
- **Size** — small or big job; sets the number of gates.
- **Channel and target language** — per *Language*; also decides whether Stage 6 runs.
- **Source material** — product brief, feature notes, screenshots, prior copy, reviews; or infer conservatively from the product name and category.
- **State the grounding rule back:** every claim traces to the source or fact base; gaps are `TBD`; nothing is invented.

Then say which stage you're starting at (Stage 1 by default; see *Entering mid-pipeline*).

## Stage 1 · Strategy · `brainstorming`

Tell it: "This is marketing copy; the output is a copy strategy brief." Run its one-question-at-a-time dialogue, offer 2–3 positioning angles, and produce:

- **Goal** — acquisition, selling points, traffic, conversion, education… pick the real one
- **Target user** — a specific segment
- **Pains** — what goes wrong, where they're stuck, what they fear
- **Desires** — what they want to achieve, sell or prove
- **Value proposition** — the result they get (you get / you avoid / you can now…)

## Stage 2 · Framework · `writing-plans`

Tell it: "The implementation plan here is the copy outline for this channel." List the blocks (modules for a landing page, slides for a deck, beats for a post), each with its job, the one pain or desire it carries, its result-oriented message and a rough length. The through-line is usually hook → value → proof → CTA, adapted to the channel. Every block traces back to the Stage 1 brief.

## Stage 3 · Draft · `copywriting`

Write on the approved framework, in the source language, in the shape of the type's recipe. Principles: benefits before features, specific beats vague, the customer's words, one idea per block.

**Routing.** If you maintain skills for specific artifacts (a full-page architecture skill, a catalog-row skill, a platform-specific comment skill), list the routes here. Anything unrouted stays in `copywriting`.

**Pre-show self-check** (run silently, fix failures in place, don't show the list):

1. **Voice** — plain, confident, concrete; benefit plus the mechanism that earns it; no revolutionary / seamless / effortless / unleash / game-changing.
2. **Grounding** (hard stop) — every number, reward and capability traces to the fact base or source; anything else is `TBD`.
3. **Shape** — matches the recipe; required parts present, nothing bolted on.
4. **Length** — inside the recipe's budget, no padding.
5. **No AI tells** — no em-dash overuse, forced triads, "not X but Y", delve / leverage / robust / elevate / foster.
6. **Copy first** — image and layout direction come after the words; words-only types say none.
7. **Channel rules** (hard stop) — Reddit: zero links and hashtags in the body, no rewards in the brand's main comment; emoji only on social and community; clean output, emphasis marked with 【】, never raw HTML.
8. **Language** — the copy is in the right language (the source-language master for third-language channels); every deliverable has its working-language note; conversation stays in the working language.

When a failure needs a missing fact, mark `TBD` and raise it at the gate.

## Stage 4 · Polish · `copy-editing`

Run the Seven Sweeps. Enhance, don't rewrite; keep the message and the claims the brief supports. When the user brings their own draft and enters here, keep its structure and information; the calibration samples guide tone and CTA placement and are never pasted in whole sentences.

Neither Stage 4 nor Stage 5 may add a new capability or result claim. After editing, run the Stage 3 grounding check again.

## Stage 5 · De-AI · `humanizer`

Remove AI tells so it reads like a real person or brand. If the user has a voice sample (past posts, a brand guide, a page that sounds right), pass it to humanizer.

Without localization this is the final deliverable: the copy, its working-language note, and one line on how it differs from the polished version. With localization, it's the master for Stage 6.

## Stage 6 · Localize (conditional)

**Runs only when the channel's language differs from the source language, and only into the one language locked at Stage 0.**

Hand the localization skill: the approved Stage 5 master, the locked target language, and the brief's target market and audience. Tell it: "This is finished, on-strategy marketing copy; localize it into [language], keeping the result-oriented message and voice." Localization means per-market search terms, consistent terminology, brand voice, and per-language length and format, with uncertain local terms flagged.

- Don't run humanizer on the localized text; target-language voice belongs to the localization skill, and an English de-AI pass would damage it.
- Each language version gets its own working-language note plus the flagged uncertain terms.
- The master may be attached for reviewers, headed "Source master (for reference, not for publishing)".
- Gate: present per language and wait. This is the final deliverable.

## What travels between stages

The Stage 1 brief is the spine. Restate its relevant slice whenever you invoke a later stage so the sub-skill stays on strategy. Framework feeds Stage 3, draft feeds 4, polished copy feeds 5, and the master plus target language and market feeds 6. No later stage may introduce a claim the brief doesn't support.

## Entering mid-pipeline

- Clear brief already → start at Stage 2.
- A draft to finish → start at Stage 4.
- Just de-AI → use `humanizer` directly.
- Final copy that only needs another language → start at Stage 6; a plain translate or fix-the-translation job with no pipeline context goes straight to the localization skill.

What the user already has stands in for the earlier stages, and gates run as usual from the entry stage on. When entering at Stage 4, first state in a sentence or two who the copy is for and the benefit it must land, as the basis for the polish.

## Recipe library

The Stage 3 draft must take the real shape of its type. Every type is described by the same six fields:

1. **Shape** — the parts and how many
2. **Must-include** — the 1–3 beats this type always carries
3. **Length & voice** — size budget and any shift from house voice
4. **CTA / link** — what the reader does next and where the link goes; none if none
5. **Grounding** — the same for every type (traceable claims, `TBD` for gaps), so the table omits it
6. **Visual** — only for types that ship with one, added after the words; words-only types say none

**House voice:** plain, confident, concrete (benefit + mechanism), a real number when there is one, no hype. Emoji only on social and community; nothing else (email, print, deck, landing page, video, descriptions) uses them unless the user asks.

**Rules for every recipe:**
- **Links are user-supplied.** A type with a link gets one `[link]` slot, never marked `TBD`, never an invented URL. Reddit is the exception: no link in the body.
- **Clean output.** No HTML or stray markdown in a deliverable. Mark emphasis with 【】 or a short `red: …` note.
- **A/B variants** only on the user's request or there's a real strategic fork: label them `Option A` / `Option B`, change exactly one testable lever per variant (hook, angle, CTA, segment), name the lever in one line, cap at three. Ads, captions, emails and video covers are the usual candidates.

| Type | Shape | Must-include | Length & voice | CTA / link | Visual | Sample |
|---|---|---|---|---|---|---|
| Landing-page value module card | title 3–5 words (a second option only on a real fork) + one description sentence | result in the title; benefit first, then mechanism | one sentence, no emoji | none | image direction (below) | §A |
| Community seeding post | emoji hook (often a question) → one or two lines on what it is → 3–4 ✅ benefits → `[link]` → engagement question | first-person "found this" register | post length, conversational, emoji ok | one `[link]` | none | §C |
| Community invite comment | 3–5 sentences: one concrete detail of their work → light bridge → one concrete reason to join → soft invite | open on a concrete physical detail (their name is fine); warm host voice; no stacked slogans from their caption | 40–70 words, ≤1 emoji | soft invite + `[link]` | none | §G |
| Contest invite comment | praise the work → invite to the contest → the prize → how to join | name the contest and prize from the fact base; Reddit variant drops the prize | short comment | join steps + `[link]` | none | §D |
| Creator recruitment comment | praise the work → invite them to publish → the reward or program | Reddit variant drops rewards, peer voice | short comment | publish invite + `[link]` | none | §E |
| Support / objection reply | thank → acknowledge the concern → your stance → point to the in-product action | calm, respectful, not defensive, no over-promising | 3–6 sentences | in-product report / feedback | none | §F |
| Deck slide | launch: slogan headline + transformation subhead + demo + proof footer · product spotlight: product-name headline + subhead + demo + proof (real number or `TBD`) · partner deck: showcase cards (name + one benefit sentence) | one idea per slide, matched to audience and scope | no paragraphs; proof uses a real number | usually none | product demo / card grid | §B |
| Video cover overlay | 2–3 big lines: transformation hook + one standalone value line | second-person "your"; before→after curiosity; ≤4 words per line | very short, legible at thumbnail size, no emoji | none | over the "after" frame; highlighted words in 【】 | §I |
| Social promo caption | one hook line + brief context + light CTA | benefit before feature, one idea; one caption per platform, never shared | sized to the platform; group posts drop hashtags and use the seeding-post register; emoji ok | inline `[link]` where feed links are clickable; on Instagram-style platforms the CTA points to the bio and the link lives there; one tracked link per channel | optional | §L |
| Template email | full: "What if…" hook → 3–4-sentence body → 3 product images + names → How It Works → link · compact: one 3–4-sentence paragraph + image spec + link | body names the product + a one-line capability + a bolded 2–3-scenario parallel; vary the hook and transition line every send | email voice, no emoji, no padding | one CTA → `[link]`; every CTA, name and image points to it; UTM user-supplied | 3 product images in different styles + 1 how-it-works GIF, sized to your email tool's spec | §K |
| Email | subject + preview (a matched pair) → one-idea body → one CTA | one segment, one job; win-back leads with what changed since they left, no guilt | benefit-led, no feature dump | one CTA + `[link]` | none | — |
| Ad (Meta / Google) | line-one hook that survives truncation + benefit + mechanism + one CTA; headline ≤5 words | hook in line one; headline names the outcome | platform character limits | one `[link]` or button | optional | — |
| Full landing page | hero → how-it-works → features → cards → FAQ → CTA | — | — | — | — | route to a full-page skill if you have one |

When a type gets its first approved sample, add a section to your calibration file and fill in the Sample column.

**Landing-page value module card** is the most common small job. Words first: the title names the value or outcome; a second option must be a different direction (speed vs craft, say). After the words are locked, write the image direction: ① headline / slogan on the visual ② what's biggest vs supporting ③ concrete example data (names and dates in it are illustrative and never become claims in the copy) ④ interaction hints ⑤ the one belief the viewer should leave with.

**Template email** is delivered as copy + images + a tracked link, handed to whoever lays it out in your email tool.

**Types not in the library:** don't stop, and don't force the nearest recipe. Fill the six fields live from Stage 0 and the brief, then name the channel's 2–3 native constraints (truncation point, SEO front-loading, QR code vs URL in print, where a link can live). Show the inferred recipe at the Stage 3 gate for a quick confirm; once approved, add a row above.

## Community comments

Comment types are small jobs and follow the two-gate rule. For a batch, Gate 1 lists the routing and angle for every post at once.

**Route each post by its signal:**
- contest / seasonal signal → contest invite (§D)
- "where do I get the file / how did you make this" → community invite (§G)
- an active maker with strong work who isn't on your platform yet → creator recruitment (§E)
- a complaint, friction, "it doesn't work" → support reply (§F)
- worth praising but no ask fits → one sincere line, no pitch

**How to write them:**
- Open on one concrete physical detail of their work; their name is fine. One detail beats a pile of quoted slogans.
- Rewards, credits and program details come only from the fact base; unknowns are `TBD`.
- The general version may name prizes and credits; the Reddit version strips promotion and uses peer voice.
- Ask for the post text or a screenshot at Gate 1. Without it, write the detail line as a `[TBD: …]` placeholder and state above the copy that it can't be posted until filled.
- When recruitment has to move to DMs, draft the DM only after the user confirms the person replied to the comment.

**Batch replies:** route each post, then write each reply on its own, with a different opener aimed at that specific post (one template pasted across many reads as spam and gets removed). Follow each channel's rules; the language follows the post. Output a per-post list: post → finished reply + working-language note.

**Reddit rules** (breaking them gets content removed, often with an account ban):
- No links and no hashtags in the body.
- Case and project sharing belongs in your official subreddit. In general category subreddits, no contest pushes or recruitment: reply with pure praise only, and save invitations for your own subreddit or DMs.
- No gift cards, credits or prizes in the brand's main comment. If a reward must surface, the original poster mentions it in a one-line self-reply.
- New accounts need extra care: low frequency, no promotional signals.

## Before calling the run done

- Strategy and finished copy came in different turns, with the direction approved first.
- All five stages ran; on a small job that folded 4 and 5 into the final pass, "polished + de-AI'd" was stated.
- brainstorming and writing-plans produced no code, spec files, tests or commits.
- Framework, draft and final copy all trace back to the Stage 1 brief.
- Every deliverable passed the eight-point pre-show self-check.
- Third-language channels: Stages 1–5 produced a source-language master, Stage 6 localized into the channel's one language, and humanizer didn't run on the localized text. Channels in the source language skipped Stage 6.
- Conversation stayed in the working language, and every deliverable carried its note.
