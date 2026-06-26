## Description: <br>
Persist, refresh, and serve website session cookies through a local SQLite-backed cookie store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanmwx](https://clawhub.ai/user/seanmwx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to keep authenticated website session cookies available to local tools without building full browser automation. It supports storing cookie profiles, refreshing them through deterministic HTTP requests, and exporting current cookies as headers or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live login cookies may grant account access if the SQLite database or command output is exposed. <br>
Mitigation: Store databases only on trusted local machines, restrict file access, avoid shared environments and CI logs, and treat exported Cookie headers and JSON as secrets. <br>
Risk: Refreshing against untrusted or non-HTTPS endpoints could disclose session cookies. <br>
Mitigation: Use only trusted HTTPS refresh URLs and prefer lightweight authenticated endpoints such as /ping, /me, or /heartbeat. <br>
Risk: The optional local HTTP wrapper can expose cookies to other processes if bound broadly or left unauthenticated. <br>
Mitigation: Keep the wrapper bound to localhost and add authentication before exposing it beyond the local machine. <br>
Risk: Sites that require JavaScript timers, WebSocket traffic, or browser-only activity may not stay logged in through deterministic HTTP refreshes. <br>
Mitigation: Use browser automation to renew those sessions and write the updated cookies back through the upsert workflow. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [Cookie Alive Pro on ClawHub](https://clawhub.ai/seanmwx/cookie-alive) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, Cookie header strings, and JSON cookie records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local SQLite cookie databases under ~/.cookie_alive unless environment variables override the storage path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
