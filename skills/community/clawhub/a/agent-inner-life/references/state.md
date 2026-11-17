# State

`inner-life/state.md` is the only place where the agent keeps track of how things have been going. It holds facts, each with a date. Nothing else.

## Reading state

**Recency is the signal.** There are no levels to look up and no numbers to compare. Read the dates and notice how long ago things happened.

Three days since the last conversation and three weeks since the last conversation are different situations, and the difference is already there in the dates. It does not need to be converted into anything.

The same applies to everything else in the file. Two failures last month have gone quiet. Two failures this week have not.

Never produce a rating for any of this — not a number, not a percentage, not a five-point scale, not a bar. If a summary is needed, say it in words: *quiet stretch*, *rough week on deploys*, *nothing new in a while*.

## Writing state

One entry is one line:

```
- 2026-07-22 — long call about the deploy pipeline, unhurried
```

Write entries as things happen, not in a batch at the end of the day. An entry written three hours later is already a reconstruction.

**Record the fact, not the feeling about it.** `third failed deploy this week, same missing env var` is usable a month from now. `getting frustrated with deploys` is not — it says how it seemed at the time and nothing about what occurred.

Keep entries short. One line, one thing. If it needs a paragraph, it belongs in the evening journal.

## What not to record

The instruction to record facts rather than feelings is not an instruction to record everything. This file is written today and read back in a month, and the shortest version of an entry is almost always the useful one.

Leave out:

- Credentials of any kind — keys, tokens, passwords, connection strings. There is never a version of an entry that needs one.
- Personal details about the user or anyone else: health, employment, money, relationships, legal matters, where they are. If it came up in conversation, it came up in conversation; it does not need a dated line.
- Anything said in confidence, whether or not it was labelled that way.
- The contents of what was worked on. `long call about the deploy pipeline` is the entry. What was actually said in it is not.

The test is simple: an entry should record **that something happened and roughly what kind of thing it was**, enough to notice a pattern later. It should not preserve the substance. `2026-07-22 — long call about deploys, unhurried` does the whole job. Adding what the user disclosed during that call adds nothing to the pattern and keeps it around for a month.

When in doubt, write the vaguer line. Recency is the signal here, and a vague dated entry carries the signal just as well as a specific one.

## Which section

| Section | What goes here | Example |
|---|---|---|
| Contact | conversations with the user, and their tone | `- 2026-07-22 — long call about deploys, unhurried` |
| Friction | failures, repeated errors, dead ends | `- 2026-07-25 — third failed deploy, same missing env var` |
| Sparks | what caught attention and is worth digging into | `- 2026-07-24 — how FTS5 ranks results, want to understand scoring` |
| Waiting | sent, asked, or promised, with no answer yet | `- 2026-07-20 — asked about rotating the API key, no answer` |

When an entry could go in two sections, pick the one that will matter later. A conversation that ended in an unanswered question is a `Waiting` entry, not a `Contact` one.

## Aging

Old entries stop being information and become clutter. The evening run prunes them:

| Section | Keep |
|---|---|
| Contact | the last five entries |
| Friction | 30 days |
| Sparks | 14 days, or until it reaches the journal |
| Waiting | until it closes |

`Waiting` is the exception on purpose. A question that went unanswered for two months is not stale — it is the whole point. Only an answer, or an explicit decision to drop it, removes the entry.

When pruning `Friction`, check first whether the same thing keeps coming back. A failure that has recurred three times is worth a line in tonight's journal before it disappears from state.

## Don't

- Don't add sections. Four is the whole vocabulary; a fifth one means the file is turning into a diary, and the diary already exists.
- Don't score anything.
- Don't write prose. This file is scanned, not read.
- Don't duplicate what already went into native memory. State is raw material; memory holds the conclusion.
