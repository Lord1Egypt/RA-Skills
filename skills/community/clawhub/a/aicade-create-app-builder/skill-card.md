## Description: <br>
Build general aicade application prompts by taking the user's base prompt plus the platform additions from the bundled 3.1 workflow reference, then assembling a final integrated prompt in the style of 3.2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aicadegalaxy](https://clawhub.ai/user/aicadegalaxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to assemble a final prompt for building or migrating an aicade app that follows the documented platform workflow, SDK integration order, iframe constraints, and upload preparation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill participates in setup for API credentials and upload preparation. <br>
Mitigation: Use local input methods for secrets when possible, keep .env files out of version control, and redact secrets from confirmations and logs. <br>
Risk: The workflow asks the agent to restate resolved upload variables before upload. <br>
Mitigation: Confirm only that required variables are present or masked, and review generated upload steps before running them. <br>
Risk: Generated prompts can influence payment, wallet, points, token, NFT, or market-related application behavior. <br>
Mitigation: Review generated prompts and application code for correct SDK module selection, platform constraints, and business rules before deployment. <br>


## Reference(s): <br>
- [Prompt Workflow](references/prompt-workflow.md) <br>
- [aicade SDK Capabilities](references/sdk-capabilities.md) <br>
- [aicade TS Bootstrap](https://github.com/aicade-galaxy/aicade-ts-bootstrap) <br>
- [aicade TS Bootstrap README](https://github.com/aicade-galaxy/aicade-ts-bootstrap/blob/main/README.md) <br>
- [aicade Galaxy](https://www.aicadegalaxy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prompt text with JSON spec inputs and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect local project environment values and write requested aicade API settings to a project .env file.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
