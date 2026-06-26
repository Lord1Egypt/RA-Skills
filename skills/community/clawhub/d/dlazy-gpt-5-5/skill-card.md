## Description: <br>
OpenAI's general-purpose model balancing reasoning quality with response speed for chat, writing, planning, and multimodal analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call the dLazy GPT 5.5 command-line interface for general-purpose language and multimodal tasks, including chat, writing, planning, code-oriented responses, and analysis of supplied image or video inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and stores or reads credentials through the dLazy CLI. <br>
Mitigation: Use organization-scoped API keys, keep them in the CLI config or environment as documented, and rotate or revoke keys from the dLazy dashboard when access changes. <br>
Risk: Prompts and referenced image or video files may be sent to dLazy API and media storage endpoints for processing. <br>
Mitigation: Review prompts and file paths before invocation, avoid sending confidential or regulated data unless permitted, and use dry-run behavior where appropriate to inspect requests before calling the API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-gpt-5-5) <br>
- [dLazy CLI homepage](https://github.com/dlazyai/cli) <br>
- [dLazy npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, json] <br>
**Output Format:** [JSON envelope containing generated outputs or async task status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the dLazy CLI, npm or npx, and a dLazy API key; prompts and referenced media files may be sent to dLazy API and media storage endpoints.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
