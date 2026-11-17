## Description:

Publish and manage Apiosk gateway listings with signed wallet authentication, listing-group aware categorization, and update/delete operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obcraft](https://clawhub.ai/user/obcraft)

### License/Terms of Use:

MIT

## Use Case:

Developers and API publishers use this skill to register, list, update, test, and deactivate paid API listings on the Apiosk gateway with signed wallet authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys are used for request signing and may be supplied through a local wallet file, environment variable, or command-line flag.

Mitigation: Use a dedicated low-value wallet or safer signer, avoid passing private keys on the command line, and protect ~/.apiosk/wallet.json permissions.

Risk: Update and delete actions can change or deactivate Apiosk listings.

Mitigation: Manually confirm the exact slug and wallet before running update or delete actions.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/obcraft/skills/apiosk-publish)
- [Apiosk](https://apiosk.com)
- [Apiosk Gateway](https://gateway.apiosk.com)
- [Foundry Installation](https://book.getfoundry.sh/getting-started/installation)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance for Apiosk publishing scripts that call gateway endpoints and require curl, jq, cast, and wallet signing material.]

## Skill Version(s):

1.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
