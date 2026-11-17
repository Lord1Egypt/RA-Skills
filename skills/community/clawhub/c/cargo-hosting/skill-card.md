## Description:

Guides agents through deploying and managing Cargo hosted apps and serverless workers, including deployments, environment variables, and custom domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scaffold and deploy static web apps or HTTP workers to Cargo, manage releases, environment variables and secrets, and troubleshoot common hosting problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external CLI, generated templates, and related prerequisite documents were not available for review, so their behavior may differ from this guidance.

Mitigation: Choose a reviewed CLI version and confirm the active workspace; inspect the selected source directory and upload exclusions before deploying.

Risk: Credentials placed in public app variables can be exposed in a downloadable app bundle, and broadly shared worker tokens can grant excess access.

Mitigation: Keep credentials out of public app variables and use worker-specific secrets with limited permissions.

Risk: Uploading local files can expose unintended content, while replacing an existing .env.local can lose local configuration.

Mitigation: Inspect the source directory and exclusions before upload; back up or merge existing .env.local files.

Risk: A signed file link grants access to anyone who holds it, and removing a resource also deletes its deployment history.

Mitigation: Share signed links only with intended recipients and preserve anything needed before removing a resource.

## Reference(s):

- [Cargo Skills project homepage](https://github.com/getcargohq/cargo-skills)
- [Cargo Hosting on ClawHub](https://clawhub.ai/cargo-ai/skills/cargo-hosting)
- [App examples](artifact/references/examples/apps.md)
- [Deployment examples](artifact/references/examples/deployments.md)
- [Worker examples](artifact/references/examples/workers.md)
- [Hosting response shapes](artifact/references/response-shapes.md)
- [Hosting troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow examples and troubleshooting guidance for the active Cargo workspace.]

## Skill Version(s):

1.4.1 (source: SKILL.md frontmatter, artifact/skill-metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
