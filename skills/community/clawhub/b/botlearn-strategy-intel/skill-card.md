## Description: <br>
Scrapes public company information via Apify and produces a structured strategic analysis for founders, operators, investors, and strategy teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivianezhou-byte](https://clawhub.ai/user/vivianezhou-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, operators, investors, and strategy teams use this skill to research a company and receive a concise strategic readout covering market direction, product and customer fit, founders, economics, and the key strategic implication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented execution flow passes a user-supplied company name into an unquoted shell command. <br>
Mitigation: Review or patch the execution instruction before installation so company names are safely quoted, validated, or passed as argv. <br>
Risk: The workflow sends target names, queries, and scraped public data to third-party services. <br>
Mitigation: Use limited-scope Apify and model-provider API keys, and avoid submitting confidential, regulated, or internal target names. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/vivianezhou-byte/botlearn-strategy-intel) <br>
- [Publisher profile](https://clawhub.ai/user/vivianezhou-byte) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Partner's Playbook](partner_playbook.md) <br>
- [Apify](https://apify.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Shell commands, Guidance] <br>
**Output Format:** [Markdown strategic analysis with section headings and a single-sentence strategic implication] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a company name and optional quick or deep depth setting; output depends on public data returned by Apify and the configured model provider.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
