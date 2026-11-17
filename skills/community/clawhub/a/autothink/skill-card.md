## Description:

Automatically adjust OpenClaw's thinking level based on message complexity and switch between low, medium, and high modes with session persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zpy0726](https://clawhub.ai/user/zpy0726)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to select and persist an agent thinking mode for a conversation, either with low, medium, or high prefixes or with the skill's optional complexity analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages passed through the CLI may be interpreted by a shell during local OpenClaw execution.

Mitigation: Remove shell-based invocation, validate and quote user-controlled arguments, and review local execution behavior before installation.

Risk: Artifact documentation and release metadata describe conflicting v1 and v2 behavior for automatic analysis and persistent mode switching.

Mitigation: Align README, skill metadata, and CLI behavior with the released v2 semantics before relying on the skill in a shared or production workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zpy0726/skills/autothink)
- [Project Homepage](https://github.com/openclaw/openclaw-autothink)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [CLI text output and JavaScript object results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects a low, medium, or high thinking mode, strips mode prefixes, and can forward the cleaned message to OpenClaw.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json; package.json and skill.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
