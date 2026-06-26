## Description: <br>
Validates OpenClaw agent configuration consistency, detects stale references, generates diagnostic reports, and supports guarded automatic repairs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StarAI-2026](https://clawhub.ai/user/StarAI-2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to check OpenClaw multi-agent configurations after adding, removing, or changing agents. It reports configuration drift, stale documentation references, and safe repair suggestions before optional fixes are applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fix mode can modify local OpenClaw configuration files. <br>
Mitigation: Start in read-only or dry-run mode, review the report, confirm backups, and use fix mode only in a trusted workspace. <br>
Risk: Diagnostic reports may include local configuration details, agent names, or file paths. <br>
Mitigation: Review generated reports before sharing them outside the workspace. <br>
Risk: The test wrapper can be unsafe if run with untrusted environment variables or paths. <br>
Mitigation: Avoid running test-skill.js with untrusted inputs; use the validator directly in the intended OpenClaw workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/StarAI-2026/agent-config-validator) <br>
- [Publisher profile](https://clawhub.ai/user/StarAI-2026) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text and Markdown diagnostic reports, with optional configuration edits when fix mode is enabled] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default behavior is read-only; fix mode can modify OpenClaw configuration files after checks and backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
