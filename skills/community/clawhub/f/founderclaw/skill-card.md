## Description:

FounderClaw is a multi-agent engineering team for OpenClaw with 29 skills, 6 agents, a structured workspace, auto mode, and vision sub-agent routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashish797](https://clawhub.ai/user/ashish797)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use FounderClaw to add an OpenClaw-based agent organization for product planning, design review, code review, QA, browser testing, security checks, deployment, and retrospectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can modify OpenClaw configuration and create a broad local agent workspace.

Mitigation: Review the release before installation and prefer a cloned, pinned source version over pipe-to-shell installation.

Risk: The browser automation service can operate with authenticated browser sessions.

Mitigation: Avoid using authenticated sessions on shared or untrusted machines and stop the browser daemon before handling sensitive web accounts.

Risk: Cookie import and browser session handling can expose sensitive account state if used carelessly.

Mitigation: Import only the cookies needed for testing and do not import cookies on machines or workspaces you do not fully trust.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ashish797/skills/founderclaw)
- [FounderClaw README](README.md)
- [Architecture](ARCHITECTURE.md)
- [FounderClaw Workspace Structure](docs/founderclaw-design.md)
- [QA Issue Taxonomy](qa/references/issue-taxonomy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration changes, and generated project artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local OpenClaw configuration, workspace files, browser automation state, review reports, QA reports, release notes, and deployment logs when the agent follows the skill workflows.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
