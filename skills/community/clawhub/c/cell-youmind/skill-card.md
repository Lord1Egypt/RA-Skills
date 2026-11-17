## Description:

Use this skill when working with YouMind through the official YouMind CLI and API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover YouMind APIs, inspect request schemas, and operate YouMind boards, notes, materials, chats, documents, slides, skills, and scheduled tasks through the official CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform remote account actions such as write, publish, trash, install-skill, and scheduled-task operations.

Mitigation: Review account-changing requests carefully, inspect API schemas before non-trivial writes, and confirm destructive actions before execution.

Risk: Content sent through the YouMind CLI or API may be received by YouMind.

Mitigation: Avoid sending sensitive content unless the user is comfortable with YouMind receiving it, and keep API keys in environment variables or explicit CLI options only when needed.

Risk: An unpinned global CLI installation can change behavior as the official CLI evolves.

Mitigation: Prefer a pinned or otherwise verified CLI version when installing or updating the YouMind CLI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cellinlab/skills/cell-youmind)
- [OpenClaw homepage metadata](https://github.com/cellinlab/cell-skills/tree/main/skills/youmind)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the official YouMind CLI and authentication through YOUMIND_API_KEY or --api-key; recommends schema inspection before non-trivial writes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
