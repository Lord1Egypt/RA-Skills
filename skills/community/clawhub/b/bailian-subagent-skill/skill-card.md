## Description:

Delegates token-intensive tasks to a Bailian (DashScope) subagent and provides MaxCompute agent_memory read/write patterns for long-term memory persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelhsin](https://clawhub.ai/user/samuelhsin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to offload large parsing, summarization, multimodal analysis, DataWorks/MaxCompute operations, and agent_memory CRUD tasks to Bailian while keeping the main session smaller.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad delegation to a Bailian subagent can expose task content outside the main agent session.

Mitigation: Review task content before delegation and do not send confidential, account, financial, or user data unless the deployment has explicit approval for that data flow.

Risk: Alibaba Cloud access keys are required for the documented MaxCompute and DataWorks examples.

Mitigation: Use least-privilege, preferably short-lived credentials supplied through environment variables, and never hardcode credentials in prompts or skill files.

Risk: The agent_memory table examples describe long-lived storage with a 3650-day lifecycle.

Mitigation: Define retention, deletion, and approval rules before writing sensitive or regulated information to agent_memory.

Risk: The MaxCompute examples use an HTTP endpoint.

Mitigation: Switch MaxCompute examples to HTTPS where supported before production or sensitive use.

Risk: The PyODPS installation example does not pin dependency versions.

Mitigation: Pin dependencies in a controlled environment before deploying the skill.

## Reference(s):

- [MaxCompute Patterns](references/maxcompute-patterns.md)
- [Bailian Subagent Skill on ClawHub](https://clawhub.ai/samuelhsin/skills/bailian-subagent-skill)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline YAML, Python, SQL, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes delegation settings, credential environment variables, dependency installation, and MaxCompute table/query examples.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
