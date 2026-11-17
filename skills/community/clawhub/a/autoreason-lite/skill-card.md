## Description:

Apply a bounded multi-candidate self-refinement loop (A/B/AB + judges + do-nothing option) to improve drafts, plans, and analyses while preventing scope creep.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cwheeler67](https://clawhub.ai/user/cwheeler67)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to improve drafts, strategy memos, explanations, product copy, and decision frameworks through a bounded A/B/AB refinement and judging loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad refinement requests may activate a deeper review loop when a small edit would be enough.

Mitigation: Use the skill's avoid cases, maximum three-round cap, and convergence rule to stop when no meaningful gain is found.

Risk: Revision pressure can introduce unsupported claims or drift from the user's intent.

Mitigation: Judge candidates against faithfulness, preserve critical facts, prefer no-change over noisy edits, and surface uncertainty when confidence drops.

## Reference(s):

- [Judge Rubric](references/judge-rubric.md)
- [Autoreason Lite ClawHub Listing](https://clawhub.ai/cwheeler67/skills/autoreason-lite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with final refined text and concise improvement bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounded to at most three refinement rounds with a +/-15% length guardrail unless the user asks otherwise.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
