## Description: <br>
Official Amazon PA API for product info, prices, and reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcbuer](https://clawhub.ai/user/jcbuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up Amazon product details by ASIN through the Amazon Product Advertising API. It is intended for product information, pricing, review, and commerce-assistant workflows that can supply Amazon Associates credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Amazon access and secret keys, which are sensitive credentials. <br>
Mitigation: Use a credential manager or protected environment configuration, restrict local .env file permissions, and avoid committing or syncing credential files. <br>
Risk: Documentation mentions tracker commands that are not declared in the release metadata. <br>
Mitigation: Expect this version to provide only the declared ama-api lookup command unless additional commands are separately verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcbuer/amazon-paapi) <br>
- [Publisher profile](https://clawhub.ai/user/jcbuer) <br>
- [Amazon Associates](https://affiliate-program.amazon.de/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, and AMAZON_PARTNER_TAG environment configuration. The declared command is ama-api for ASIN lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
