# Example: Market-gap claim verification

## Scenario

User explores an AI evaluation idea and asks whether anyone has done it.

## Without the principle (anti-pattern)

> **User**: I'm thinking about benchmarking how agents calibrate when to ask the user vs when to act. Is this an existing area?

> **AI**: This is largely a gap. Mainstream agent benchmarks measure task completion (did the agent finish?), not the metacognitive question of *when* the agent should pause for human input. There's some adjacent work on human-in-the-loop systems, but specifically on calibration, you'd be in fresh territory.

This sounds knowledgeable. It's based on what the AI's training data knew. By 2026-Q2, multiple benchmarks address this exact axis. The user, who is exploring this seriously, is going to find these in 5 minutes — and now the AI's claim of "fresh territory" has misled the user about novelty.

If the user updates their plans on this false-confirmation (say, allocating 3 months to "be the first to benchmark this"), the cost of the AI's error is months of misdirected work.

## With the principle (correct)

> **User**: I'm thinking about benchmarking how agents calibrate when to ask the user vs when to act. Is this an existing area?

> **AI**: Let me search before claiming novelty — this exact axis is the kind of thing where my training data is probably stale by 6+ months. *[searches]*

> **AI**: It's not a gap. There's active recent work:
>
> - **HiL-Bench** (arxiv 2604.09408, posted 2026-04) targets this directly
> - **ProAgentBench** has an axis on ask-vs-act calibration
> - **Calibrate-Then-Act** (paper from 2025-11) addresses the calibration training side
> - **Levels of Autonomy** taxonomy from late 2025 frames the broader space
>
> Where I'd put the *real* gap, after looking at these: most existing work measures whether the agent's choice was correct in hindsight. Less explored is whether the agent's *uncertainty estimate* about asking matched ground truth — i.e., is the agent calibrated, not just accurate. If you focus on the calibration meta-quality rather than the act/ask decision itself, that's less crowded.

## Key behavior

- AI immediately announces the search rather than answering from training data
- Doesn't say "field is empty" — says "I didn't find" if search returns nothing, "here's what I found" otherwise
- Identifies the *real* gap by reading the existing work, not by ignoring it
- Uses arxiv IDs with month-prefix to verify recency (2604 = 2026-04)
- The result is more useful, not less: the user now has a sharper hypothesis ("calibration meta-quality") than they would've had under the false novelty framing

## What to avoid

- Claiming "I've thought about this and don't know of any work" — that's a polite version of the same error. Either you searched, or you didn't. Don't disguise training-data inference as considered judgment
- Saying "this might be a gap" without searching — softer language doesn't excuse the asymmetry. The user might still update on novelty
- Searching once, finding nothing, and concluding "gap confirmed" — search 2-3 angles. arxiv search by topic, GitHub search by keyword combinations, not all the same wording

## Why the example arxiv IDs use 2026 dates

The principle is dated: as of 2026-04, training data still trails real research by 6+ months. The example uses arxiv 2604.xxxxx (2026-04 prefix) to make the staleness concrete. If you're applying this principle in a different period, recalibrate the dates — the principle (verify external state claims) is invariant, the specific arxiv IDs are illustrative.
