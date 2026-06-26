## Description: <br>
Monitors brand visibility across AI search and chat platforms, generates a 0-100 GEM visibility score, analyzes why a brand is not recommended, and can send reports to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yk-global-01](https://clawhub.ai/user/yk-global-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, brand operators, and developers use this skill to check how visible a brand or competitor is in supported AI answer platforms and to generate a report with scores, snippets, and optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brand, competitor, campaign, or client terms may be sent to external services during monitoring. <br>
Mitigation: Review terms before running the skill and avoid sensitive test data unless external disclosure is acceptable. <br>
Risk: Reports may be delivered to Feishu when push delivery is enabled. <br>
Mitigation: Use --no-push unless Feishu delivery is intentional and the webhook destination is trusted. <br>
Risk: The bundled Tavily API service has weak placeholder authentication if run as a public service. <br>
Mitigation: Do not expose api/geo_api.py publicly until placeholder keys are replaced, real authentication and rate limits are added, and TAVILY_API_KEY is protected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yk-global-01/brand-visibility-monitor) <br>
- [YK Global](https://yk-global.com) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with console status text and optional Feishu card delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes report files under /tmp; may call external search, verification, AI analysis, and Feishu webhook endpoints when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
