## Description: <br>
Monitor home lab servers via Beszel (PocketBase). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karakuscem](https://clawhub.ai/user/karakuscem) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and home lab operators use this skill to query Beszel for server health and container CPU usage from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Beszel credentials and may expose monitoring access if broad credentials are used or stored in shared shell startup files. <br>
Mitigation: Use a limited Beszel account, keep credentials out of broadly loaded shell startup files, and rotate credentials if access is exposed. <br>
Risk: The skill contains unexplained guidance that could lead users to share Beszel server access with an unknown Gmail account. <br>
Mitigation: Do not share the Beszel server with jenny@gmail.com unless you personally know and trust that account. <br>
Risk: The default Beszel endpoint is local HTTP, which may be inappropriate for remote or shared networks. <br>
Mitigation: Prefer a local-only endpoint or an HTTPS-only Beszel endpoint before using the skill with real monitoring data. <br>


## Reference(s): <br>
- [Beszel Check on ClawHub](https://clawhub.ai/karakuscem/beszel-check) <br>
- [karakuscem ClawHub profile](https://clawhub.ai/user/karakuscem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown-formatted terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and Beszel connection credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
