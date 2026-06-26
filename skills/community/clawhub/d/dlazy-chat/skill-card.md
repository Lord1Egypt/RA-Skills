## Description: <br>
Chat with the dLazy sandbox agent, a project-scoped assistant that runs skills end-to-end over multiple turns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to discover dLazy skills and projects, then start or continue project-scoped chat sessions with the hosted sandbox agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, project context, and files attached with --files are sent to dLazy hosted services. <br>
Mitigation: Use the skill only with data appropriate for dLazy's service, and avoid attaching sensitive files unless approved for that environment. <br>
Risk: The skill requires a dLazy API key that may be stored locally or supplied through DLAZY_API_KEY. <br>
Mitigation: Protect the API key, restrict access on shared machines, and rotate or revoke the key if the machine or configuration is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-chat) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and streamed CLI text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx and a dLazy API key; attached files may be uploaded to dLazy storage.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
