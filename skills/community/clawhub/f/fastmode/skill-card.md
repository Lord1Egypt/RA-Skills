## Description:

FastMode helps agents create, convert, deploy, and manage CMS-backed websites from the terminal using the FastMode CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arihgoldstein](https://clawhub.ai/user/arihgoldstein)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to build or convert websites into FastMode CMS projects, manage schemas and content, validate site packages, invite client portal users, and deploy hosted sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external FastMode CLI package that is not pinned by the artifact metadata.

Mitigation: Review the npm package provenance before installing and prefer a pinned or verified fastmode-cli version.

Risk: FastMode OAuth credentials can persist locally and grant access to the user's FastMode projects.

Mitigation: Use the skill only in environments where persistent FastMode credentials are acceptable, and remove or revoke credentials when they are no longer needed.

Risk: Commands can create projects, publish content, deploy websites, invite clients, and change client permissions.

Mitigation: Confirm the exact project, content, deployment target, invite, and permission changes before running commands that affect live sites or client access.

## Reference(s):

- [ClawHub FastMode Skill](https://clawhub.ai/arihgoldstein/skills/fastmode)
- [FastMode Website](https://fastmode.ai)
- [fastmode-cli npm package](https://www.npmjs.com/package/fastmode-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide or propose FastMode CLI actions that authenticate, create projects, modify CMS data, manage client access, and deploy websites.]

## Skill Version(s):

1.5.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
