## Description: <br>
Generate a weekly AI report with OpenClaw top skills, official announcements, industry news, and capped paper ratio in Markdown format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Matilda-Grifin](https://clawhub.ai/user/Matilda-Grifin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and operations teams use this skill to generate a weekly Chinese Markdown digest of AI announcements, industry news, papers, open-source activity, and OpenClaw leaderboard items from configured public sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public AI news sources and the OpenClaw leaderboard, so configured source URLs affect what content enters the report. <br>
Mitigation: Review sources.json before use and keep sources limited to trusted public feeds. <br>
Risk: When --use-llm is enabled, report inputs are sent to the configured LLM provider. <br>
Mitigation: Use a dedicated API key with limits and verify OPENAI_BASE_URL, Ark settings, and LLM_ALLOWED_HOSTS before running. <br>
Risk: Relaxing endpoint controls can route traffic to untrusted services or weaken transport security. <br>
Mitigation: Avoid --allow-insecure-ssl, --allow-custom-llm-endpoint, and webhook sending unless the target HTTPS endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Matilda-Grifin/ai-news-weekly-agent) <br>
- [Publisher profile](https://clawhub.ai/user/Matilda-Grifin) <br>
- [Skill definition](artifact/skill.md) <br>
- [Project README](artifact/README.md) <br>
- [Configured news sources](artifact/sources.json) <br>
- [Example weekly report](artifact/daily_docs/ai_weekly_20260323.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report written to daily_docs/ai_weekly_YYYYMMDD.md, with optional webhook notification text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default window is 168 hours; paper items are capped by --max-paper-ratio; source links and publication dates are preserved.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
