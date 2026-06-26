## Description: <br>
Extracts consumer insights from pre-analyzed Amazon reviews, including pain points, buying factors, user profiles, usage patterns, competitor sentiment, and listing copy suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apiclaw](https://clawhub.ai/user/apiclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, sellers, product researchers, and developers use this skill to analyze Amazon review sentiment for individual ASINs, competitor sets, or product categories. It helps identify customer complaints, purchase drivers, differentiation opportunities, and review-backed listing improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an APIClaw API key and sends Amazon ASINs, keywords, category paths, competitor lists, and business research context to APIClaw. <br>
Mitigation: Use a limited or low-risk API key when available, monitor credit usage, and avoid submitting confidential business context unless APIClaw is approved for that use. <br>
Risk: Market and review conclusions may be incomplete or time-sensitive because the skill relies on APIClaw sampling, lower-bound estimates, realtime data, and endpoint availability. <br>
Mitigation: Keep the required disclaimer, data provenance table, API usage table, and confidence labels in user-facing reports, and validate important decisions with additional sources. <br>
Risk: The bundled reference file contains market-entry wording that does not exactly match the review-intelligence skill name. <br>
Mitigation: Treat the wording as a documentation inconsistency and keep usage focused on the disclosed Amazon review, product, competitor, pricing, and market-data endpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/apiclaw/amazon-review-intelligence-extractor) <br>
- [APIClaw API Documentation](https://api.apiclaw.io/api-docs) <br>
- [APIClaw](https://apiclaw.io) <br>
- [APIClaw API Key Setup](https://apiclaw.io/en/api-keys) <br>
- [API Field Reference](references/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables, confidence labels, data provenance, API usage, and optional inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output language matches the user's input language; reports omit empty dimensions and should only include insights returned by APIClaw.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
