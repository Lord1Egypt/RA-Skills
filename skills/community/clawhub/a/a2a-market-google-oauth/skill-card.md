## Description: <br>
Handle Google OAuth login, account linking, and session bootstrap for A2A market users and operators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement Google OAuth authorization, identity linking, callback validation, and session bootstrap for A2A market buyer and merchant sign-in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated OAuth or session-management code could request overly broad scopes or mishandle refresh-token storage. <br>
Mitigation: Review generated code before deployment, restrict OAuth scopes, store only hashed refresh tokens, and rotate refresh tokens on use. <br>
Risk: Authentication, audit, or WebSocket events could expose raw tokens or sensitive account data. <br>
Mitigation: Redact token material and sensitive account fields from logs and event payloads before connecting production streams. <br>
Risk: Weak callback checks could allow incorrect account linking or invalid session creation. <br>
Mitigation: Validate state and nonce with server-side storage, and reject callbacks when issuer or audience does not match configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/a2a-market-google-oauth) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, shell commands] <br>
**Output Format:** [Markdown with code-oriented implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers OAuth endpoint contracts, identity mapping, token/session lifecycle, audit events, and validation expectations.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
