## Description:

Manage Ghost CMS content via the REST API. Create and publish posts, manage tags, and fetch site analytics. Supports both the Content API for public data and the Admin API for authenticated management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to manage Ghost CMS posts, tags, and site statistics from an agent-assisted command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Ghost Admin API credentials unsafely and can publish or modify live content with limited safeguards.

Mitigation: Use a test Ghost site or a tightly scoped integration key, verify GHOST_URL is the exact HTTPS endpoint you trust, and rotate any Admin API key already used with these scripts.

Risk: Agent-suggested commands can create, update, or publish CMS content unintentionally.

Mitigation: Review proposed commands and generated post content before execution, and omit publishing flags unless immediate publication is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kryzl19/skills/ghost-cms-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands and JSON or table command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GHOST_URL and GHOST_ADMIN_API_KEY environment variables; commands may read, create, update, or publish Ghost CMS content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
