## Description: <br>
A professional storyboard skill for film, advertising, short video, and educational narrative scenarios, built around a strict 'plan first, render later' flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and production teams use this skill to turn creative briefs into confirmed storyboard plans, character references, structured panel prompts, and generated image deliveries for cinematic or narrative projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may store credentials in local CLI configuration. <br>
Mitigation: Use the documented dLazy authentication flow or per-run DLAZY_API_KEY values, rotate or revoke keys when needed, and avoid shared machines for persistent credentials. <br>
Risk: Prompts and selected local media files may be sent to dLazy cloud services for generation. <br>
Mitigation: Use the skill only with content approved for dLazy processing, and avoid confidential prompts or media unless the user's organization permits that data flow. <br>
Risk: The workflow depends on the third-party dLazy CLI and hosted API. <br>
Mitigation: Prefer npx for ephemeral use when appropriate, review the CLI source or npm package before sensitive work, and install only if third-party cloud generation is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/image-storyboard) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with bulleted workflow updates, inline shell commands, structured prompt drafts, and generated image URLs when CLI execution succeeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plan-first workflow with explicit confirmation gates and one synchronous generation command at a time.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
