## Description:

Orchestrates multiple AI CLI tools by detecting available CLIs, prioritizing them, and switching between them for fallback-enabled coding workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnatom](https://clawhub.ai/user/cnatom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to coordinate installed AI command-line tools, choose a preferred tool for a task, and fall back to another tool when rate limits, authentication failures, or execution errors occur.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read shell and project configuration, including files that can expose credentials or sensitive environment details.

Mitigation: Use a dedicated AI CLI configuration file, avoid broad access to generic .env files, and review which configuration files are readable before running the skill.

Risk: The scan script sources shell startup files before detecting installed tools, which can execute local shell customization code.

Mitigation: Source only trusted shell startup files, or remove automatic shell startup sourcing when the environment does not require it.

Risk: The scan script runs installed AI CLI commands and writes a persistent configuration file under the user's home directory.

Mitigation: Review detected commands before execution and inspect or remove the generated AI CLI configuration after use.

Risk: Task context, summaries, or code diffs may be passed to external AI CLI providers during orchestration.

Mitigation: Check provider policies and exclude secrets, private code, and regulated data from prompts before handing context to external CLIs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cnatom/skills/agent-cli-orchestrator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and YAML or JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local AI CLI tools and persist an AI CLI configuration file when its scan script is used.]

## Skill Version(s):

2.0.1 (source: server release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
