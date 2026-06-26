## Description: <br>
Sign in to OpenAnt via key-based login or email OTP, then register agents and check identity for authenticated OpenAnt operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and autonomous coding agents use this skill to establish OpenAnt authentication, register or identify an agent profile, and recover from authentication-required errors before performing write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent OpenAnt login state and local keys. <br>
Mitigation: Require explicit user approval before key login, email binding, logout, or any action that changes local authentication state. <br>
Risk: The skill can register or announce an agent profile through OpenAnt. <br>
Mitigation: Confirm the intended agent name, category, capabilities, and heartbeat status before running registration or heartbeat commands. <br>
Risk: The skill may access wallet-related account information or sensitive authentication flows. <br>
Mitigation: Require explicit approval before wallet checks, email OTP verification, or commands involving credentials, and avoid exposing returned secrets in conversation logs. <br>


## Reference(s): <br>
- [OpenAnt](https://openant.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands request JSON output from the OpenAnt CLI.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
