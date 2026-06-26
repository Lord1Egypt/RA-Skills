## Description: <br>
Uses the dLazy CLI and hosted product-to-ecommerce-video template to help agents turn product specs, manuals, catalogs, or marketplace listings into conversion-focused shopping video workflows with multilingual voiceover and an optional virtual host. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ecommerce sellers, marketers, and agents supporting product promotion use this skill to start or continue dLazy projects that transform product materials and marketplace listings into shopping-video generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may store credentials in the user's local CLI configuration or read them from the DLAZY_API_KEY environment variable. <br>
Mitigation: Protect the local dLazy configuration and environment variables, and rotate or revoke the organization API key from the dLazy dashboard if exposure is suspected. <br>
Risk: Files attached with the CLI are uploaded to dLazy media storage before being referenced by the hosted agent. <br>
Mitigation: Attach only files intended for upload and review product materials for sensitive or regulated data before invoking the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-product-to-ecommerce-video) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-oriented terminal guidance and dLazy CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx and a dLazy API key; attached local files are uploaded through the dLazy CLI before the hosted agent references them.] <br>

## Skill Version(s): <br>
1.2.2 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
