## Description: <br>
Provides high-availability ACP bridge session management for OpenClaw by persisting ACP session mappings, injecting provider environment variables into spawned sessions, scheduling reviewed cron tasks, and coordinating advisory workspace locks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to improve ACP bridge reliability for autonomous agent sessions. It helps restore session mappings after restarts, pass provider environment into trusted spawned sessions, schedule reviewed main-session cron tasks, and coordinate shared workspace access with advisory locks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider credentials may be injected into spawned or scheduled sessions. <br>
Mitigation: Use least-privilege, revocable API keys, run dry-run validation before injection, and avoid injecting secrets into untrusted or fully autonomous sessions. <br>
Risk: Main-session cron scheduling can run reviewed host commands outside sandbox isolation. <br>
Mitigation: Enable scheduling only for bounded, reviewed, allowlisted commands, keep schedules easy to revoke, and prefer sandboxed sessions for untrusted or external code. <br>
Risk: Persisted ACP session mappings and stale sessions may survive restarts. <br>
Mitigation: Protect the local session store with appropriate file permissions, set short restoration windows, and periodically purge stale sessions. <br>
Risk: Workspace locks are advisory and depend on cooperating agents. <br>
Mitigation: Require agents to acquire and release locks around shared-resource writes, use try/finally release patterns, and monitor lock status for stale owners. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/romainsantoli-web/firm-acp-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples and inline shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential-handling, session recovery, scheduling, and workspace-locking guidance; no standalone generated artifact is promised by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
