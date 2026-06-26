## Description: <br>
CompanyInformation helps agents query FEEDAX company-news and public-opinion data for listed companies, including sentiment, heat score, industry classification, and related company fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longgggggg](https://clawhub.ai/user/longgggggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to monitor company news and public opinion, filter results by company, keyword, sentiment, recency, or heat, and export results for investment research or risk review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles FEEDAX API keys and the security summary flags unsafe key-handling patterns. <br>
Mitigation: Provide the API key through an environment variable or protected local config, and do not paste it into chat or persistent agent memory. <br>
Risk: The current script contacts a plaintext HTTP endpoint. <br>
Mitigation: Use the skill only when that transport risk is acceptable for the query and operating environment. <br>
Risk: The script writes CSV and Markdown result files by default, which may persist sensitive investigation details. <br>
Mitigation: Use --no-output for sensitive investigations or direct output to an approved local directory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/longgggggg/companyinformation) <br>
- [FEEDAX](https://www.feedax.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown summaries, terminal text, CSV files, and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FEEDAX API key; writes CSV and Markdown result files by default unless --no-output is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
