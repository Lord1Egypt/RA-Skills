## Description: <br>
Dlazy Website To Video uses the dLazy CLI and hosted website-to-video template to turn a URL or landing page into a promo, social ad, or product demo video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to ask dLazy to capture a website or landing page and generate a project-scoped promotional, social ad, or product demo video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive dLazy credentials. <br>
Mitigation: Keep the API key in the documented local CLI config or DLAZY_API_KEY environment variable, and rotate or revoke it from the dLazy dashboard when needed. <br>
Risk: Prompts, URLs, and files passed with --files are sent to dLazy services. <br>
Mitigation: Use the skill only with data approved for dLazy processing, and avoid submitting confidential files or URLs unless the user has accepted that external-service flow. <br>
Risk: The workflow runs a third-party npm CLI. <br>
Mitigation: Review the pinned @dlazy/cli package or source before use in sensitive environments, and keep the install pinned as documented. <br>


## Reference(s): <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx, a dLazy API key, and network access to api.dlazy.com and files.dlazy.com; attached files may be uploaded to dLazy media storage.] <br>

## Skill Version(s): <br>
1.2.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
