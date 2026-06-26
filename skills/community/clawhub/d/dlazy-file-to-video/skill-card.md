## Description: <br>
Dlazy File To Video helps turn PPT, Word, Excel, PDF, and other document inputs into explainer, report, courseware, or training video workflows through the dLazy hosted agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to start or continue dLazy file-to-video projects from document inputs, including explainer videos, report broadcasts, courseware, and training videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requires sensitive dLazy credentials and may send prompts, options, and attached files to dLazy API and file-storage endpoints. <br>
Mitigation: Install only if the publisher and hosted service are trusted, avoid uploading sensitive files unless policy permits it, and rotate or revoke dLazy API keys when access should change. <br>
Risk: The authoritative security evidence marks the release suspicious and says it should be reviewed before installation. <br>
Mitigation: Review the skill bundle and referenced CLI before use, and avoid running it in sensitive repositories or environments until the review is complete. <br>


## Reference(s): <br>
- [Dlazy File To Video on ClawHub](https://clawhub.ai/dlazyai/dlazy-file-to-video) <br>
- [ClawHub publisher profile: dlazyai](https://clawhub.ai/user/dlazyai) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires dLazy API credentials; attached local files may be uploaded through the dLazy CLI before being referenced by the hosted agent.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
