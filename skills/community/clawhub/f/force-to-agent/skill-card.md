## Description: <br>
Extract AGENTS.md, SOUL.md, TOOLS.md, and an optional openclaw.json patch from pasted custom-GPT markdown, then create a new workspace-<agent> folder and write the files there instead of overwriting the current workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nga-khan](https://clawhub.ai/user/nga-khan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to convert pasted custom-GPT or FORCE-to-OpenClaw markdown into a separate OpenClaw workspace with AGENTS.md, SOUL.md, TOOLS.md, and an optional openclaw.json patch candidate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted agent markdown from untrusted sources can produce workspace files that contain unsafe or misleading behavior. <br>
Mitigation: Review the generated AGENTS.md, SOUL.md, TOOLS.md, and any optional openclaw.json patch before running the new workspace. <br>
Risk: An openclaw.json patch candidate can change tool or skill configuration if explicitly applied. <br>
Mitigation: Apply configuration changes only inside the newly created workspace and confirm the requested keys before merging them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nga-khan/force-to-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summary with generated workspace file paths and optional configuration patch guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or describes AGENTS.md, SOUL.md, TOOLS.md, and optional openclaw.json patch candidates in a separate workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
