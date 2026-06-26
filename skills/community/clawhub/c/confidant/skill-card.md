## Description: <br>
Secure secret handoff and credential setup wizard for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericsantos](https://clawhub.ai/user/ericsantos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Confidant to request sensitive credentials from users through a browser-based handoff flow, then save or apply those credentials without exposing them in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The secret handoff flow depends on unpinned external npm tooling. <br>
Mitigation: Install only after trusting the @aiconnect/confidant and localtunnel packages, and review package provenance before use. <br>
Risk: Public tunnel mode can expose the local credential handoff server beyond the local machine. <br>
Mitigation: Prefer local-only use, enable tunnels only when needed for remote users, and stop tunnel and server processes after the handoff. <br>
Risk: Secrets can be printed to stdout or written to under-scoped or arbitrary paths. <br>
Mitigation: Avoid stdout mode, use scoped and revocable secrets, and verify each destination path before saving credentials. <br>


## Reference(s): <br>
- [Confidant ClawHub release](https://clawhub.ai/ericsantos/confidant) <br>
- [Publisher profile: ericsantos](https://clawhub.ai/user/ericsantos) <br>
- [Confidant homepage](https://github.com/aiconnect-cloud/confidant) <br>
- [localtunnel documentation](https://theboroer.github.io/localtunnel-www/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce secure request URLs, saved credential files, environment variable setup guidance, diagnostics, and machine-readable status or error JSON.] <br>

## Skill Version(s): <br>
1.5.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
