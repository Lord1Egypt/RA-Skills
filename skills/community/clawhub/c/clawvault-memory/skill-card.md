## Description:

Provides an agent workflow for using the ClawVault plugin to search, save, verify, and consolidate local persistent memories across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidtkeane](https://clawhub.ai/user/davidtkeane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an OpenClaw agent disciplined, local, cross-session memory workflows for recalling prior work, saving verified facts, capturing corrections, and consolidating recurring lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables local memories that persist across sessions, including quiet saving after an initial disclosure.

Mitigation: Use it only when persistent memory is desired, disclose memory behavior to users, and avoid saving secrets, credentials, or personal data unless the user explicitly requests it.

Risk: The skill depends on an external ClawVault plugin that is not included in the artifact and is not pinned in the evidence.

Mitigation: Inspect or pin the required `clawhub:openclaw-plugin-clawvault` plugin before installation and gateway restart.

Risk: Installing the similarly named `clawhub:clawvault` package leaves the skill unable to call the expected `clawvault_*` tools.

Mitigation: Install the full package name `clawhub:openclaw-plugin-clawvault` and verify the expected ClawVault tools are available before relying on the skill.

## Reference(s):

- [ClawVault plugin repository](https://github.com/davidtkeane/openclaw-plugin-clawvault)
- [ClawHub skill page](https://clawhub.ai/davidtkeane/skills/clawvault-memory)
- [Publisher profile](https://clawhub.ai/user/davidtkeane)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown with inline tool-call examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for memory search, verified saving, consolidation, installation checks, and manual recovery from an incorrect plugin install.]

## Skill Version(s):

1.1.8 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
