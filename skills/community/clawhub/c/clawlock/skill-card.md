## Description: <br>
ClawLock helps agents run security scans, skill audits, configuration hardening, drift checks, discovery, and optional red-team tests for Claw-compatible environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[g1at](https://clawhub.ai/user/g1at) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to inspect Claw-compatible agent environments, audit skills before installation, review configuration risks, and generate hardening guidance. Optional online checks and red-team tests should be run only for authorized targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask the agent to install or update external code and replace its local skill file. <br>
Mitigation: Review and trust the PyPI package, GitHub repository, and skill-file diff before allowing installs, updates, or file replacement. <br>
Risk: Security scans and red-team tests can touch sensitive environments or unauthorized endpoints if aimed incorrectly. <br>
Mitigation: Run offline or report-only scans first, and run red-team tests only against targets the user owns or is authorized to test. <br>
Risk: Optional online checks may send limited scan-related data to external services when enabled. <br>
Mitigation: Prefer local-first options when privacy matters, and clearly report which online capabilities ran, were skipped, or were unavailable. <br>


## Reference(s): <br>
- [ClawLock repository](https://github.com/g1at/ClawLock) <br>
- [ClawLock ClawHub listing](https://clawhub.ai/g1at/clawlock) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON or HTML reports from the underlying tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference optional online checks, local scan results, report files, and skipped checks depending on user authorization and environment capabilities.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
