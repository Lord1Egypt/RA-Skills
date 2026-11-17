## Description:

This skill helps ecommerce and marketing teams generate commercial posters and product images with approved Chinese, English, numeric, and punctuation copy using AI Hive GPT Image 2, plus copy contracts, offline character audits, and targeted typo repair.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, marketing, and design teams use this skill to create Chinese and bilingual commercial image assets where approved copy must be preserved by zone. It is suited for product feature cards, campaign key visuals, social covers, localized ads, package-front concepts, and typo repair workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-selected images and approved copy are sent to AI Hive for generation.

Mitigation: Use only assets and text approved for that service, and avoid sensitive or regulated content unless the data-sharing decision has been reviewed.

Risk: Generated images may still contain incorrect, missing, repeated, or visually malformed text.

Mitigation: Run the offline character audit where applicable and require manual review before publishing; place zero-tolerance text such as legal terms, prices, QR codes, and packaging requirements in a professional layout tool.

Risk: Local setup involves a Python dependency and an API key that can optionally be saved on disk.

Mitigation: Use a virtual environment, pin dependencies when deploying, and provide the key through AI_HIVE_API_KEY when local credential storage is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/chinese-text-commercial-poster-generation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow can submit image-generation jobs, save generated images locally, and run offline character-level audits of expected versus observed copy.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
