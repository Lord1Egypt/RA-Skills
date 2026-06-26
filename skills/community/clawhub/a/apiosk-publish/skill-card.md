## Description: <br>
Publish and manage Apiosk gateway listings with signed wallet authentication, listing-group aware categorization, and update/delete operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obcraft](https://clawhub.ai/user/obcraft) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and API publishers use this skill to register, update, list, test, and deactivate Apiosk gateway listings with signed wallet authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles raw wallet private keys for signed Apiosk management requests. <br>
Mitigation: Use a dedicated low-value wallet, avoid passing the private key on the command line, and protect ~/.apiosk/wallet.json with restrictive permissions. <br>
Risk: Signed commands can register, update, list, or deactivate Apiosk gateway listings. <br>
Mitigation: Review the exact slug, endpoint, price, and active status before running register, update, or deactivate commands. <br>
Risk: Installing the skill gives an agent Apiosk listing-management capability. <br>
Mitigation: Install it only when the intended workflow is to manage Apiosk listings. <br>


## Reference(s): <br>
- [Apiosk Publish on ClawHub](https://clawhub.ai/obcraft/apiosk-publish) <br>
- [Apiosk](https://apiosk.com) <br>
- [Apiosk Gateway](https://gateway.apiosk.com) <br>
- [Foundry installation](https://book.getfoundry.sh/getting-started/installation) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, cast, and wallet signing material.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
