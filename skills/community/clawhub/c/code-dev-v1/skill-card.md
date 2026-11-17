## Description: <br>
Code Dev V1 helps engineering teams coordinate versioned development work, release management, team coding standards, delivery audits, and multi-environment release pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan multi-task versioned development, manage releases and changelogs, define team quality standards, and generate audit-oriented delivery records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated shell or Git release commands can modify working trees, tags, branches, or deployment state. <br>
Mitigation: Review commands before execution and require explicit approval for staging, production, rollback, or release-tag actions. <br>
Risk: Release integrations may require CI/CD tokens or webhook URLs. <br>
Mitigation: Keep credentials in protected environment variables or a secret manager, and avoid committing secrets or live webhook URLs. <br>
Risk: Local .code-toolkit audit and configuration files may contain project or delivery metadata. <br>
Mitigation: Review generated audit and configuration files before sharing them outside the project or publishing release artifacts. <br>


## Reference(s): <br>
- [Code Dev V1 on ClawHub](https://clawhub.ai/thcjp/skills/code-dev-v1) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce release plans, quality-gate summaries, changelog guidance, audit traces, and local .code-toolkit configuration examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
