## Description:

Automate Amplitude tasks via Rube MCP (Composio): events, user activity, cohorts, user identification. Always search tools first for current schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

Developers and analytics operators use this skill to guide agents through Amplitude workflows via Rube MCP, including sending events, finding users, retrieving activity, managing cohorts, and updating user properties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent access to Amplitude through Rube can expose user activity and make production analytics changes such as sending events, updating user properties, or modifying cohorts.

Mitigation: Use least-privilege Amplitude credentials, confirm the target project and environment, avoid unnecessary user activity queries, and require explicit review before production writes or cohort changes.

Risk: Stale schemas, Amplitude internal ID requirements, rate limits, and asynchronous cohort updates can cause failed or incorrect operations.

Mitigation: Search Rube tools for current schemas first, resolve Amplitude internal user IDs before activity queries, batch or chunk large operations, and check asynchronous cohort operation status.

## Reference(s):

- [Rube MCP endpoint](https://rube.app/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with tool sequences, parameter notes, tables, and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires active Rube MCP and an authenticated Amplitude connection; runtime tool schemas should be searched before use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
