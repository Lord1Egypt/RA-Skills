## Description: <br>
Create, optimize, and scale Apple Search Ads campaigns with API automation, attribution integration, and bid strategy recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and growth teams use this skill to plan, automate, report on, and optimize Apple Search Ads campaigns for iOS apps. It supports campaign management, attribution integration, bid strategy, and performance analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to a real Apple Search Ads account, including campaign, keyword, bid, budget, and status changes. <br>
Mitigation: Require explicit human approval before any mutation to live campaigns or account configuration. <br>
Risk: The skill depends on Apple API credentials and private key material. <br>
Mitigation: Use least-privilege Apple credentials, keep private keys in a protected file or secret manager, and avoid storing secrets in shell startup files or logs. <br>
Risk: The skill can persist business context and reports under ~/apple-search-ads/. <br>
Mitigation: Review and clear local memory and generated reports as needed, and protect files that contain campaign or performance data. <br>
Risk: Attribution workflows may involve advertising and attribution data. <br>
Mitigation: Do not enable IDFA or log attribution payloads unless the app has the required consent, disclosure, and privacy controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/apple-search-ads) <br>
- [Skill source overview](artifact/SKILL.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [API reference](artifact/api-reference.md) <br>
- [iOS integration guide](artifact/ios-integration.md) <br>
- [Scripts and automation](artifact/scripts.md) <br>
- [Strategy playbook](artifact/strategy.md) <br>
- [Memory template](artifact/memory-template.md) <br>
- [Apple Search Ads API certificates settings](https://app.searchads.apple.com/cm/app/settings/apicertificates) <br>
- [Apple Ads API base endpoint](https://api.searchads.apple.com/api/v5) <br>
- [Apple AdServices attribution endpoint](https://api-adservices.apple.com/api/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, Swift, JavaScript, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include campaign recommendations, API request examples, local memory templates, and shell commands for Apple Search Ads workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
