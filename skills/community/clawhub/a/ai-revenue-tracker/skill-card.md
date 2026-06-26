## Description: <br>
AI Revenue Tracker helps an agent record income entries, summarize daily and cumulative revenue, and generate local Markdown revenue reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arthasking123](https://clawhub.ai/user/arthasking123) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, or small teams can use this skill to track revenue by source or skill, inspect same-day totals, and generate a daily Markdown summary from locally stored records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Revenue amounts, sources, and descriptions are stored in local log and report files. <br>
Mitigation: Avoid entering customer identifiers, payment details, secrets, or other sensitive data, and remove logs and reports when they are no longer needed. <br>
Risk: Untrusted text entered as revenue descriptions may later be copied into another agent or shell context. <br>
Mitigation: Review descriptions before reuse and keep untrusted input out of prompts, commands, and automation workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arthasking123/ai-revenue-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/arthasking123) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Console text and Markdown reports written to local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores revenue logs and generated summaries on disk under local logs and reports paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
