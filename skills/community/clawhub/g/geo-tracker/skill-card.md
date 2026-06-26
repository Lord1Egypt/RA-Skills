## Description: <br>
Track and optimize brand visibility across AI search engines by monitoring brand mentions, comparing competitors, running GEO audits, and generating optimization reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[X-RayLuan](https://clawhub.ai/user/X-RayLuan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Marketing, growth, and content teams use this skill to measure how AI engines mention a brand, compare visibility against competitors, and identify content changes that may improve generative search visibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brand-monitoring prompts, brand names, competitor names, and generated reports may include confidential strategy, personal data, regulated data, or other sensitive business information that could be sent to external AI providers. <br>
Mitigation: Avoid secrets, personal data, regulated data, and confidential strategy in prompts; review provider terms for selected engines before use. <br>
Risk: Scheduled or batch audits can repeatedly call external AI provider APIs under the user's API keys and may save potentially sensitive reports locally. <br>
Mitigation: Set API spending limits, review scheduled runs, and save reports only in locations appropriate for the sensitivity of the audit data. <br>


## Reference(s): <br>
- [GEO Optimization Guide](references/geo-optimization.md) <br>
- [GEO Prompts Library](references/prompts.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal summaries, Markdown audit reports, and optional JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on user-selected brand names, competitor names, prompts, engines, API keys, and optional scheduled runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
