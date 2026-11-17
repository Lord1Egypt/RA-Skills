## Description:

Set up email forwarding for custom domains to receive verification codes, password resets, and other emails at a domain you own but don't actively use for email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandonwadepackard-cell](https://clawhub.ai/user/brandonwadepackard-cell)

### License/Terms of Use:


## Use Case:

Domain owners and administrators use this skill to route mail for custom-domain addresses to an accessible inbox for account recovery, verification codes, password resets, or low-cost receive-only email forwarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Catch-all routing and account recovery workflows can expose reset codes or private mail beyond a narrow authorized use.

Mitigation: Use the skill only for domains and accounts you administer, prefer a specific forwarding address, and avoid catch-all routing unless it is necessary.

Risk: Temporary forwarding can continue to route sensitive domain mail after the immediate recovery task is complete.

Mitigation: Disable temporary forwarding after use when it is no longer needed and update recovered accounts to a primary email address.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with provider-specific setup steps, DNS record examples, and verification checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers GoDaddy, Cloudflare Email Routing, Namecheap, and ImprovMX forwarding workflows.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
