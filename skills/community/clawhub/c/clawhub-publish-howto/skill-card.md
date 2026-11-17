## Description:

Guides developers through publishing, updating, and troubleshooting OpenClaw skills on ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbj375767338-arch](https://clawhub.ai/user/bbj375767338-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill as a practical guide for publishing skills to ClawHub, configuring authentication, avoiding GitHub rate limits, and diagnosing common release errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide recommends storing a GitHub access token in persistent shell configuration, which can expose long-lived credentials.

Mitigation: Use a credential manager, GitHub CLI/keychain flow, or a short-lived fine-grained token for a single command, then revoke it afterward.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bbj375767338-arch/skills/clawhub-publish-howto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes publishing checklists, authentication notes, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
