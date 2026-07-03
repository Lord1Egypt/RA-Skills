## Description: <br>
Provides OpenClaw power users with a documentation reference for hidden HTTP endpoints, debug settings, environment variables, and advanced configuration shortcuts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw power users use this skill as a reference for diagnostics, HTTP API routes, debug flags, and configuration examples. It is best suited for controlled troubleshooting and setup review because several documented options can weaken security if enabled broadly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill highlights OpenClaw settings that can weaken security or expose private data if enabled carelessly. <br>
Mitigation: Install only as a power-user reference and review each security-sensitive setting manually before use. <br>
Risk: Raw stream logging, live signed-in browser control, disabled auth checks, and disabled signature validation can expose sensitive data or reduce trust boundaries. <br>
Mitigation: Keep these settings disabled unless needed in a test or controlled environment, then remove them after troubleshooting. <br>
Risk: Elevated execution, Docker host binds, and HTTP tool allow-list changes can bypass normal sandbox protections. <br>
Mitigation: Avoid broad allow-list changes and host binds; scope any required exception to a controlled environment with explicit review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/evez-cheat-codes) <br>
- [Publisher profile](https://clawhub.ai/user/evezart) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reference text with tables, code blocks, shell commands, and JSON5 configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output covering OpenClaw diagnostics, HTTP APIs, browser automation, cron, memory search, telemetry, and sandbox controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
