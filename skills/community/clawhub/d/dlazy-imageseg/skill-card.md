## Description: <br>
Image matting tool that separates foreground from background and returns a transparent background URL for product images, character cutouts, and composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to call the dLazy image segmentation CLI for foreground extraction and transparent-background image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key that may be stored in the local CLI configuration. <br>
Mitigation: Use OS account protections for the CLI config, prefer per-invocation credentials when appropriate, and rotate or revoke the API key from the dLazy dashboard if exposure is suspected. <br>
Risk: Images passed to the tool may be uploaded to dLazy-hosted endpoints for processing. <br>
Mitigation: Confirm the image content is appropriate for upload to dLazy before running the command, especially for confidential or regulated data. <br>
Risk: A global npm install persists the dLazy CLI on the host. <br>
Mitigation: Use npx @dlazy/cli@1.2.0 for on-demand execution when a persistent global install is not needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dlazyai/dlazy-imageseg) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces image output URLs hosted by files.dlazy.com; async requests may return a task identifier for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
