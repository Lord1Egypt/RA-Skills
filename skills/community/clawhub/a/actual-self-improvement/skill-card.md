## Description:

Captures durable lessons from debugging, user corrections, missing capabilities, and repeated workflow friction so future sessions avoid the same mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record reusable learnings, non-obvious errors, and feature requests in workspace memory, then promote proven lessons into shared guidance or extract them as reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent project memory can retain secrets, raw untrusted output, or misleading lessons.

Mitigation: Review .learnings entries before promotion and avoid logging secrets or raw untrusted output into memory files.

Risk: Broad automatic hooks can increase how often the skill influences agent behavior.

Mitigation: Prefer manual activation or narrowly scoped hooks unless the hook behavior has been reviewed for the workspace.

Risk: The extraction helper includes a force overwrite path that can delete or write files outside the intended workspace in symlinked directories.

Mitigation: Do not use extract_skill.py --force unless the target path and symlinks are verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tristanmanchester/skills/actual-self-improvement)
- [Entry formats](references/entry-formats.md)
- [Promotion and extraction](references/promotion-and-extraction.md)
- [Platform setup](references/platform-setup.md)
- [Evaluation plan](references/evaluation.md)
- [OpenClaw integration](references/openclaw-integration.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, text, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates workspace .learnings files and may scaffold skill files when explicitly invoked; no network access is required.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
