## Description: <br>
A workflow skill for marketing brochure design that guides requirements gathering, layout-first design, confirmation, and brochure mock-up delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, marketers, and agents use this skill to plan brochure content, generate layout-first artwork, wait for explicit layout approval, and then produce folded and lifestyle mock-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires a dLazy API key that may be stored in the local CLI configuration. <br>
Mitigation: Use DLAZY_API_KEY or npx when avoiding a long-lived global install or saved credential, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Prompts and selected media files are sent to dLazy cloud services for generation. <br>
Mitigation: Review prompts and media before execution and avoid sending confidential or regulated content unless the user has approved that cloud processing path. <br>
Risk: The workflow depends on a third-party CLI and cloud API. <br>
Mitigation: Install only if comfortable with the third-party dLazy CLI and cloud service; prefer the pinned package version and review the published source or npm package before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/image-marketing-brochure) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy website](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with prompt drafts, confirmation checkpoints, synchronous dLazy CLI commands, and generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx and a dLazy API key; image generation uses the dLazy CLI and cloud API.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
