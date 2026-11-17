# Changelog

All notable changes to the **explainer** skill. Versioning follows SemVer.

## 2.0.0 — every real-run command carries `--approved`, and the core refuses without it

**Breaking, and the break is upstream.** `ofox-video-core` 2.0.0 makes its
four billable subcommands — `generate`, `create`, `batch`, `chain` — refuse to
run unless `--approved` is on the command line. This skill's one real-run
`generate` command now passes it. The `--dry-run` commands are untouched: a
quote is how the number being approved gets produced, so gating it would close
the only route through itself.

**What a caller has to do differently**

- **Install `ofox-video-core` 2.0.0 or newer.** This version of this skill
  needs it. On an older core the updated commands stop with `unknown option
  '--approved'` before any request — nothing is submitted and nothing is
  billed, so the failure is safe, but every real run fails.
- **A command copied from an older version of this file is now refused.**
  Anything pasted from an earlier revision, a transcript or a wrapper script
  hits the guard, prints the quote-first steps and exits non-zero. Nothing is
  submitted and nothing is billed. Re-run it with `--dry-run` to get the
  quote, or with `--approved` once the cost table has gone in front of the
  user.
- **The `batch` route needs it too.** This file shows only `batch --dry-run`;
  its real run takes `--approved` in the same place.

**What `--approved` is not.** It does not prove that an approval happened — an
agent can type it without showing anyone a price, exactly as it could
previously just run the command. What changed is that spending without quoting
is no longer the default: it now has to be written into the command, where a
transcript shows it and a reviewer can object. The gate in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md)
is still the rule, and this skill still states it in full.

**Documentation only otherwise. No price, default, prompt template, flag
meaning or generation behaviour changed.**

## 1.2.1 — the recovery command asked for the whole repo, and asked the agent to run it

**Documentation only. No flag, price, prompt template or generation behaviour
changed.**

"If the script isn't found" ended in a skills.sh command that installed *every*
skill in this repo, into *every* agent, user-level, with confirmation
suppressed — four widenings past the one skill that was actually missing.
ClawHub's scanner flags exactly that (rule T08, "unpinned and overbroad
third-party installation via npx"), and the flag is accurate rather than noise:
an agent that read the line and ran it would have rewritten the user's whole
skills setup to recover one relative path.

The line now asks for the missing skill and nothing else —
`npx skills add ofoxai/skills --skill ofox-video-core`, which asks for that one
skill and answers none of the agent, scope or confirmation questions on the
user's behalf. The repo's own `npx ofox-skills ofox-video-core` still answers
all three (every agent, user-level, no prompts), which is why the line handed
to the user is the skills.sh one.

**What a caller has to do**: nothing changes for any command this skill
already prints, and nothing changes while `ofox-video-core` is installed. What
changes is conduct on the one path where it genuinely is absent — **relay the
command and let the user run it**; do not run an installer yourself. An
install writes outside the working directory, and that is not a decision to
take silently for someone.

All three distribution routes are still named (this repo's own
`npx ofox-skills`, skills.sh, and LobeHub or ClawHub), because recovery advice
that names one installer is wrong advice on every other channel this skill
ships through.

## 1.2.0 — "about ninety words" is wrong; sentences cost seconds too

**Documentation only. No flag, command or safety behaviour changed** — but the
**word budget this skill is named for has changed**, so a script written
against the old number can overrun. Read the first bullet before writing
another one.

A 30-second run (`42d8b5c3-31f4-41d2-90eb-b07a3181b465`, 2026-09-17, seed
`1021654967`, 480p / 16:9, the **Voiceover** template, 80 words in 8
sentences, $3.30) closed this skill's two biggest gaps at once — the duration
it is named for, and the shape it had never generated.

**What a caller has to do differently:**

- 🚨 **Stop planning at "about ninety words in thirty seconds" or at a flat 3
  words a second.** Both were in the description, the headline section, the
  budget table, the defaults table and the recap. The new budget is a formula,
  because the measurement showed the missing term:

  ```
  speech span ≈ words / 3.56 + 0.7 x (sentences − 1)
  ```

  Measured: 22.49s of actual speaking plus 5.64s of internal silence in **7
  pauses — exactly the script's 7 sentence boundaries**, ~0.7s each. Speaking
  rate 3.56 w/s. The formula predicts 27.4s for that script; the delivered
  span was 28.13s, with 1.39s of tail and no truncation. **90 words in 8
  sentences needs 30.2s of span and does not fit a 30-second clip.**
- ⚠️ **Count sentences, not only words.** Two 80-word scripts can differ by
  several seconds, and short punchy sentences are the *slower* ones. When a
  script runs long, **joining sentences** buys back time that cutting words
  does not. This is the opposite of how the old guidance read.
- **The safe 30-second script is now ~80 words in ~8 sentences**, which is
  measured. The 10 / 15 / 20-second rows apply the same formula with the same
  headroom and have **not** been run at those lengths.

**Why the old number survived this long, and it is worth knowing:** it was
never measured. It was a 20-second clip's overall rate (3.05 w/s) multiplied
by 1.5. The two runs' overall rates (3.05 and 2.84) look like a contradiction
and are not — they are scripts with different sentence densities, and only the
second run separated speech from silence and could say so.

**What improved:**

- **The voiceover shape is no longer unrun.** It was "gallery practice only,
  never run here" — the last shape in this file with nothing behind it. The
  clip has no person in any frame, a slow continuous push with no cut, no
  invented lettering anywhere, and its ending holds on its final subject
  (frames at 22s and 29.5s are nearly identical). One run, English, 480p.
- Both shapes this skill offers now have a paid run at a duration the file
  leads with, so the risk in a first clip has moved from the **format** to the
  **script**.

**Still unmeasured, and the file says so:** the 0.7s boundary cost comes from
one script's 7 boundaries — the most load-bearing number here and the least
replicated. Non-English scripts, other resolutions and durations past 30
seconds remain untested, and the CJK character rates are still gallery-derived.

## 1.1.2 — the troubleshooting table still stated the old absolute

**Documentation only. No default, price, prompt template or behaviour
changed.**

1.1.1 corrected the defaults row and left the failure table saying "a
photoreal face cannot be carried by a frame". That was the general mechanism
claim the 2026-09-16 measurement narrowed — a frame can carry one, for a
likeness the caller is authorised to use — and it also disagreed with this
file's own continuity table, which already points at `talking-head` as the
route that re-attaches a portrait. The row now says what is actually true
here: nothing in **this skill's** route carries a face between jobs, because
the words route brings back staging and not a face. The advice in the fix
column is untouched.

## 1.1.1 — the defaults table called a measured flag untested

**Documentation only. No default, price, prompt template or behaviour
changed.**

The `--real-person` row said "untested on this model in this repo". It was
measured on 2026-09-16 lifting `bytedance/seedance-2.5`'s refusal of a
real-person reference image. The row now says so, names the flag for what it
is — Ofox's privacy-preserving preprocessing path for **authorised**
real-person references, an authorisation route rather than a way past a check
— and links `ofox-video-core`'s `references/api-params.md` for the evidence
and its limits.

The advice itself does not move: this skill's presenter is written in text, a
text-generated person was never what the refusal was about, and a skill whose
presenter comes from a photograph is `talking-head`. The continuity table's
"a portrait re-attached to each job is `talking-head`'s route, and its own
continuity is unmeasured" is a claim about a different thing — whether a face
holds across jobs — and nothing has measured that, so it stands as written.

## 1.1.0 — the number this skill is built on is no longer an extrapolation

**One paid run, and it was aimed at the one claim that mattered.** Job
`edef379e-9ac0-41c9-ab59-6378d030239e`, 2026-09-16,
`bytedance/seedance-2.5` on `byteplus`, 20 seconds at 480p, seed `623333235`,
text-to-video with nothing attached, 2 dollars 20. A 59-word
presenter-to-camera monologue written from this file's own template.

| Question | Measured |
|---|---|
| **Speech rate** | **3.05 words a second** — 59 words across a 19.33s speech span (`silencedetect` at -30dB: first word 0.399s, last 19.729s, 7 internal pauses) |
| **The thesis** | 3.05 x 30 = 91.5, so "a 30-second clip holds about ninety spoken words" holds |
| **Truncation** | none — `whisper tiny.en` returns all 59 words in order, nothing added or dropped |
| **The closing beat** | 0.335s of silence after the last word, at a script budgeted at almost exactly 3 words a second. The template asks for that beat and it fitted |

**What changed in the file is the kind of evidence, not the number.** The 3
words a second here was inherited from *two-person dialogue* measurements and
applied to a single continuous speaker — which is not a conservative estimate
but a category error, because the dialogue tier's low floor comes from clips
where most seconds have nobody speaking at all. `talking-head` shipped exactly
that mistake and had to correct it. The monologue tier now has its own
measurement on this skill's own default model.

**Two rates on two models, written as two observations.**
`talking-head` measured 3.16 w/s on `alibaba/wan-3.0-prime` the same day; this
skill measured 3.05 on `bytedance/seedance-2.5`. They agree, and they both sit
a little above the budget — but neither is repeated, they are different
scripts at different lengths, and the file says so rather than promoting the
pair into a rate the API is known to hold to.

**Bounds, written into the file rather than left implied:** one run, one
script, English, 480p, **20 seconds**. Thirty seconds was never run — the
ninety-word row is a linear extension of a twenty-second observation, and the
file now says that where the row is stated. The Chinese and Japanese
characters-per-second budgets are exactly as untested as they were.

**Also retired: "this skill has no paid run of its own"**, in all four places
it appeared — the measured table, the recap template, the pre-spend message
and the cost-anchor note. The anchor is now one point (20s / 480p / t2v,
2 dollars 20), stated as one point, with `--dry-run` still the only source of
a quote.

**And one methodology note kept rather than tidied away.** A first pass with
`silencedetect` at a 0.35s minimum found no trailing silence, and the reading
drawn from it — "a script at 3 words a second squeezes the closing beat out" —
was wrong. The beat is there in the frames; the pause is 0.335s, just under
the threshold looking for it. That is written into the file as a warning about
concluding from a tool's silence, because it is the kind of error that reads
like a finding.

## 1.0.0 — first release

A scenario skill for turning something written — an article, a README, a
release note, a paper — into a short clip of it being said out loud, either by
a presenter to camera or as a voiceover over footage. Execution is delegated
to `ofox-video-core`.

**The scenario was redefined before it was built, by a measurement.** The
original framing assumed a script could be supplied as audio. It cannot: the
API accepts an `audio_url` reference, validates it, fetches it and bills the
job, and the delivered audio is **not** the audio that was sent — measured
2026-09-15 on job `d8561509-dcc6-4f2c-8864-a193cd239b14`, 55 cents, envelope
correlation 0.41 between input and output. The user supplies text; the model
generates the speech.

**The skill's first section exists to correct the request it almost always
receives.** People ask for "a 30-second video of this article". A 30-second
clip holds about **ninety spoken words** — 7.5% of a 1,200-word post, under a
tenth of it — so it cannot summarise anything. The honest product is *one idea
from the source, said once*, and the skill says so in the first reply rather
than after the bill. It also refuses the tempting alternative explicitly: a
summary squeezed into ninety words becomes a string of abstractions that means
nothing to someone who has not read the source, which is worse than one
concrete idea fully said.

**Picking the idea is treated as the actual work**, and gets a procedure
rather than a suggestion: list the source's candidate claims, write each as
the sentence that would really be spoken, score all of them against four tests
(stands alone, concrete, fits the budget, worth someone's attention), then
offer the two or three survivors to the user as the actual sentences. `Idea`
is a must-ask row with no "Let the AI decide" — it is their article. A worked
selection over a fictional release post shows two candidates failing and two
passing, with the reason for each.

**The word capacity is linked, not restated, and budgeted against the right
tier.** The measured rates live in `ofox-video-core`'s `prompt-structure.md`;
this skill carries only the consequence — a clip-length-to-word-count table
with the share of a 1,200-word article each length represents. The tier that
applies to a single continuous speaker is monologue / talking head, 3.5 words
a second in English and 5 characters a second in Chinese; the dialogue-drama
band (0.4–1.7 words/s) measures two people with silence between their lines
and is a floor here rather than a budget. The skill plans a little under its
own tier — **3 words a second, 4 characters a second** — because the templates
spend clip time on an opening beat and a written silent ending while asking
for an unhurried delivery, and because the asymmetry is one-sided:
under-filling costs a pause, overrunning costs the whole clip.

**What is measured and what is not is a table, not a footnote.** The audio
finding, the five completed text-to-video jobs built around photoreal people,
the submission-time refusal of a photoreal person in an attached frame, the
music/moderation failure and the invented-text rule are marked measured; the
word rates and the voiceover-with-no-visible-speaker shape are marked gallery
practice. **This skill has no paid run of its own**, and the approval-gate
section requires that to be said in the same message as the cost table.

**Two limits users hit immediately are stated before they are hit:**

- **On-screen text is not available from a description.** Text rendered from
  prompt text comes back invented or garbled, repeatedly; a negative list
  alone does not hold on a lettered set. Captions and lower thirds go on in an
  editor, where they are free and correct. The one working route — a prepared
  title card attached as the first frame, which is preserved — is documented
  along with what it costs (the frame slot, and the clip's shape follows the
  image).
- **A photoreal presenter does not survive between jobs.** Each `generate` is
  stateless, and the usual fix of carrying the last frame forward is refused
  at submission when that frame holds a photoreal person. The skill gives four
  available series shapes instead of one impossible one, and points an
  illustrated recurring presenter at `seedance-anime-drama`, which works for
  exactly that reason.

Also in this release:

- **Two prompt templates** — presenter to camera (the shape this repo has run)
  and voiceover over footage (gallery practice only, priced as an experiment)
  — both single-shot with no manifest and no cut list, both quoting the chosen
  idea verbatim, both carrying `no music` in the sound block *and* the music
  words in `AVOID` after a scored cue failed output moderation on copyright in
  this repo, unbilled.
- **The spoken language follows the source's language**, never asked, with the
  warning that translating a line on the way into the prompt buys an
  English-dubbed clip the user discovers after paying.
- **A four-question brief** with skip rows that route "use my photo" to
  `talking-head`, "put the bullet points on screen" to the text section, and a
  six-feature doc back through idea selection rather than into one clip.
- **No hardcoded model, price, resolution, duration or aspect-ratio table.**
  Those are catalog facts and the skill points at `ofox-video.sh models` /
  `providers MODEL` / `generate --dry-run`. The default model is the script's
  own, because nothing here attaches a portrait and so nothing forces a
  different one.
- **No cost anchor, because there has never been a bill.** The dry-run figure
  at the parameters about to be sent is the only number to show, and the gate
  message also carries the chosen idea in full and one line saying what the
  clip is *not*.
- **An after-it-lands checklist** — were all the words said, is the idea still
  the idea, did any lettering get invented — because `STATUS completed`
  answers none of them.
- **It says when not to buy.** If the user wants the article summarised, that
  is a free writing task; if they want slides, diagrams or readable bullets, a
  narrated deck does it properly; past two or three parts, a screen recording
  with a voiceover is the better product.
- **The core-directory probe ships from day one**, so the skill works on
  LobeHub's `ofoxai-skills-<name>` layout as well as skills.sh / ClawHub /
  `npx ofox-skills`.

**What a caller has to do**: install `ofox-video-core` beside this skill.
`npx ofox-skills` installs every skill in this repo, which is what keeps the
sibling path resolvable.
