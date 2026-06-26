## Description: <br>
Fetches the latest AI Insight Daily RSS items, formats summaries, and can push them to configured webhook channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DamomHd](https://clawhub.ai/user/DamomHd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve recent AI Insight Daily entries from an RSS feed, display concise Markdown summaries, and optionally deliver the summaries to notification webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically post retrieved content to webhook URLs configured in AI_DAILY_WEBHOOKS. <br>
Mitigation: Keep AI_DAILY_WEBHOOKS unset unless push delivery is intended, and configure only trusted webhook endpoints. <br>
Risk: Webhook tokens may be exposed in command output because push status messages include truncated webhook URLs. <br>
Mitigation: Avoid sharing command logs and prefer versions or wrappers that mask webhook URLs before logging. <br>
Risk: Unsafe input handling could run unintended code when user-controlled values are passed into the shell-generated Python snippet. <br>
Mitigation: Use trusted numeric count values, avoid untrusted RSS URL input, and prefer a fixed version that validates inputs safely. <br>
Risk: The script imports feedparser but the artifact does not declare the Python dependency. <br>
Mitigation: Install and pin feedparser in the agent environment before use, or run the skill in an environment with the dependency already declared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DamomHd/aiinsight-daily-new) <br>
- [AI Insight Daily RSS source](https://justlovemaki.github.io/CloudFlare-AI-Insight-Daily/rss.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown summary text printed to stdout, with optional JSON webhook payloads sent to configured endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts an optional count argument and reads AI_DAILY_WEBHOOKS, AI_DAILY_DEFAULT_COUNT, and AI_DAILY_RSS_URL from the environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
