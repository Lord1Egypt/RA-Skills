## Description: <br>
Provides agent guidance and curl-based DingTalk Notable API workflows for managing AI table sheets, fields, and records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breath57](https://clawhub.ai/user/breath57) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operators use this skill to configure DingTalk app credentials and operate DingTalk AI tables. It supports sheet, field, and record management tasks, including list, create, update, query, and delete workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores DingTalk credentials and tokens in a local configuration file. <br>
Mitigation: Use a least-privileged DingTalk app, avoid shared machines, restrict permissions on the local config file, and do not print full credentials in agent responses. <br>
Risk: The skill can create, update, or delete DingTalk AI table sheets, fields, and records. <br>
Mitigation: Require explicit user confirmation of the target base, sheet, field, or record IDs before any destructive operation. <br>
Risk: Cached DingTalk tokens may become invalid before their cached expiry time. <br>
Mitigation: On DingTalk 401 responses, bypass the cache with the documented nocache token refresh flow before retrying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/breath57/dingtalk-ai-table-only-curl) <br>
- [DingTalk AI table API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include DingTalk API request and response examples, configuration key checks, and credential-handling guidance.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
