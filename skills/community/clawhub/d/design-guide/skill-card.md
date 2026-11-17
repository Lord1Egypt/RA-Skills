## Description:

Design Guide is a frontend design and production engineering skill that helps agents inventory projects, choose and present design directions, implement accessible responsive interfaces, and verify interaction, visual regression, accessibility, and performance quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grubbylee](https://clawhub.ai/user/grubbylee)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI coding-agent users use this skill to guide frontend design, redesign, review, and implementation work across web apps, dashboards, tools, landing pages, and responsive UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to run local development, preview, QA, and verification commands in a user's project.

Mitigation: Install and use it only when the agent is expected to work on frontend code, and review proposed commands before running them in sensitive repositories.

Risk: Preview commands in untrusted repositories may expose sensitive environment variables to local development tooling.

Mitigation: Run previews in trusted workspaces with minimal environment variables and no unnecessary secrets loaded.

Risk: The optional sync script is intended to overwrite managed design-guide skill directories across supported AIDE targets.

Mitigation: Review the target directories before syncing and keep private profiles outside the managed skill folder.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/grubbylee/skills/design-guide)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Design Process](references/design-process.md)
- [Artifact Presentation](references/artifact-presentation.md)
- [Executable Implementation Contract](references/implementation-contract.md)
- [Production Quality Gates](references/quality-gates.md)
- [Existing Product Design Review](references/product-design-review.md)
- [State and Data Coverage](references/state-and-data.md)
- [AIDE Integration](references/aide-integration.md)
- [Internationalization Contract](references/internationalization.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline code blocks, JSON contracts, generated or edited frontend files, shell commands, and QA reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May manage local preview servers, produce review artifacts, capture screenshots, and run frontend verification commands when the user task calls for them.]

## Skill Version(s):

0.1.2 (source: server release metadata, VERSION, design-guide.json, and changelog dated 2026-08-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
