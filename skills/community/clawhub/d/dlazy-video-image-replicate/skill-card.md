## Description: <br>
Studies a user-provided reference image or video and helps recreate the same look and structure with the user's own subject, product, or characters through the dLazy hosted service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users invoke this skill when they want dLazy to analyze a reference image or video and guide recreation of a similar result with their own content. It is suited for project-scoped, multi-turn image or video replication workflows that may include local file attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and attached files are sent to dLazy's hosted API and media storage. <br>
Mitigation: Install only when this data sharing is acceptable, use the pinned npx command if a persistent global CLI is not desired, and rotate or revoke the dLazy API key when needed. <br>
Risk: The skill requires sensitive credentials for dLazy service access. <br>
Mitigation: Authenticate with `dlazy login`, `dlazy auth set`, or `DLAZY_API_KEY`, and keep the saved key restricted to the intended OS user account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-video-image-replicate) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and streamed CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key; file attachments may be uploaded to dLazy media storage through the pinned CLI.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
