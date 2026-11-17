## Description:

Anti-Slop helps agents edit substantial prose and non-trivial code to reduce formulaic AI-style vocabulary, over-formatting, sycophantic framing, and common AI-generated code anti-patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjasta-tarigan](https://clawhub.ai/user/anjasta-tarigan)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and engineers use this skill as a second-pass editor for drafts, documentation, reports, creative writing, and code. It helps identify clustered AI-style prose patterns and common AI-generated code issues before final delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may proactively change tone, formatting, wording, or code structure when exact voice or implementation style matters.

Mitigation: Review final outputs when preserving exact wording, authorial voice, formatting, or code structure is important.

Risk: A diagnostic slop scan can over-weight isolated words or formatting choices that are appropriate in context.

Mitigation: Treat scanner findings as editing prompts and use the skill's density-based guidance rather than deleting terms mechanically.

## Reference(s):

- [Prose Tells: The Full Reference](references/prose-tells.md)
- [Code Slop: The Full Reference](references/code-slop.md)
- [Self-Edit Checklist](references/self-edit-checklist.md)
- [Research Notes](references/research-notes.md)
- [Anti-Slop ClawHub Skill Page](https://clawhub.ai/anjasta-tarigan/skills/anti-slop)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional code, shell command, or JSON diagnostic output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use the bundled standard-library scanner for longer prose; scanner output is diagnostic rather than a pass/fail gate.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
