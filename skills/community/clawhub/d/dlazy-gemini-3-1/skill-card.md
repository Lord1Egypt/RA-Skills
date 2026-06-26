## Description: <br>
Google's multimodal model with strong long-context and vision understanding, suitable for document parsing, image/video understanding, and structured output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call the dLazy CLI for Gemini 3.1 multimodal generation, including text prompts, image or video inputs, document parsing, and structured output workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious and reports guidance involving helper scripts with full unsandboxed authority. <br>
Mitigation: Review bundled helper scripts before use, disable autoreview full-access mode with `--no-yolo` or `AUTOREVIEW_YOLO=0`, and only grant tool access intentionally. <br>
Risk: The skill requires sensitive credentials for dLazy API access. <br>
Mitigation: Use scoped API keys, store them through the documented dLazy CLI configuration or environment variable flow, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Prompts and referenced image or video files may be sent to dLazy API and media storage endpoints. <br>
Mitigation: Avoid sending confidential or regulated content unless the user's organization has approved dLazy's service terms and data handling for that use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-gemini-3-1) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON responses from the dLazy CLI, with optional Markdown guidance and shell commands for setup or troubleshooting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key and may return asynchronous task identifiers when invoked with no-wait mode.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
