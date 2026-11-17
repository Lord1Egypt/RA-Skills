## Description:

Helps build, update, and troubleshoot SaaS websites, including pages, site data, and forms, through a user-provided site connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsqduron](https://clawhub.ai/user/hsqduron)

### License/Terms of Use:

MIT-0

## Use Case:

Website owners and developers use this skill to plan, build, migrate, and maintain SaaS websites, including pages, product and article data, and customer-facing forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Site credentials could grant access to the wrong website or expose sensitive content.

Mitigation: Provide connection addresses and Bearer tokens only for sites you control; verify the target site before use.

Risk: Writes, deletes, and batch imports can change published content, and a failed batch may leave partial changes.

Mitigation: Review the target and impact of each proposed change before approval, especially deletes and batch imports.

Risk: Customer-facing forms may collect phone numbers, email addresses, verification codes, or uploaded files.

Mitigation: Add appropriate privacy notices and review collection and handling before publishing forms.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hsqduron/skills/ai-website-builder)
- [Website pages guide](references/website-common-pages.md)
- [Site connection and tools reference](references/mcp-tools.md)
- [Forms and data interface reference](references/advanced-data-interface.md)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with HTML, CSS, JavaScript, and template code as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can propose site content and changes through a user-authorized site connection.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
