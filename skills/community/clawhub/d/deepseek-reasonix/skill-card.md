## Description:

Deepseek Reasonix helps agents provide DeepSeek terminal programming guidance, setup references, troubleshooting notes, and code-context suggestions for long-session coding workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get DeepSeek-oriented terminal coding-agent guidance, setup and troubleshooting references, and simple code-context suggestions during coding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags a vague claimed purpose, so users may expect a complete DeepSeek coding agent when the artifact mainly provides tutorial-style guidance and a helper script.

Mitigation: Review the skill behavior before installation and treat it as a guidance/helper artifact unless additional maintained agent capabilities are verified.

Risk: The helper script uses a shared temporary cache that could corrupt user-writable files in a local attack scenario on shared or privileged systems.

Mitigation: Use a private per-user cache directory with safe file creation before running the script on shared machines or privileged accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/deepseek-reasonix)
- [Programmer Xiao Liu DeepSeek-Reasonix tutorial](https://www.bilibili.com/video/BV1RtGU6hEDd)
- [Kunpeng Talk DeepSeek-Reasonix experience](https://www.bilibili.com/video/BV1sCVN6xEan)
- [AI Sui Feng DeepSeek and Reasonix overview](https://www.bilibili.com/video/BV1QbGy65E53)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with optional code or command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return code-context suggestions based on provided snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
