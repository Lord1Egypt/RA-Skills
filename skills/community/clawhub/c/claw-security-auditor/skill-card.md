## Description: <br>
Autonomously scans installed OpenClaw skills for security risks, assigns risk scores and levels, and produces security reports with mitigation recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theelephantcoder](https://clawhub.ai/user/theelephantcoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to statically review installed skills for risky behavior, inspect findings, and decide whether to disable, sandbox, whitelist, or patch a skill before trusting it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad local permissions, including reading skill and filesystem content, writing local audit state, executing shell commands, and serving a localhost dashboard. <br>
Mitigation: Install only when a privileged local auditing tool is needed, review the source before use, and run scans in a constrained workspace or sandbox where practical. <br>
Risk: The local dashboard and persistent whitelist or trust controls can affect how future findings are reviewed. <br>
Mitigation: Avoid leaving the dashboard running while browsing untrusted sites, review the whitelist regularly, and treat trust changes as security-sensitive local state. <br>
Risk: The artifact includes intentionally risky sample skill scripts for test coverage. <br>
Mitigation: Use the sample scripts only as static test fixtures and do not run bundled sample skill scripts in normal use. <br>
Risk: The auto-fix workflow can generate patched skill instructions that alter permissions. <br>
Mitigation: Review any generated SKILL.patched.md before replacing or using a skill definition. <br>
Risk: Continuous monitoring can repeatedly read local skill files and run at login if enabled. <br>
Mitigation: Enable background monitoring only intentionally and review the monitor configuration before adding launchd or systemd startup entries. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/theelephantcoder/claw-security-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/theelephantcoder) <br>
- [README](artifact/README.md) <br>
- [Example audit output](artifact/data/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON/CSV exports, local dashboard views, patched SKILL.md suggestions, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static analysis only; reports include risk scores, risk levels, triggered rules, potential threats, malicious simulations, and recommended actions.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
