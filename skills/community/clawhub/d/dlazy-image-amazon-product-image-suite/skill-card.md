## Description: <br>
A professional product image generation skill purpose-built for the Amazon e-commerce platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketplace operators, and agents use this skill to plan and generate Amazon-ready product image sets, including main images, secondary images, and A+ Brand Content modules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may store credentials in local CLI configuration. <br>
Mitigation: Protect the local dLazy configuration, prefer per-session environment variables when persistence is not desired, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Prompts and uploaded product media are sent to dLazy cloud services for generation. <br>
Mitigation: Upload only product media approved for transfer to dLazy, and avoid including confidential or regulated content unless the user's organization has approved that use. <br>
Risk: Generated product images can be inaccurate, non-compliant, or misleading for marketplace use. <br>
Mitigation: Review generated images against Amazon image requirements, product facts, brand rules, and applicable advertising claims before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/image-amazon-product-image-suite) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx, a dLazy API key, and access to dLazy API and file-hosting endpoints.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
