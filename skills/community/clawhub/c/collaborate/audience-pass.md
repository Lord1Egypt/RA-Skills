# Audience Pass — Testing Reception Before Shipping

For artifacts that are technically correct but face an audience: docs, READMEs, APIs, UIs, emails, talks, PRs, error messages. Correctness is checkable by the author; reception is not — the author cannot unknow their own context. The pass simulates consumption, not review.

## Consume, Do Not Review

The counterpart performs the audience's actual task using only the artifact:

- README/setup doc → follow the steps literally on a clean environment; stop at the first step that requires knowledge the doc did not provide.
- API → write the first call using only the reference; no peeking at source.
- UI flow → attempt the primary task; narrate what each element appears to do before clicking.
- Email/proposal → read once at natural speed, then answer: "what are they asking me to do?"

A counterpart who reads the artifact and comments on it is reviewing, not consuming — restart the pass.

## The Persona Ladder

Run the persona that matches the stakes; the least patient consumer (SKILL.md Quick Reference) is the default first rung.

| Persona | Simulation rule | Catches |
|---|---|---|
| Least patient consumer | First 10 seconds decide continue/bail; nothing below the fold exists | Buried leads, slow openings, unclear value |
| Newcomer with zero context | Every unexplained term is a full stop | Curse of knowledge, missing prerequisites |
| Expert skimmer | Searches and jumps; never reads linearly | Unfindable structure, headings that lie about content |
| Hostile reader | Actively looking for a reason to reject | Overclaims, unsupported numbers, tone that grates |
| 3am on-call reader | Degraded attention, needs the action NOW | Runbooks that explain before they instruct |

## What to Log

Three timestamps, in order of value:

1. **First confusion** — the first sentence/element where the consumer's model diverged from the author's intent.
2. **First unanswered question** — the question the audience asks that the artifact never addresses.
3. **First trust drop** — the first overclaim, broken step, or stale detail; trust does not recover within one artifact.

Fix in document order: everything after the first confusion was consumed by a reader the author lost already.

## Comprehension Check

End every pass with the counterpart restating the artifact's point in one sentence, unaided. A mismatch is a verdict on the artifact, not the reader — the artifact says it wrong. This is the cheapest test in the whole pass; never skip it.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Author runs their own audience pass | You cannot simulate not-knowing what you know | Recruit or simulate with a hard persona rule held all round |
| Polishing past the bail point | Effort lands where the audience never reaches | Fix the first 10 seconds first |
| Treating persona feedback as edits | The consumer reports symptoms; the author owns the cure | Log confusion points; do not accept rewrites mid-pass |
| One persona for all artifacts | A runbook and a landing page fail differently | Pick the persona by stakes; run a second rung only if the first passes clean |
