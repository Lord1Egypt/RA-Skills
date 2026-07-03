## Description: <br>
A-share intelligence investigation skill that gathers and cross-checks company, competitor, event, background, and claim information and returns structured reports with credibility labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors, product and market teams, journalists, business development teams, and general users use this skill to research A-share companies, compare competitors, track public sentiment, perform background checks, and verify claims. Reports are intended to support decision-making with source-aware findings and credibility annotations. <br>

### Deployment Geography for Use: <br>
Global (content focus: China A-share market and Chinese-language sources) <br>

## Known Risks and Mitigations: <br>
Risk: Generated investigation reports, including business or personal-background content, may be sent to RedFox. <br>
Mitigation: Use a revocable REDFOX_API_KEY and manually review, redact, or block report contents before allowing any external save. <br>
Risk: Person-background screening can create privacy, consent, or sensitive personal-data concerns. <br>
Mitigation: Avoid private-person profiling and sensitive personal data; limit use to lawful, consented, and proportionate business contexts. <br>
Risk: Investigation findings may include incorrect, single-source, or misleading information. <br>
Mitigation: Confirm key claims against authoritative sources and treat credibility labels as review aids rather than final proof. <br>


## Reference(s): <br>
- [README.en.md](README.en.md) <br>
- [Core Workflow](references/core_workflow.md) <br>
- [Investigation Modes](references/investigation-modes.md) <br>
- [Engine Strategy](references/engine-strategy.md) <br>
- [Investigation Templates](references/investigation-templates.md) <br>
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?souce=github) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with tables, source notes, credibility labels, and inline shell commands for RedFox report saving] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY for saving generated investigation reports to RedFox.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
