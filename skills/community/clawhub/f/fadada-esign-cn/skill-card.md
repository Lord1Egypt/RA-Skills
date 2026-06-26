## Description: <br>
Provides FaDaDa FASC API 5.0 electronic contract signing workflows, including contract sending, signing status checks, and signed contract downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fadada-esign](https://clawhub.ai/user/fadada-esign) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operations teams use this skill to integrate FaDaDa electronic signing into HR contracts, sales agreements, and other document approval workflows. It helps agents prepare configuration, call signing APIs, send contracts, query task status, and retrieve signed documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send, download, or cancel contract signing workflows that affect real agreements. <br>
Mitigation: Confirm the contract, signer identities, phone numbers, provider endpoint, task IDs, and output paths before running send, batch, download, or cancel commands. <br>
Risk: FaDaDa application credentials and signing links are sensitive. <br>
Mitigation: Use environment variables or a secure secret store for API secrets, restrict config-file permissions, and treat signing links as confidential. <br>
Risk: Downloaded signed contracts may contain confidential personal or business information. <br>
Mitigation: Store downloaded contracts only in approved locations and limit access according to the organization's document handling policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fadada-esign/fadada-esign-cn) <br>
- [FaDaDa Open Platform](https://www.fadada.com/) <br>
- [FASC API 5.0 documentation](https://docs.fadada.com/) <br>
- [API reference](references/api_reference.md) <br>
- [Data models](references/data_models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples plus JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce FaDaDa API request guidance, CLI commands, configuration files, and status or download workflow instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
