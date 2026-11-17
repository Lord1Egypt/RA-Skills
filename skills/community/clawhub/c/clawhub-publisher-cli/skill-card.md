## Description:

Use the bundled ClawHub Publisher CLI to validate, prepare, zip, and publish OpenClaw skills to ClawHub with clearer validation, cleaner packaging, and safer publish prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sam-k-migz](https://clawhub.ai/user/sam-k-migz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to validate local OpenClaw skill folders, prepare cleaner publish bundles, optionally create zip archives, and run guided ClawHub publish commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publishing workflow can unintentionally include local secrets, symlinks, or other unintended files in prepared packages.

Mitigation: Audit the prepared bundle before publishing, remove .env/.npmrc files and symlinks from skill folders, and prefer dry-run before executing a publish.

Risk: Running the CLI on untrusted skill folders can expose the user to unsafe local files or package contents.

Mitigation: Use it only on skill folders you trust and can inspect, and update vulnerable dependencies before production publishing workflows.

## Reference(s):

- [ClawHub Publisher release page](https://clawhub.ai/sam-k-migz/skills/clawhub-publisher-cli)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local file packaging and publish command execution through the bundled CLI.]

## Skill Version(s):

0.1.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
