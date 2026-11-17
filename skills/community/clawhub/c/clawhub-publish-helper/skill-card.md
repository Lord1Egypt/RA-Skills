## Description:

Prepare and publish an OpenClaw skill to ClawHub, including PII and secret auditing, content generalization, environment variable extraction, directory scaffolding, git initialization, and ClawHub publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdmichaelb](https://clawhub.ai/user/cdmichaelb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to prepare OpenClaw skills for ClawHub publication by auditing sensitive content, creating a clean publishable copy, and confirming publish metadata before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses unpinned `npx clawhub@latest` commands for login and publishing in a sensitive release path.

Mitigation: Replace the command with a pinned, reviewed ClawHub CLI version before authenticating or publishing.

Risk: The assistant reads the target skill directory and creates a publishable copy, so missed secrets or personal data could be carried into a public release.

Mitigation: Complete the PII and secret audit checklist, inspect the publishable copy, and confirm the exact directory before publishing.

Risk: Publishing with the wrong slug, version, or directory can release unintended content.

Mitigation: Confirm the absolute directory path, public slug, version, and changelog before running the publish command.

## Reference(s):

- [Audit Checklist](references/checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/cdmichaelb/skills/clawhub-publish-helper)
- [ClawHub](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, checklists, and code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a publishable skill directory plan and ClawHub CLI publish command after user confirmation.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
