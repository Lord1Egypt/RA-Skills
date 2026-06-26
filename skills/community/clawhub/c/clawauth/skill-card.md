## Description: <br>
Let agents request OAuth access from end users via short links, continue working asynchronously, and later claim reusable third-party API tokens from local keychain storage instead of a centralized SaaS token vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs user-delegated OAuth access to supported third-party APIs without blocking the session. It guides the agent through starting an OAuth handoff, polling status, claiming completed sessions once, and handing token use to operator-controlled API tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may gain access to reusable third-party account tokens after a user completes OAuth. <br>
Mitigation: Install only in trusted runtimes, grant minimal OAuth scopes, use a pinned and reviewed clawauth CLI, and keep downstream API access under operator-controlled secret handling. <br>
Risk: Sensitive token payloads may appear in command output during claim or token inspection flows. <br>
Mitigation: Prevent command output from being pasted into chat or captured in logs, traces, or telemetry; do not export tokens into shell environment variables. <br>
Risk: Security evidence marks the release suspicious because token handling guidance is mixed and requires review. <br>
Mitigation: Review the skill and CLI behavior before deployment, confirm token revocation/removal procedures, and deploy only when OAuth token exposure is an intended capability. <br>


## Reference(s): <br>
- [Clawauth Commands (Agent Reference)](references/commands.md) <br>
- [Clawauth hosted service](https://auth.clawauth.app) <br>
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [OpenClaw macOS Skills documentation](https://docs.openclaw.ai/platforms/mac/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes JSON parsing, asynchronous polling, local keychain storage, and avoiding token disclosure in chat, logs, traces, telemetry, or shell environments.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
