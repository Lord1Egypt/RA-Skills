## Description: <br>
Automates collection of product data from 1688 and prepares or uploads product listings to OZON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z4201812](https://clawhub.ai/user/z4201812) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace operators and agents use this skill to turn a 1688 product URL, weight, and purchase price into OZON listing data, translated images, pricing, and an upload workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled real-looking credentials may expose third-party accounts or let the skill act with unintended authority. <br>
Mitigation: Replace and rotate every bundled credential before installation, then load secrets from a controlled user configuration or environment variables. <br>
Risk: Normal runs can perform live OZON publishing and stock updates. <br>
Mitigation: Use debug mode, a test seller account, or a mandatory manual confirmation gate before any upload step. <br>
Risk: Product data and images may be sent to OCR, translation, image-hosting, and optional Feishu services. <br>
Mitigation: Run in an isolated workspace, confirm each external destination is approved, and disable Feishu unless notifications are explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/z4201812/1688-to-ozon) <br>
- [Publisher profile](https://clawhub.ai/user/z4201812) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [README_OZON_PUBLISHER.md](README_OZON_PUBLISHER.md) <br>
- [toy_set_mapping.md](scripts/mappings/toy_set_mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON files, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown progress and reports, JSON product and pricing files, image URLs, and OZON API upload results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, agent-browser, marketplace API credentials, and external OCR, translation, image-hosting, and optional Feishu services.] <br>

## Skill Version(s): <br>
1.0.71 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
