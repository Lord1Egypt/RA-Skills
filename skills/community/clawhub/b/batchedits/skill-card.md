## Description: <br>
Autonomously edit videos, add captions, and remove silences via BatchEdits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuckwhisler](https://clawhub.ai/user/chuckwhisler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw to BatchEdits for captioning videos, removing silences, applying reusable editing styles, uploading local videos, starting remote processing jobs, and checking job status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected local videos to BatchEdits for remote processing. <br>
Mitigation: Confirm the exact file path before upload and use the skill only for videos that may be sent to BatchEdits. <br>
Risk: The workflow asks the agent to execute a server-generated curl command. <br>
Mitigation: Inspect the full curl command and destination domain before running it. <br>
Risk: The skill requires a sensitive OAuth client token. <br>
Mitigation: Use a scoped, revocable BatchEdits token and avoid exposing it in shared logs or prompts. <br>


## Reference(s): <br>
- [BatchEdits MCP endpoint](https://batchedits.com/api/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/chuckwhisler/batchedits) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OAuth token setup, MCP server configuration, tool-call sequencing, and upload curl command guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
