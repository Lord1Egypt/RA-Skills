## Description: <br>
Tongyi Wanxiang 2.7 video model that supports text-to-video, first/last-frame-to-video, and reference-to-video generation through the dLazy CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request dLazy-hosted Wan2.7 video generation from prompts, images, videos, first and last frames, or audio inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, parameters, and referenced local media to the third-party dLazy cloud service. <br>
Mitigation: Use it only when third-party video generation is intended, avoid sending sensitive prompts or media, and review service terms before use. <br>
Risk: The skill requires a dLazy API key stored in local configuration or supplied through an environment variable. <br>
Mitigation: Protect the API key, restrict local config file access, and rotate or revoke the key from the dLazy dashboard when needed. <br>
Risk: Broad video-generation trigger wording could route generic generation requests to this third-party provider unintentionally. <br>
Mitigation: Invoke the skill with explicit product wording such as Dlazy Wan2.7 or dlazy wan2.7 when routing work to this provider. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlazyai/dlazy-wan2-7) <br>
- [dLazy CLI Homepage](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy Website](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is returned by the dLazy service as hosted output URLs; asynchronous runs may return a generation task identifier for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
