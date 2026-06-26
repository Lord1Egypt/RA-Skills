## Description: <br>
An OpenClaw skill for tracking keyword trends and generating structured reports using Tavily search, local report storage, and optional webhook delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesong-hue](https://clawhub.ai/user/yesong-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content strategists, market researchers, and automation users use this skill to monitor configured keywords, collect search results, and generate recurring markdown trend reports that can be saved locally or sent to a webhook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Keywords and generated reports may be sent to Tavily and, when configured, to a webhook provider. <br>
Mitigation: Use non-sensitive keywords where possible and send reports only to trusted HTTPS webhook endpoints. <br>
Risk: The skill requires a Tavily API key, which is a sensitive credential. <br>
Mitigation: Use a dedicated Tavily key stored in environment variables and rotate or revoke it if exposed. <br>
Risk: The artifact describes running node index.js, but the provided artifact does not include that runtime implementation. <br>
Mitigation: Verify the installed files and runtime entry point before executing the skill. <br>


## Reference(s): <br>
- [Content Keyword Tracker on ClawHub](https://clawhub.ai/yesong-hue/content-keyword-tracker) <br>
- [Tavily API](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with keyword sections, result tables, summary statistics, and trend indicators.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are described as timestamped local files with optional webhook delivery when configured.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
