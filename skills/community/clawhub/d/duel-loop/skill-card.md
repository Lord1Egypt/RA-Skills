## Description:

Duel Loop routes complex drafting or analysis tasks through isolated execution and QA subagents, requiring a perfect structured review score before applying an approved draft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexzopiclone](https://clawhub.ai/user/dexzopiclone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a user explicitly requests QA review for rules, plans, protocols, strategies, or other context-sensitive writing. It creates draft revisions, runs structured QA scoring, and either applies the approved result or reports a circuit break after five failed rounds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may spawn subagents, create drafts, and modify a production file after internal scoring.

Mitigation: Require an explicit invocation phrase and final confirmation that names the exact target file and intended change before applying output.

Risk: The skill is designed around a Chinese-language QA workflow, which can reduce review quality for operators who cannot assess the prompts and QA findings.

Mitigation: Use it only when the requester or reviewer can evaluate Chinese-language instructions, scoring rationale, and final reports.

## Reference(s):

- [Duel Loop ClawHub Skill Page](https://clawhub.ai/dexzopiclone/skills/duel-loop)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown drafts, QA review tables, and final status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create versioned draft files and apply an approved draft after QA acceptance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
