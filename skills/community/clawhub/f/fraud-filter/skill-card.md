## Description: <br>
Community trust scores for AI agent payment endpoints - checks endpoint reputation before payment and queues anonymous failure reports locally (network reporting is opt-in). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattpolly](https://clawhub.ai/user/mattpolly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Fraud Filter to assess AI agent payment endpoints before payment, warn or block low-trust endpoints, and queue anonymous local failure reports after poor transaction outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can monitor and sometimes block payment-like tool calls. <br>
Mitigation: Review the on_block and on_caution settings before use, and require explicit user confirmation before temporarily overriding a block. <br>
Risk: The security scan reports broad local and remote controls that need review before installation. <br>
Mitigation: Install only if those controls are acceptable for the environment; keep the dashboard stopped when it is not needed. <br>
Risk: Network participation can submit queued failure reports to the reporting service. <br>
Mitigation: Review queued reports before enabling participate_in_network or triggering a flush. <br>
Risk: Custom trust or report URLs could change the source of payment-risk decisions or report submission. <br>
Mitigation: Avoid custom trust/report URLs unless they are explicitly trusted, and disable sync_hotlist for offline environments. <br>


## Reference(s): <br>
- [Fraud Filter ClawHub Release](https://clawhub.ai/mattpolly/fraud-filter) <br>
- [Fraud Filter Homepage](https://fraud-filter.com) <br>
- [Technical Architecture](TECHNICAL.md) <br>
- [Signal Format & Score Calculation](references/signal-format.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command output, and local JSON/JSONL data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May warn, allow, or block payment-like tool calls based on configured trust policy; reporting stays local unless network participation and flushing are explicitly enabled.] <br>

## Skill Version(s): <br>
0.4.0 (source: SKILL.md frontmatter, openclaw.plugin.json, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
