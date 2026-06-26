## Description: <br>
Build and launch low-cost digital products for Gumroad, itch.io, and DriveThruRPG using Pillow for image assets and Groq for product listing copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sabroo3-commits](https://clawhub.ai/user/sabroo3-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and agents use this skill to prepare downloadable digital products, including cover images, asset bundles, platform listing copy, and storefront setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Groq API keys or confidential product details could be exposed through environment files, logs, commits, or prompts sent to Groq. <br>
Mitigation: Store the Groq key outside version control, avoid printing it, and keep secrets, customer data, and confidential plans out of prompts. <br>
Risk: The skill asks the agent to install and use Pillow before generating image assets. <br>
Mitigation: Install dependencies only in an approved environment and review generated files before publishing or distributing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sabroo3-commits/digital-product-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Python, and JavaScript code blocks; generated work products may include PNG images, ZIP bundles, and product listing text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Pillow for local image creation and Groq for external copy generation when a Groq API key is configured.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
