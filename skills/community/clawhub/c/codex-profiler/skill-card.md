## Description: <br>
Maintained Codex operations skill: unified /codex_usage + /codex_auth path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeadlySilent](https://clawhub.ai/user/DeadlySilent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Codex profile usage, guide OAuth refresh or setup, and manage OpenClaw Codex profile ordering with a verify-after-apply workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interact with local OpenClaw Codex OAuth profiles and auth-store state. <br>
Mitigation: Use it only on trusted machines and prefer the documented gateway-native openclaw models auth commands for profile mutations. <br>
Risk: Auth workflows may leave token-bearing payloads or staged auth files under /tmp/openclaw. <br>
Mitigation: Check /tmp/openclaw after use and remove leftover sensitive temporary files once verification succeeds. <br>
Risk: Queued auth-store changes can restart or affect the local gateway. <br>
Mitigation: Run read-only preflight first, apply changes explicitly, and verify status and auth order after the apply step. <br>


## Reference(s): <br>
- [Codex Multi-Account Rotation Guide](references/multi-account-rotation.md) <br>
- [Codex Profiler on ClawHub](https://clawhub.ai/DeadlySilent/codex-profiler) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce concise usage summaries, auth workflow guidance, and gateway-native OpenClaw command sequences.] <br>

## Skill Version(s): <br>
1.0.27 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
