## Description: <br>
Build agent-facing web experiences with ATXP-based authentication, following the ClawDirect pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[napoleond](https://clawhub.ai/user/napoleond) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build agent-facing web applications with ATXP authentication, MCP tools, cookie-based browser access, and optional payment-enabled actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sample auth-cookie bootstrap pattern needs production hardening before deployment. <br>
Mitigation: Prefer a short-lived one-time exchange code; otherwise use HTTPS, immediate redirects, strict query logging controls, Secure/HttpOnly/SameSite cookies, token expiry, revocation, hashed token storage, and pinned npm dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/napoleond/clawdirect-dev) <br>
- [ClawDirect reference implementation](https://github.com/napoleond/clawdirect) <br>
- [ATXP documentation](https://skills.sh/atxp-dev/cli/atxp) <br>
- [ClawDirect directory](https://claw.direct) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, JSON, environment variable, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation templates and setup guidance for agent-facing web applications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
