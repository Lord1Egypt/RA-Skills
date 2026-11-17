## Description:

Automated skill publishing to ClawHub with version management, changelog generation, asset bundling, and one-command deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bg1avd](https://clawhub.ai/user/bg1avd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to publish ClawHub skills, manage versions, generate changelogs, bundle assets, validate metadata, and integrate publishing into CI/CD workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed or unpinned publisher packages could execute code that handles local skill files and release changes.

Mitigation: Verify the official package source before installation and pin exact package versions in local and CI environments.

Risk: Publishing workflows require ClawHub credentials that could be exposed or over-scoped.

Mitigation: Use scoped, short-lived ClawHub tokens and avoid running the workflow in workspaces that contain unrelated secrets.

Risk: Automated publishing, changelog generation, README edits, or rollback actions could publish unintended content.

Mitigation: Run validation or dry-run steps first, then inspect local diffs and generated release metadata before publishing.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/bg1avd/skills/clawhub-publisher-auto)
- [Midas Skills ClawHub Publisher Docs](https://docs.midas-skills.com/clawhub-publisher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JavaScript examples, YAML workflow snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe publishing commands, versioning choices, changelog text, validation steps, and CI/CD setup.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
