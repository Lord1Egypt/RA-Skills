## Description: <br>
Query CDE China drug review public data for breakthrough therapy announcements, priority review announcements, included lists by company or drug, in-review registration lookups by company or drug, and acceptance-number review status lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[changye](https://clawhub.ai/user/changye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query current public China Center for Drug Evaluation drug-review listings by announcement type, company, drug name, year range, or acceptance number. It is intended for live lookup and structured summarization, not static medical or regulatory advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs Selenium-driven browser automation against the public CDE website, and evidence.security flags undisclosed browser fingerprint spoofing. <br>
Mitigation: Review the automation behavior before installation, run it only in an environment where local Chrome or Chromium automation is acceptable, keep query volume low, and prefer an official CDE data or API route when available. <br>
Risk: Live CDE page structure, network payloads, or site access expectations can change and cause incomplete or unreliable results. <br>
Mitigation: Treat query output as current public-page evidence, check failures and empty results against the live CDE site, and avoid inventing results when parsing or Selenium execution fails. <br>


## Reference(s): <br>
- [CDE homepage](https://www.cde.org.cn) <br>
- [CDE information disclosure entry](https://www.cde.org.cn/main/xxgk/listpage/9f9c74c73e0f8f56a8bfbc646055026d) <br>
- [CDE review task disclosure](https://www.cde.org.cn/main/xxgk/listpage/369ac7cfeb67c6000c33f85e6f374044) <br>
- [Setup](references/setup.md) <br>
- [Queries](references/queries.md) <br>
- [Development guide](references/development-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands and JSON CLI results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the live CDE website, local Python and Chrome or Chromium availability, strict company or drug name matching, and the documented 2016 through 2026 year range for in-review and acceptance-number flows.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
