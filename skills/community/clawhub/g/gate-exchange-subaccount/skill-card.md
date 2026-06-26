## Description: <br>
Gate Exchange sub-account management skill for querying, listing, creating, locking, and unlocking Gate sub-accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate users and operators use this skill to manage normal Gate sub-accounts through the Gate MCP server, including status checks, listing, creation, locking, and unlocking with main-account authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Gate main-account authority for sub-account management. <br>
Mitigation: Use a least-privileged Gate API key limited to sub-account management and confirm every create, lock, or unlock action before execution. <br>
Risk: Top-priority runtime rules are delegated to a remote Gate rules file outside the reviewed artifact. <br>
Mitigation: Review the remote Gate runtime rules and the Gate MCP installation before use; stop write actions if the rules, authentication, or MCP availability cannot be verified. <br>
Risk: Create, lock, and unlock operations can change account access and trading state. <br>
Mitigation: Validate the target UID or login name, check current state before writes, and re-query status after execution. <br>


## Reference(s): <br>
- [Gate Sub-Account MCP Specification](references/mcp.md) <br>
- [Gate Exchange Sub-Account Scenarios](references/scenarios.md) <br>
- [Gate MCP](https://github.com/gate/gate-mcp) <br>
- [Gate Skills Repository](https://github.com/gate/gate-skills) <br>
- [Gate Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown responses with MCP tool calls, confirmation prompts, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gate MCP, Gate API-key authentication, main-account privileges, and explicit confirmation before create, lock, or unlock operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter version 2026.3.23-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
