## Description: <br>
Helps agents use the official YouMind CLI and API to discover available operations, inspect schemas, and work with YouMind boards, notes, materials, chats, skills, and scheduled tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cellinlab](https://clawhub.ai/user/cellinlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a YouMind account through the official CLI, including discovering APIs, checking request schemas, and carrying out read or write tasks on YouMind content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a YouMind API key and can operate a user's YouMind account. <br>
Mitigation: Install only when that account access is intended; use a limited or revocable API key where available, avoid exposing secrets in chat or shell history, and verify the @youmind-ai/cli package source. <br>
Risk: The skill can trigger account-changing operations such as publishing, trashing content, installing skills, or creating scheduled tasks. <br>
Mitigation: Use read-first API discovery and schema inspection for non-trivial actions, and require explicit user confirmation before destructive, publishing, installation, or scheduled-task operations. <br>


## Reference(s): <br>
- [Skill homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/youmind) <br>
- [YouMind service endpoint](https://youmind.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI command plans, schema summaries, API call parameters, and concise operation results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
