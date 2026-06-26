## Description: <br>
Daily Producer creates personalized daily news reports by collecting multi-platform sources from a user profile, filtering and scoring items, generating structured report JSON, and rendering HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ailab2026](https://clawhub.ai/user/ailab2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a reader profile, collect recent items from opencli and web sources, generate a structured daily report, validate it, render an HTML page, and optionally send a Feishu card notification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact many external platforms and reuse browser or login state through opencli. <br>
Mitigation: Review configured sources before running, limit enabled platforms to those needed, and use least-privilege or separate browser sessions where possible. <br>
Risk: The skill may read Feishu app credentials and send Feishu messages. <br>
Mitigation: Use scoped Feishu credentials, confirm chat destinations before enabling notifications, and require review before notification configuration changes. <br>
Risk: The bundled feedback server is described as reachable on the network by default. <br>
Mitigation: Bind the server to localhost or add authentication before exposing feedback endpoints. <br>
Risk: The security summary reports embedded proxy credentials and feedback-based behavioral tracking. <br>
Mitigation: Remove embedded proxy credentials before use and disable or minimize feedback telemetry unless the user explicitly opts in. <br>
Risk: Graphify or third-party AI export settings may move report content into external or local downstream systems. <br>
Mitigation: Review export settings and data destinations before enabling Graphify or third-party AI integrations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ailab2026/daily-producer) <br>
- [Publisher profile](https://clawhub.ai/user/ailab2026) <br>
- [Daily Producer skill definition](SKILL.md) <br>
- [Daily production pipeline overview](reference/pipeline/00_overview.md) <br>
- [AI report JSON generation rules](reference/pipeline/06_generate_json.md) <br>
- [Profile configuration template](reference/profile_template.yaml) <br>
- [opencli output formats](reference/opencli_output_formats.md) <br>
- [Daily payload example](reference/daily_payload_example.json) <br>
- [Feedback schema](reference/feedback_schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, HTML, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands; generated report artifacts are JSON and HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces raw collection files, validated daily report JSON, rendered HTML, optional Feishu card notifications, and optional feedback data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
