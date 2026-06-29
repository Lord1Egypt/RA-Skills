## Description: <br>
Scans Bilibili AI-related videos, clusters trending topics, generates a visual HTML daily report, and produces structured multi-engine intelligence investigation summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI researchers, industry intelligence analysts, and content creators use this skill to generate daily or targeted Bilibili AI trend reports with video clusters, interaction data, and cross-source investigation summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a real RedFox API key for normal API-backed use. <br>
Mitigation: Review the skill before installing, provide the key only through the documented environment variable, and avoid hard-coding or exposing the key in code, prompts, logs, or generated outputs. <br>
Risk: Optional subscription mode has review-worthy credential and local scheduling behavior. <br>
Mitigation: Avoid enabling --subscribe until plaintext key storage and crontab or LaunchAgent behavior are reviewed and fixed; prefer manual runs for sensitive environments. <br>
Risk: Bundled investigation guidance includes person-background and litigation-oriented use cases that may create privacy or authorization concerns. <br>
Mitigation: Use those investigation modes only when explicitly needed, appropriately authorized, and reviewed for applicable privacy and policy requirements. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/redfox-data/bili-ai-feed) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?souce=github) <br>
- [Engine strategy](references/engine-strategy.md) <br>
- [Investigation modes](references/investigation-modes.md) <br>
- [Investigation templates](references/investigation-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, HTML, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversation report plus generated HTML report file and shell commands for optional local execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY for API-backed queries; subscription mode can schedule local daily generation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
