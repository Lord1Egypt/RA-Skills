## Description: <br>
Daily Income Logger helps agents record income from multiple platforms, summarize daily earnings, analyze weekly or monthly trends, and export CSV/JSON reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mesiyoq965-sudo](https://clawhub.ai/user/mesiyoq965-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, freelancers, and operators use this skill to log daily platform income locally, review current totals, and generate weekly or monthly trend summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive income records may be stored as plaintext local JSON or exported as plaintext CSV/JSON. <br>
Mitigation: Use only on trusted devices, restrict file permissions, avoid shared or synced folders when inappropriate, or place the data under encrypted storage. <br>
Risk: The record command writes through a temporary tmp.json file in the current working directory. <br>
Mitigation: Run it from a trusted directory or adapt the temporary file path to a protected location under the logger data directory before use. <br>


## Reference(s): <br>
- [Daily Income Logger on ClawHub](https://clawhub.ai/mesiyoq965-sudo/daily-income-logger) <br>
- [Publisher profile](https://clawhub.ai/user/mesiyoq965-sudo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores income records locally as plaintext JSON and can export plaintext CSV/JSON reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
