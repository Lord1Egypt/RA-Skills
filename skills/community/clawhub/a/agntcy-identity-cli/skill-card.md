## Description: <br>
AGNTCY Identity Issuer CLI and Node Backend for managing verifiable agent identities, metadata, and badges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jadiaconu](https://clawhub.ai/user/jadiaconu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to work with AGNTCY identity issuer workflows, including creating identities, managing issuer configuration, issuing badges, publishing verifiable credentials, and verifying published badges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CLIENT_SECRET and local vault contents may expose sensitive OAuth credentials or signing key material. <br>
Mitigation: Use a dedicated test vault and scoped test OAuth client first, and avoid pasting secrets or vault contents into chat, logs, tickets, or issue trackers. <br>
Risk: Production signing keys could be affected if commands are run against a production vault before review. <br>
Mitigation: Review the upstream Go module or backend scripts and validate the workflow in a controlled environment before using production signing keys. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jadiaconu/agntcy-identity-cli) <br>
- [AGNTCY Identity Project Homepage](https://github.com/agntcy/identity) <br>
- [AGNTCY Identity Issuer Go Module](https://github.com/agntcy/identity/cmd/issuer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference identity CLI commands, issuer URLs, OAuth client settings, and local vault configuration paths.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
