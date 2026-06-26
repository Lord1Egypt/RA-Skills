## Description: <br>
Connect Tool Library helps agents manage CogenticLink tool library tokens, browse remote tool categories and schemas, and execute remote CLI, API, and MCP tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cogenticlab](https://clawhub.ai/user/cogenticlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure access to CogenticLink tool libraries, inspect available tool categories and schemas, and call remote tools through the CogenticLink CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens may be exposed if pasted directly into shell commands or retained in shell history. <br>
Mitigation: Prefer environment variables, secure prompts, or a credential store; rotate any token that may have been exposed. <br>
Risk: Stored tool library credentials may remain available after the intended work is complete. <br>
Mitigation: Remove unused libraries from the local CogenticLink configuration when access is no longer needed. <br>


## Reference(s): <br>
- [Connect Tool Library on ClawHub](https://clawhub.ai/cogenticlab/connect-tool-library) <br>
- [CogenticLink npm package](https://www.npmjs.com/package/cogenticlink) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide tool calls that return JSON content arrays or error details from CogenticLink.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
