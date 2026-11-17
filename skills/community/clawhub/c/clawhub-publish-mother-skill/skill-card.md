## Description:

Workflow for publishing and updating OpenClaw skills on ClawHub using verified token authentication and validation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers publishing or updating OpenClaw skills on ClawHub use this skill to prepare skill directories, authenticate with the ClawHub CLI, run dry-run publish checks, and troubleshoot common publishing failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authentication troubleshooting script can print a real CLAWHUB_TOKEN value in command output.

Mitigation: Mask or remove token echoing before running troubleshooting in environments where logs may be stored or shared.

Risk: The artifact promotes stealth browser and residential proxy login flows for authentication.

Mitigation: Prefer documented token authentication for headless publishing and review any browser automation approach against ClawHub and GitHub policies before use.

Risk: Publishing from an unreviewed working directory can upload unintended files.

Mitigation: Run validation and dry-run publishing from a clean directory after reviewing all files that will be included.

## Reference(s):

- [ClawHub Publish Mother Skill](https://clawhub.ai/stefanferreira/skills/clawhub-publish-mother-skill)
- [Camo Fox for ClawHub Publishing](references/camo-fox.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and shell helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes validation, dry-run publishing, and authentication troubleshooting workflows.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
