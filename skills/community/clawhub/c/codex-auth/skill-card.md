## Description: <br>
DEPRECATED shim skill for /codex_auth. Use codex-profiler instead; codex-auth is no longer the maintained path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeadlySilent](https://clawhub.ai/user/DeadlySilent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this deprecated helper to start and finish OpenAI Codex OAuth profile authentication for OpenClaw, including profile selection, callback handling, and local auth profile updates. The evidence recommends the maintained codex-profiler path for ongoing /codex_auth and /codex_usage operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deprecated standalone flow may be less appropriate than the maintained codex-profiler path for ongoing Codex auth and usage operations. <br>
Mitigation: Prefer codex-profiler unless the deprecated codex-auth behavior is specifically required. <br>
Risk: Queued apply mode writes OAuth tokens to predictable /tmp paths and restarts the local gateway in the background. <br>
Mitigation: Avoid shared machines, avoid --queue-apply unless the restart and temporary token exposure are acceptable, and review status and backup paths after use. <br>
Risk: Callback URLs and OAuth tokens are sensitive and can expose account access if pasted into the wrong place or echoed in full. <br>
Mitigation: Paste callback URLs only into the intended finish command and never display full callback query parameters, access tokens, or refresh tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DeadlySilent/codex-auth) <br>
- [SECURITY.md](artifact/SECURITY.md) <br>
- [RISK.md](artifact/RISK.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses with command guidance and local configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OAuth callback URLs and token values are sensitive and should not be echoed in full.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
