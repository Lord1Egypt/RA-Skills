## Description: <br>
Generate high-quality SVG vector graphics from text using Recraft v3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to invoke dLazy's Recraft v3 SVG generation CLI from text prompts, with aspect ratio and style controls for vector graphic generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and stores it in local CLI configuration unless an environment variable is used. <br>
Mitigation: Use per-invocation environment variables when persistence is not desired, and rotate or revoke the key from the dLazy dashboard when access should end. <br>
Risk: Prompts and explicitly referenced files are sent to dLazy-hosted API and media endpoints for generation. <br>
Mitigation: Use the skill only with prompts and files that are appropriate to send to dLazy, and avoid sensitive content unless the user's organization permits that use. <br>
Risk: The workflow depends on an external paid cloud service and can fail for missing credentials, insufficient balance, policy rejection, or service errors. <br>
Mitigation: Check authentication and account credits before use, handle returned error codes clearly, and use dry-run or async polling options when appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlazyai/dlazy-recraft-v3-svg) <br>
- [dLazy CLI Source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy Homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated results are returned as hosted file URLs; async mode may return a generateId for polling.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
