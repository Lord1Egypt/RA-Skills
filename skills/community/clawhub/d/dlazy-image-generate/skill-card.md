## Description: <br>
Image generation skill that automatically selects the best dLazy CLI image model based on the prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate, edit, replicate, segment, vectorize, or upscale images through the dLazy hosted API from natural-language prompts and optional media references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and can store or use credentials locally. <br>
Mitigation: Use explicit invocation, keep keys scoped to the needed organization, and rotate or revoke keys when access is no longer required. <br>
Risk: Prompts and referenced local media files are sent to dLazy cloud endpoints for inference and storage. <br>
Mitigation: Avoid sending sensitive prompts or files, and confirm uploads before using local media references. <br>
Risk: The install path uses a latest-version third-party CLI package. <br>
Mitigation: Review the dLazy CLI source or package before installation and prefer npx for on-demand execution when a persistent global binary is unnecessary. <br>
Risk: Image generation may consume paid credits or fail when the account balance is insufficient. <br>
Mitigation: Confirm generation intent before running commands and check account credits when the CLI reports insufficient balance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlazyai/dlazy-image-generate) <br>
- [dLazy Homepage](https://dlazy.com) <br>
- [dLazy CLI Source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Markdown, Text] <br>
**Output Format:** [Markdown guidance with dlazy CLI commands and JSON output URLs from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a dLazy API key, npm or npx, network access to api.dlazy.com and files.dlazy.com, and user credits for generation.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
