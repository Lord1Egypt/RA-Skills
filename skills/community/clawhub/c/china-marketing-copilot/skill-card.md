## Description: <br>
A China consumer-electronics marketing copilot that helps agents produce launch strategy, message architecture, KOL/channel briefs, creative concepts, competitive analysis, comment-risk simulations, negative-signal warnings, and data-processing guidance for 3C categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killsnake01](https://clawhub.ai/user/killsnake01) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Marketing, social, channel, product, sales, and startup teams use this skill to plan and review China-market 3C product launches. Agents use its offline knowledge base, templates, risk rules, and evaluation samples to produce actionable marketing strategy, copy guidance, KOL briefs, competitive insights, and risk checks. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Imported comments, subtitles, scraped pages, or customer feedback may contain personal identifiers or content the user is not authorized to process. <br>
Mitigation: Confirm authorization before import, remove usernames and identifiers where possible, and avoid login-gated scraping. <br>
Risk: The skill can propose updates to knowledge-base files or SKILL.md that could introduce incorrect marketing guidance. <br>
Mitigation: Review proposed content changes before applying them and run the package validation scripts before release. <br>
Risk: The security summary notes routing cautions around implicit activation. <br>
Mitigation: Use the skill when the task clearly concerns China 3C marketing, risk review, launch planning, competitive analysis, or related data processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/killsnake01/china-marketing-copilot) <br>
- [README](README.md) <br>
- [Data index and freshness rules](docs/data-index.md) <br>
- [Machine-readable data source ledger](docs/data-sources.json) <br>
- [Strategy decision system](docs/templates/strategy-decision-system.md) <br>
- [Risk assessment template](docs/templates/risk-assessment.md) <br>
- [Negative early warning library](docs/ecosystem/negative-early-warning.md) <br>
- [Marketing task evaluation samples](docs/evals/marketing-task-samples.md) <br>
- [Negative signal evaluation samples](docs/evals/negative-signal-samples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with structured tables, checklists, labeled confidence notes, and occasional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve source labels, mark uncertain claims as pending verification, and end substantive responses with the skill's self-check line.] <br>

## Skill Version(s): <br>
1.3.7 (source: server release metadata and VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
