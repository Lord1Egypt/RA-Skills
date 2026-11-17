## Description:

Deploy websites and apps to clawdship.dev with zero signup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicodlz](https://clawhub.ai/user/nicodlz)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to package and deploy static sites or Dockerfile-based web apps to Clawdship, then report the live URL, API key handling requirements, billing link, and trial pricing to the human operator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload selected local directories and API credentials to a deployment endpoint.

Mitigation: Verify the deployment path before execution and remove secrets such as .env files, private keys, and other credentials from the packaged directory.

Risk: The deployment API endpoint can be changed through the CLAWDSHIP_API environment variable.

Mitigation: Use the default Clawdship API unless the human operator explicitly approves a trusted alternate endpoint.

Risk: Site deletion, redeploys, custom domain changes, and credit top-ups can affect live services or incur payment actions.

Mitigation: Require explicit human approval before running destructive, production-impacting, domain-management, or payment-related commands.

## Reference(s):

- [Clawdship homepage](https://clawdship.dev)
- [ClawHub skill page](https://clawhub.ai/nicodlz/skills/clawdship)
- [Publisher profile](https://clawhub.ai/user/nicodlz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and deployment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return live site URLs, one-time API keys, billing links, and status or error text from deployment API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
