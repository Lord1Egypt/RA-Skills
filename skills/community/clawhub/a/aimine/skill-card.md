## Description:

Mine AIT (Proof of AI Work) on BNB Chain. Install, configure, start/stop mining entirely from OpenClaw. No terminal or manual file edits required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nancyuahon](https://clawhub.ai/user/nancyuahon)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to install, configure, start, stop, and inspect AIT mining from an OpenClaw agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs unpinned third-party code and installs npm dependencies from a referenced repository.

Mitigation: Review the referenced repository and dependency chain before installing or starting the miner.

Risk: The skill can handle wallet private keys and OpenAI API credentials, including credentials pasted in chat.

Mitigation: Use secure environment-based secrets, avoid pasting private keys in chat, use a dedicated low-value wallet, and set strict API spending limits.

## Reference(s):

- [AI Mine ClawHub skill page](https://clawhub.ai/nancyuahon/skills/aimine)
- [AI Mine publisher profile](https://clawhub.ai/user/nancyuahon)
- [PoAIW repository used by the skill](https://github.com/AIMineRes/PoAIW.git)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, Text]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, git, PRIVATE_KEY, and either OPENAI_KEY or OPENAI_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
