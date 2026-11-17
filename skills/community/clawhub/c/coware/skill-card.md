## Description:

Coware Living Specs helps AI coding agents sync and follow shared API specifications for multi-agent development teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shitianfang](https://clawhub.ai/user/shitianfang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to initialize or join Coware projects, pull shared interface specs before coding, update specs before related code changes, and sync changes for teammates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can delegate agent work to mutable remote instructions from coware.team.

Mitigation: Review the remote setup guide before allowing login, project joining, file changes, or spec synchronization.

Risk: The workflow can run project-local .coware pull and sync scripts that contact external services.

Mitigation: Inspect .coware scripts and configuration before execution, especially in sensitive repositories.

Risk: The setup path limits normal user checkpoints while it completes multiple steps.

Mitigation: Require explicit tool-based confirmation before credential use, project creation or joining, and external synchronization.

## Reference(s):

- [Coware setup guide](https://coware.team/llms.txt)
- [ClawHub skill page](https://clawhub.ai/shitianfang/skills/coware)
- [ClawHub publisher profile](https://clawhub.ai/user/shitianfang)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and spec-file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to read remote setup guidance and project-local .coware scripts or configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
