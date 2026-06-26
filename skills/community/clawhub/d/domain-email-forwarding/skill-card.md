## Description: <br>
Set up email forwarding for custom domains to receive verification codes, password resets, and other messages at an accessible inbox using GoDaddy, Namecheap, Cloudflare Email Routing, or ImprovMX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandonwadepackard-cell](https://clawhub.ai/user/brandonwadepackard-cell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Domain owners, administrators, and account recovery users use this skill to route mail for domains they control to an inbox they can access, especially for verification codes, password resets, catch-all forwarding, or low-cost receive-only domain email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing MX records or forwarding settings can interrupt existing domain mail delivery. <br>
Mitigation: Use the skill only for domains you own or administer, save the current DNS and MX settings first, and check whether existing mailboxes depend on the current configuration. <br>
Risk: Catch-all or broad forwarding can route sensitive messages for many addresses at the domain to one inbox. <br>
Mitigation: Forward only to an inbox you control, test forwarding before relying on it, and remove or narrow temporary forwarding after the recovery or routing task is complete. <br>
Risk: Account recovery codes and password reset emails are sensitive and can change account access. <br>
Mitigation: Use forwarding only for accounts and domains you are authorized to administer, then update recovered accounts to a current primary email address. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with setup steps, decision tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes provider-specific DNS and forwarding guidance; no executable code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
