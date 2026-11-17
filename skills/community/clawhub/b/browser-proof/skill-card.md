## Description:

Browser Proof is a public ClawHub browser-QA evidence skill for creating a machine-readable bundle with steps, artifacts, checks, and a shareable report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and release reviewers use this skill to capture browser QA or debugging runs as a portable evidence pack with a session manifest, ordered step log, structural bundle check, and Markdown handoff report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser QA evidence can include secrets, cookies, raw tokens, private paths, or untrusted browser-observed text.

Mitigation: Use trusted manifests and browser observations, avoid recording secrets or cookies, prefer relative artifact paths, and keep generated bundles inside a project workspace.

Risk: Validation and report-sanitization weaknesses can allow incomplete evidence or misleading report content to be shared.

Mitigation: Run the bundled bundle check, resolve missing evidence or absolute path findings, and review generated Markdown before publishing it to GitHub, Slack, Linear, or a release channel.

## Reference(s):

- [Browser Proof GitHub Repository](https://github.com/zack-dev-cm/browser-proof)
- [Browser Proof ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/skills/browser-proof)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON manifests, JSON bundle checks, Markdown reports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser QA evidence files that should be reviewed before sharing.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
