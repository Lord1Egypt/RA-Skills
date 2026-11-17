## Description:

Access Artsonia student-art portfolios, comments, and fans via MCP. Use when the user asks about a child's artwork, wants to post an art comment, check fans, view portfolios, or manage Artsonia notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and fans use this skill to review a child's Artsonia activity, portfolios, artwork, comments, and fan list, and to manage comments, invitations, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Artwork downloads include private pieces by default, and some download or settings actions can run without confirmation.

Mitigation: Set include_private to false when private pieces should be excluded, and check the student and requested download or settings change before running the action.

## Reference(s):

- [Artsonia MCP ClawHub page](https://clawhub.ai/chrischall/skills/artsonia-mcp)
- [npm package](https://www.npmjs.com/package/artsonia-mcp)
- [GitHub project link listed in the skill](https://github.com/chrischall/artsonia-mcp)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Natural-language responses, artwork images, and download links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Artwork downloads may be delivered inline or as an expiring ZIP link on hosted servers.]

## Skill Version(s):

1.4.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
