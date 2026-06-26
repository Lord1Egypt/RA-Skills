## Description: <br>
Identifies creative fatigue, budget leaks, and scaling opportunities by running the eonik creative audit engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techievena](https://clawhub.ai/user/techievena) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, growth teams, and agent users use this skill to run scoped Meta Ads audits that surface creative fatigue, budget leaks, and scaling opportunities. It requires an eonik API key and an explicit Meta account ID before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Meta ads audit data to eonik using EONIK_API_KEY. <br>
Mitigation: Install only if you trust eonik to process that data, use an appropriate scoped key when available, and set an explicit act_ Meta account ID before running. <br>
Risk: Audit summaries and generated report files can contain sensitive ad IDs, spend, performance metrics, and recommendations. <br>
Mitigation: Run the skill only from an approved private channel, keep redaction enabled unless approved, and protect or delete generated reports after use. <br>
Risk: Scheduled audits can repeatedly process ad-account data and distribute findings without fresh operator review. <br>
Mitigation: Enable scheduled audits only with documented owner or security approval, and periodically review or remove scheduled runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/techievena/eonik-creative-audit) <br>
- [eonik](https://eonik.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain-text audit summary with JSON report files and shell command/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EONIK_API_KEY and a config.json with meta.account_id. The pipeline writes dated JSON reports under output/ and redacts spend and ad details by default.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
