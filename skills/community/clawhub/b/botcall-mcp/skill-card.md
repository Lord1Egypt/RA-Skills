## Description: <br>
Give your AI agent a real phone number for SMS verification. Provisions numbers, receives SMS, and extracts verification codes via the botcall API. Requires a BOTCALL_API_KEY from botcall.io. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danecodes](https://clawhub.ai/user/danecodes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use botcall-mcp to connect an MCP-capable agent to Botcall so it can provision phone numbers, read SMS messages, and retrieve verification codes for authorized workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to Botcall phone numbers and SMS messages, including verification codes. <br>
Mitigation: Use it only for accounts and services you are authorized to manage, and avoid exposing verification codes in prompts or logs. <br>
Risk: BOTCALL_API_KEY is required and can authorize Botcall API usage. <br>
Mitigation: Protect BOTCALL_API_KEY like a password, store it in environment configuration, and rotate it if it is exposed. <br>
Risk: The release is installed through an npm package before the MCP server runs. <br>
Mitigation: Review the npm package before running it in environments where phone numbers, SMS messages, or account workflows are sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danecodes/botcall-mcp) <br>
- [Botcall](https://botcall.io) <br>
- [npm package](https://www.npmjs.com/package/botcall-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration, guidance] <br>
**Output Format:** [Markdown setup guidance and MCP tool outputs containing phone numbers, SMS messages, verification codes, and usage data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BOTCALL_API_KEY; get_code may long-poll for up to 30 seconds.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
