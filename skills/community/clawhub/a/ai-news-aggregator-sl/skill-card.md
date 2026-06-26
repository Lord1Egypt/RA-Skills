## Description: <br>
Fetches AI and technology news, or a custom topic, from RSS feeds and optional search, social, and video sources, then writes an English editorial digest with the selected AI provider and can post it to Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ScottLL](https://clawhub.ai/user/ScottLL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect recent news or trending items on AI, technology, or a custom topic, generate a concise editorial digest, and deliver it to a Discord channel or preview it locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A digest may be posted to the configured Discord webhook when the user expected only a preview. <br>
Mitigation: Start with dry-run or a test Discord channel, verify the webhook target, and use test-discord mode before enabling routine posting. <br>
Risk: External news, social, or video source text can influence the generated summary. <br>
Mitigation: Review important posts before relying on them and avoid sensitive custom topics when using untrusted external sources. <br>
Risk: The skill uses multiple service credentials for AI providers, search, social, video, and Discord posting. <br>
Mitigation: Use limited-scope API keys, provide only the keys needed for the selected sources, and rotate credentials if a webhook or key is exposed. <br>


## Reference(s): <br>
- [AI News Aggregator on ClawHub](https://clawhub.ai/ScottLL/ai-news-aggregator-sl) <br>
- [ScottLL Publisher Profile](https://clawhub.ai/user/ScottLL) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown digest text, Discord webhook message, and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May post to Discord unless run with dry-run or test-discord mode; output depends on configured API keys and selected provider.] <br>

## Skill Version(s): <br>
1.2.8 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
