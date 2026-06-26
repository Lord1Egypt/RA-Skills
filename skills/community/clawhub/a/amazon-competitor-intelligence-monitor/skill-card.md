## Description: <br>
Deep competitor intelligence for Amazon sellers with Full Scan analysis and Quick Check monitoring that uses APIClaw data to compare competitors, ranking, pricing, reviews, trends, and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apiclaw](https://clawhub.ai/user/apiclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and commerce operators use this skill to run competitor scans, compare tracked ASINs, monitor price and ranking changes, and generate strategy guidance for marketplace positioning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A plaintext API key is bundled in monitor-data/config.json. <br>
Mitigation: Remove bundled monitor-data before use, rotate the exposed key, and provide APICLAW_API_KEY through the local environment. <br>
Risk: Preloaded baseline and history files may expose prior monitoring targets and influence future alerts. <br>
Mitigation: Start with empty monitor-data and create a fresh baseline for the user's own ASINs and thresholds. <br>
Risk: The reference material includes broader market-analysis wording that does not fully match the competitor-monitoring release. <br>
Mitigation: Review generated reports against the skill purpose and API provenance table before using recommendations for business decisions. <br>
Risk: Recurring Quick Check behavior can consume API credits and continue monitoring competitors. <br>
Mitigation: Require explicit approval for any scheduled monitoring setup and review API credit usage after each run. <br>


## Reference(s): <br>
- [APIClaw Skill Reference](artifact/references/reference.md) <br>
- [APIClaw API Documentation](https://api.apiclaw.io/api-docs) <br>
- [APIClaw API Key Setup](https://apiclaw.io/en/api-keys) <br>
- [ClawHub Skill Page](https://clawhub.ai/apiclaw/amazon-competitor-intelligence-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with tables, API usage and data provenance sections, alert summaries, and optional monitoring setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APICLAW_API_KEY and consumes APIClaw credits; reports include sampling disclaimers and confidence labels for conclusions.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
