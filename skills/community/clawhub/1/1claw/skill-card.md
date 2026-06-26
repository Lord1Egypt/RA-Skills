## Description: <br>
HSM-backed secret management for AI agents: store, retrieve, rotate, and share secrets via the 1Claw vault without exposing them in context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kmjones1979](https://clawhub.ai/user/kmjones1979) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to fetch, store, rotate, share, and delete vault secrets just in time, and to simulate or submit HSM-backed transaction-signing requests without placing private credentials in conversation context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, write, delete, and share vault secrets. <br>
Mitigation: Use a dedicated agent API key, bind it to the intended vault, and grant only the paths and actions needed for the task. <br>
Risk: Sharing, deletion, policy changes, and transaction broadcasts can expose or alter sensitive assets. <br>
Mitigation: Require explicit user approval before those actions and prefer simulation before transaction submission. <br>
Risk: The skill depends on the external @1claw/mcp package for MCP operation. <br>
Mitigation: Review or pin the external package before granting access to important secrets. <br>
Risk: Retrieved secret values could be exposed if echoed into agent responses or logs. <br>
Mitigation: Fetch secrets just in time, use them directly for the intended call, and do not summarize or store raw values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kmjones1979/1claw) <br>
- [1Claw dashboard](https://1claw.xyz) <br>
- [1Claw documentation](https://docs.1claw.xyz) <br>
- [1Claw MCP package](https://www.npmjs.com/package/@1claw/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code] <br>
**Output Format:** [Markdown with inline JSON, bash, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers MCP, SDK, REST, vault, secret, sharing, and transaction-signing workflows.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
