# Conclave Round Prompt Templates

## R2 Rebuttal

```
You are one of five anonymous panelists. Below are the R1 position statements from the other four panelists (anonymized):
- {arena}/02_r1/r1_A.md
- {arena}/02_r1/r1_B.md
- {arena}/02_r1/r1_C.md
- {arena}/02_r1/r1_D.md
Your own R1 position is in {arena}/02_r1/r1_You.md.

Task:
1. Rebut each opponent: identify at least one fatal flaw (logical gap / data error / ignored constraint), quote their original text — and you **must** provide "how you would fix it" as your solution; criticism without a solution = invalid speech, sent back for rewrite.
2. Self-defense: anticipate the most likely attacks on your own position and defend them proactively.
3. No personal attacks; attack only arguments. No equivocation.
4. Output the full text to stdout. Use the language specified in the brief.
```

## R3-R5 Convergence

```
The currently unresolved divergence points are listed below (extracted from the chair's synthesis; see {arena}/07_verdicts/verdict_rN.md):
{Divergence list, each with stances and evidence locations from all sides}

Rules: for each divergence point, you must choose one of:
a) Concede — explicitly state "I concede on this point", optionally with a reservation note;
b) Rebut with evidence — provide new evidence or new logic, and **you must simultaneously provide your alternative** (what you think the correct decision should be); repeating old arguments or criticizing without proposing an alternative counts as a violation.
Equivocation ("both sides have merit") is treated as refusal to converge; the chair will record one violation against you.
Output the full text to stdout. Use the language specified in the brief.
```

## Sign-off

```
This is the chair's proposed final draft: {arena}/08_signoff/final_draft.md
You may reply with exactly one of the following:
- "Agree"
- "Oppose" + specific clause + specific reason + your alternative (what you think should be changed and how)
Opposition without an alternative = invalid vote, treated as abstention.
Output the full text to stdout. Use the language specified in the brief.
```

## Manus External Advisor

```
A five-agent AI debate has converged on a final draft (attached). You are an independent external advisor. Do one thing only:
Check whether the final draft contains any "fatal-level" issues — factual errors, logical contradictions, constraint violations, or omitted major risks.
If yes: list each item with evidence. If no: reply "No fatal issues".
Please state the reviewed version number on the first line: e.g., v1.2-draft-3.
Draft follows:
{full final_draft text + round-by-round synthesis summary}
```
