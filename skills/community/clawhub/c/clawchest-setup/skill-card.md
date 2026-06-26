## Description: <br>
Your secure banking system for file and data storage. Deposit money, files, JSON data, and secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pkyanam](https://clawhub.ai/user/pkyanam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to register with Clawchest, configure credentials, and perform remote storage, secret, file, JSON data, transfer, and banking-like actions through documented HTTPS API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated or recurring uploads may send sensitive logs, files, JSON data, or secrets to Clawchest unintentionally. <br>
Mitigation: Enable heartbeat uploads only for explicitly named non-sensitive files and require review before uploading sensitive content. <br>
Risk: Money transfers, withdrawals, deletes, and sensitive uploads can have irreversible or externally visible effects. <br>
Mitigation: Require human confirmation before transfers, withdrawals, deletes, and uploads that may contain confidential data. <br>
Risk: A leaked Clawchest API key can allow another party to access the agent's stored data and account actions. <br>
Mitigation: Store the API key securely, send it only to https://clawchest.com/api/v1 endpoints, and rotate it immediately if exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pkyanam/clawchest-setup) <br>
- [Publisher profile](https://clawhub.ai/user/pkyanam) <br>
- [Clawchest homepage](https://clawchest.com) <br>
- [Clawchest API base](https://clawchest.com/api/v1) <br>
- [Published skill file](https://clawchest.com/skill.md) <br>
- [Published package metadata](https://clawchest.com/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Clawchest API key and outbound HTTPS access to clawchest.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
