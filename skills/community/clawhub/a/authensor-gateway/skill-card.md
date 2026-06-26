## Description: <br>
Fail-safe policy gate for OpenClaw marketplace skills that intercepts tool calls before execution and checks them against an Authensor policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AUTHENSOR](https://clawhub.ai/user/AUTHENSOR) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams using OpenClaw marketplace skills use Authensor Gateway to require policy checks, approvals, and denials before tool calls execute. It is intended for users who want human oversight, audit receipts, and fail-closed behavior when the control plane is unreachable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tool-call metadata is sent to an external Authensor control plane and receipts are stored by the service. <br>
Mitigation: Verify the control-plane URL, use a dedicated Authensor API key, and install only when external mediation and audit receipts are intended. <br>
Risk: The packaged skill provides prompt-level enforcement unless the separate hook is installed. <br>
Mitigation: Use the referenced PreToolUse hook when deterministic code-level enforcement is required. <br>
Risk: If the control plane is unavailable, the skill is designed to deny actions fail-closed. <br>
Mitigation: Confirm connectivity and operational readiness before relying on the gateway in active workflows. <br>


## Reference(s): <br>
- [Authensor for OpenClaw](https://github.com/AUTHENSOR/Authensor-for-OpenClaw) <br>
- [ClawHub Listing](https://clawhub.ai/AUTHENSOR/authensor-gateway) <br>
- [Publisher Profile](https://clawhub.ai/user/AUTHENSOR) <br>
- [ClawHavoc Research](https://snyk.io/blog/clawhavoc) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides instruction-only policy-gate behavior and approval guidance; it does not bundle executable code.] <br>

## Skill Version(s): <br>
0.7.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
