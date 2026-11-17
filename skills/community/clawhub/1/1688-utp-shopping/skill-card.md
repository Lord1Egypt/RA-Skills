## Description:

1688-utp-shopping helps agents support 1688 procurement workflows, including product search, comparison, cart management, checkout, and payment through UTP MCP or CLI flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users, procurement teams, and agent operators use this skill to turn natural-language shopping requests into 1688 product search, supplier comparison, cart, checkout, and order-status workflows. It is also useful for environments that need installation and operating guidance for UTP over MCP or CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may install unpinned global npm software and make persistent MCP configuration or PATH changes.

Mitigation: Review the installer first, verify the npm package source and version, and back up agent MCP configuration and PATH settings before installation.

Risk: The skill can guide real shopping, checkout, and payment workflows.

Mitigation: Keep checkout and payment behind the documented human confirmation flow and require the user to review order details before submission.

Risk: UTP state under the user's home directory can include local configuration, device tokens, and shopping preferences.

Mitigation: Protect local UTP files with normal account permissions, avoid exposing encrypted address fields in chat, and remove local state when decommissioning the skill.

## Reference(s):

- [README](README.md)
- [Checkout and order guide](references/checkout-guide.md)
- [Linux cloud mode guide](references/cloud-mode.md)
- [Error handling guide](references/error-guide.md)
- [UTP website and feedback guide](references/feedback-guide.md)
- [Install guide](references/install-guide.md)
- [Preferences guide](references/preferences-guide.md)
- [Commerce host registry](references/registry.md)
- [Update guide](references/update-guide.md)
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-utp-shopping)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON tool arguments and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce shopping UI cards through MCP hosts or text results through CLI mode; checkout and payment flows use human confirmation steps.]

## Skill Version(s):

2.4.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
