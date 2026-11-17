## Description:

AI-powered website generation and deployment. Generate, edit, and deploy websites to .chilledsites.com in seconds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgosnell](https://clawhub.ai/user/paulgosnell)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to generate, edit, upload, and deploy websites and media through the ChilledSites REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create accounts and use ChilledSites credentials.

Mitigation: Require explicit user confirmation before signup or authenticated API use, and store returned credentials only in approved secret storage.

Risk: Prompts, HTML, CSS, JavaScript, secrets, customer data, or regulated information may be sent to ChilledSites or become part of a hosted site.

Mitigation: Do not submit confidential or regulated content unless sharing it with the service and potentially publishing it is acceptable.

Risk: The skill can upload, edit, delete, and deploy public websites.

Mitigation: Require confirmation before generation, upload, edit, deletion, or deployment, and review the target subdomain and site content before publishing.

Risk: Heartbeat instructions can add recurring ChilledSites checks or prompts to agent behavior.

Mitigation: Add recurring instructions only when the user intentionally wants ongoing ChilledSites activity and knows how to remove it.

## Reference(s):

- [ChilledSites App](https://chilledsites.com)
- [ChilledSites API Base](https://api.chilledsites.com)
- [OpenClaw Setup Guide](https://chilledsites.com/for-openclaw)
- [ClawHub Skill Page](https://clawhub.ai/paulgosnell/skills/chilledsites)
- [Publisher Profile](https://clawhub.ai/user/paulgosnell)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ChilledSites API credentials and may produce hosted website URLs, generated site code, media generation requests, and account or token status responses.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
