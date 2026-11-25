---
name: bias-lens
description: Use when the user asks to check a text, draft, article, message or conversation for cognitive biases, cognitive distortions or logical fallacies, or to scan, highlight or flag reasoning that looks biased. Matches each reasoning step against a regularly updated bias catalog, quotes the flagged passages and gives a concrete check for each. Not for stereotype or fairness audits of content about groups, AI model or dataset bias, political-bias ratings of news outlets, risk-of-bias ratings of research studies, or fact-checking claims against sources. Needs python3 and read-only access to a free public catalog API; the client never sends the text being checked.
metadata: {"openclaw": {"requires": {"bins": ["python3"]}}}
allowed-tools: Read Bash(python3:*)
---

# Bias lens

Read a text, map its reasoning, and match each reasoning step against the bias catalog. The output is a set of observations with checks, never a verdict about the author. Aim at the habit, let the reader say "this doesn't fit", and treat no findings as a good result. Knowing bias names grants no immunity. A reader may reject a finding, skip a passage or keep an example private; refusal is never further evidence of bias. The catalog's authored descriptions are aids to interpretation, not proof that a passage demonstrates a scientifically established effect.

## 1. Map the reasoning

Before you open the catalog, list the text's reasoning moves. Each move needs an exact quote (copied verbatim, so it can be highlighted), a one-line paraphrase of what it does, and its speaker when there is more than one. For long texts, read contiguous sections and keep a compact map with timestamps or line/paragraph references so coverage and later decisions can be checked. The moves to look for:

- **Claim:** something stated as true.
- **Inference:** "X, so Y". Write down the hidden step that links them.
- **Evidence:** what is offered as support, and what kind it is (anecdote, statistic, authority, popularity, feeling, memory).
- **Estimate or prediction:** a probability, size, duration or outcome.
- **Attribution:** why someone did something (character or situation, self or others).
- **Comparison or choice:** the options set side by side, and the options left out.
- **Hindsight or memory:** what "was obvious" or "always happened".

Skip moves that are plain facts, instructions or feelings with no inference attached. In video transcripts, skip sponsor reads, channel plugs and repeated teaser clips; these do not supply additional reasoning moves.

## 2. Check context and ownership

Before matching, review each move in its surrounding argument and mark it as current reasoning, past reasoning later corrected, someone else's reported reasoning, or a joke or rhetorical move. Count overlapping segments and repeated arguments once. A text that *explains* a bias is not committing it.

For conversations, review each speaker separately, including interviewers: their assertions, explanations and endorsed premises are eligible, while asking a question or testing another person's position does not establish endorsement. Track qualifications and corrections across that speaker's turns; another speaker's objection is context, not a retraction on their behalf. Do not assign a reported third party's reasoning to the person recounting it.

For each candidate argument, spell out the link from evidence to conclusion and a reasonable alternative reading before searching. An unsupported explanation, an artistic preference or a factual mistake does not by itself identify a shortcut. If a transcript or translation still leaves ownership, irony or meaning unclear, leave the move out rather than treating transcription noise as evidence.

Only current, endorsed reasoning becomes a main finding. Keep useful self-reported past reasoning that is explicitly corrected for **Self-corrections**, with both the earlier step and the correction; assess the earlier step using what was knowable then, and do not present it as the speaker's current belief. When someone voices a position to rebut it, assess the rebuttal, not the voiced position.

**Judge a dated text by its own date.** Note when it was written, and test each move against what was knowable then. If you know how the story ended, set that aside: a decision that turned out badly is not evidence that the reasoning was biased. If a pattern only becomes visible with later knowledge, it is not a finding. Mention it in the report as hindsight to resist, citing `hindsight-bias` or `outcome-bias`.

## 3. Smart search

Run `python3 <skill-dir>/scripts/bias_lens.py index` once, where `<skill-dir>` is this skill's folder. It fetches a public catalog snapshot and prints one line per entry: ID, plain definition, related IDs. Record the catalog version printed to stderr in the report. Subsequent `detail` calls use that cached snapshot without network access; do not refresh it during the reading. Avoid concurrent readings sharing one cache, or set a different `XDG_CACHE_HOME` for each. If the network is unavailable, `index --offline` explicitly reuses the cache; disclose that choice. If no usable snapshot exists, stop catalog matching and report the failure rather than inventing entries.

The catalog holds cognitive biases and, tagged `[distortion]` in the index, CBT cognitive distortions such as `emotional-reasoning` and `catastrophizing`. Distortions match personal reasoning about yourself, other people and the future, so expect them most in messages, diaries and memoirs; they also cover a feeling offered as proof of a public claim ("my horror shows how big the disaster was"). Never present a distortion finding as a symptom.

Entries tagged `[fallacy]` are flaws in an argument's structure, not thinking habits. Match them only when the text itself shows the move: the word whose meaning shifts, the actual claim beside the reply, the workable option left out. A fallacy finding says the reason given does not support the conclusion; it never says the conclusion is false or the author dishonest. Use the live index for available entries and their families rather than assuming a fixed list.

For each inference, estimate, attribution or comparison, find candidates by **mechanism, not topic**. A text about money is not automatically mental accounting. Ask what shortcut would produce this exact step. Shortlist two or three candidates per move at most.

Then run `python3 <skill-dir>/scripts/bias_lens.py detail <id> [<id> ...]` for the shortlist. Each description contains a qualification sentence saying what the bias is *not*. If the qualification fits the passage, drop the candidate. Use the `related` links to choose between neighbours, and name the runner-up when the call is close.

If a move looks flawed but no entry in the live index fits, say so in one line instead of forcing a match. Do not replace mechanism matching with substring search, which finds topics rather than reasoning steps.

## 4. Report

Start with the text, marking findings inline as `==quoted passage==[1]`. Keep the rest of the text unchanged; for long texts, show only the paragraphs that contain findings. If the text is not in the user's language, quote it in the original and add a short gloss in the user's language after each quote. For long inputs, add a brief coverage note and save the reasoning map with each move's disposition, including exclusions and findings omitted by the cap.

Then one block per finding:

```
[1] Escalation of commitment (close alternative: plan continuation bias)
https://tarot.catarchy.space/biases/escalation-of-commitment/
Step: "we've spent two years on it" is offered as the reason to keep going.
Check: If you were starting today with no history, would you choose this?
Strength: clear / possible
```

- **Step** names the inference in the text, not a trait of the writer. When the text's main conclusion rests on this step, say so; a slip in a side remark matters less than one the argument depends on.
- **Check** is a concrete test the reader can run, in the spirit of the catalog examples. Not a confession, not "be aware of your biases".
- **Strength:** `clear` when the passage only makes sense with this shortcut, `possible` when a reasonable reading avoids it. With `possible`, add the reasonable reading in a few words (for example "every essay chooses its words; this frame is the genre").
- When a qualification sentence nearly applies, write the Check so it uses that sentence: name the case where the bias would not apply, then ask whether this passage is that case.
- At most five main findings per speaker, with no quota to fill. Put `clear` findings before `possible` ones, and steps the main conclusion rests on before side remarks. For conversations, group findings by speaker with unique reference numbers across the report; briefly account for a speaker with no findings so silence does not look like skipped coverage.

After the findings, add these short sections. Skip any that would be empty:

- **Self-corrections:** the strongest corrected past examples, attributed to their speaker, with exact quotes for the earlier reasoning and the correction. If a catalog mechanism fits, link it and explain the earlier step; keep these separate from current findings and their cap.
- **Left out:** moves that looked like a bias and were rejected, one line each with the reason (a qualification fits, the move is narration rather than argument, or it is a plain unsupported claim and not a bias). Also give the number of findings cut by the limit of five per speaker.
- **Outside the catalog:** flaws for which no entry in the live index fits, one line each with the speaker when relevant.
- **Not marked on purpose:** say so whenever the text has religious, political-identity or emotional content you chose not to mark, so the reader knows it was a choice and not a miss.
- **What it reasons well:** one line, when there is something real to say. Look for places where the author checks their own perception or includes facts that cut against their thesis.
- **Catalog gap:** if a strong move had no good entry after checking the live index, name the missing habit or argument flaw by its common name as a suggestion for the catalog. Do not create the entry.

No findings is a valid answer. Say which reasoning moves you checked and why none matched.

Before handing over the report, check it:

- [ ] Every finding quotes the text verbatim and has a catalog link, a Step, a Check and a Strength.
- [ ] Every `possible` finding names its reasonable reading.
- [ ] No speaker has more than five main findings, and cut findings are counted under **Left out**.
- [ ] Corrected past reasoning sits under **Self-corrections**, not among the findings.
- [ ] The catalog version is recorded, and `--offline` use is disclosed.
- [ ] Every speaker and side was held to the same standard, including the one whose conclusion you agree with. If the findings land on one side only, the text should explain why, not your own view.
- [ ] Nothing in the report describes the author's character or mental health.

## The script

`scripts/bias_lens.py` uses Python 3.9+ and its standard library to GET `https://tarot.catarchy.space/api/public/v1/catalog/`. No account, token, Tarot repo checkout or Python package installation is required. Only catalog requests reach the service; never send the input text. It stores public catalog JSON under `$XDG_CACHE_HOME/bias-lens`, defaulting to `~/.cache/bias-lens`, and revalidates it with ETags at the start of a reading. `BIAS_LENS_CATALOG_URL` can select another server implementing schema version 1; it only changes where the catalog is read from, and the client still sends nothing but catalog GET requests. Connection and schema failures exit with a clear error; stale content is used only when explicitly requested with `index --offline`.

## Limits

- The catalog describes thinking habits. A text shows only what someone wrote, so findings are possible patterns, not diagnoses.
- Never treat religious identity, distress, disagreement or a mistaken fact as evidence of a bias.
- If the user shares their own painful thoughts while upset, respond to them first. Offer the reading only when they ask for it or agree to it, and never as treatment.
- The catalog is read-only here. Do not edit bias entries while running this skill; suggest catalog changes separately if a gap shows up.

## Improving the skill

When a run surfaces a repeated mistake, a missing check or a better report format, suggest a focused improvement. Edit the installed skill only when the user asks. Put a new check next to the step it changes and prefer sharpening an existing rule to adding another.
