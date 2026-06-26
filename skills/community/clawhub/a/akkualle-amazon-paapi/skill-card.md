## Description: <br>
Searches Amazon products and retrieves product details using Amazon Product Advertising API (PA-API), including support for price lookups and affiliate links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akkualle](https://clawhub.ai/user/akkualle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, commerce operators, and affiliate publishers use this skill to search Amazon.de products, retrieve product details by ASIN, and prepare affiliate-linked product information through PA-API-backed commands. <br>

### Deployment Geography for Use: <br>
Global; configured by default for the Amazon.de marketplace. <br>

## Known Risks and Mitigations: <br>
Risk: Amazon PA-API credentials could be exposed if provided through an untrusted shell, shared logs, or committed configuration. <br>
Mitigation: Provide AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, and AMAZON_PARTNER_TAG only through a trusted local environment or secret manager, and avoid printing or committing those values. <br>
Risk: The skill references amazon-search and amazon-product commands but does not include executable code, so a local command with those names could come from an untrusted source. <br>
Mitigation: Confirm the installed amazon-search and amazon-product executables are expected and trusted before using this skill. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/akkualle/akkualle-amazon-paapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Amazon PA-API access key, secret key, and partner tag; defaults target webservices.amazon.de and eu-west-1 unless configured otherwise.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
