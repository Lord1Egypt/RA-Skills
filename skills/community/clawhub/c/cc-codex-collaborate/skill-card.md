## Description:

Coordinate Claude Code and Codex in a milestone-based collaboration loop. Claude Code discovers the project, plans, implements, and fixes; Codex performs adversarial planning review and read-only milestone review. Working documents are stored under docs/cccc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayl1n](https://clawhub.ai/user/jayl1n)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate Claude Code and Codex on coding tasks through project discovery, milestone planning, adversarial plan review, read-only milestone review, and iterative fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loop automation can install persistent Claude hooks.

Mitigation: Review the exact .claude/settings.json hook changes before enabling automation and use loop-stop to disable hooks when the workflow is no longer needed.

Risk: Repository diffs may be sent to a configurable Codex executable during review.

Mitigation: Keep codex.cli_command set to a trusted Codex executable and avoid running reviews while tracked diffs contain credentials, private keys, customer data, or production configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayl1n/skills/cc-codex-collaborate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, generated project documents, JSON configuration, hook scripts, and command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a milestone collaboration workflow and local project files under docs/cccc after setup.]

## Skill Version(s):

0.1.13 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
