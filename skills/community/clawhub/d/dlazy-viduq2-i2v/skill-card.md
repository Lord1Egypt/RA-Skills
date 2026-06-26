## Description: <br>
Convert static images into dynamic videos using the Vidu Q2 image-to-video model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to invoke dLazy's Vidu Q2 image-to-video CLI for generating short videos from reference images, first and last frames, prompts, and related generation parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, parameters, and media files are sent to dLazy services for generation. <br>
Mitigation: Do not submit sensitive or restricted media unless this use is approved for the user's data policy and dLazy account. <br>
Risk: The dLazy API key may be saved in the local CLI configuration. <br>
Mitigation: Use DLAZY_API_KEY or the npx invocation for less persistent setup when appropriate, and rotate or revoke keys from the dLazy dashboard if exposure is suspected. <br>
Risk: The skill depends on an external npm CLI package. <br>
Mitigation: Use the pinned @dlazy/cli version declared by the skill and review the package or source before installing in sensitive environments. <br>
Risk: Generated outputs are returned as hosted media URLs from dLazy file storage. <br>
Mitigation: Treat returned URLs and generated media as external artifacts and handle them according to the user's retention and sharing requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-viduq2-i2v) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return hosted media URLs, or an asynchronous task identifier when no-wait mode is used.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
