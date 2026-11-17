## Description:

Pulls startup project data and AI-generated build specifications from CoFounder.im so an agent can review and build validated project plans with user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexfilatov](https://clawhub.ai/user/alexfilatov)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to fetch CoFounder.im projects, inspect generated build specifications, and coordinate approved implementation phases. It is intended for CoFounder.im project builds rather than general coding tasks or scaffolding unrelated projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched CoFounder.im build phases can include dependency installs, network access, verification commands, or other project actions that should not be accepted blindly.

Mitigation: Review every fetched phase before approving sub-agents, dependency installs, network access, or verification commands, and run builds in a clean project directory or container.

Risk: Unpinned install commands can create supply-chain uncertainty.

Mitigation: Use a trusted or pinned installer version where possible before installation.

Risk: The skill uses COFOUNDER_API_TOKEN to access project data from CoFounder.im.

Mitigation: Keep the token scoped to CoFounder.im API access and avoid sharing it with sub-agents or commands unless required for the reviewed API call.

## Reference(s):

- [CoFounder.im OpenClaw homepage](https://cofounder.im/openclaw)
- [ClawHub skill page](https://clawhub.ai/alexfilatov/skills/cofounder-im)
- [CoFounder.im settings](https://cofounder.im/users/settings)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires COFOUNDER_API_TOKEN, curl, and jq; project-specific build dependencies vary by generated plan.]

## Skill Version(s):

1.2.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
