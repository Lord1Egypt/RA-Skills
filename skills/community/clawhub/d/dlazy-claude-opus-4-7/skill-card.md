## Description: <br>
Anthropic's flagship multimodal model for long-context reasoning, code generation, and complex tool orchestration with text, image, and video inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can invoke the dLazy CLI to send prompts and optional image or video inputs to a hosted Claude Opus 4.7 model endpoint for reasoning, code generation, and multimodal analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and uses an authenticated CLI. <br>
Mitigation: Install and authenticate only when you trust the publisher, and use credentials only in accounts and repositories where those permissions are appropriate. <br>
Risk: Prompts and referenced local image or video files may be sent to dLazy API and storage endpoints. <br>
Mitigation: Review inputs before execution and avoid sending confidential or restricted files unless the service terms and account controls are acceptable. <br>
Risk: The skill depends on installing or invoking the third-party @dlazy/cli package. <br>
Mitigation: Use the pinned package version from the skill metadata and review the package source and install path before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-claude-opus-4-7) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy service](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON responses from the dLazy CLI, often containing model-generated text or structured output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Async mode may return a generation identifier for later polling.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
