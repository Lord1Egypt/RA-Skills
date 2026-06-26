## Description: <br>
Generates a daily AI news brief by collecting multiple AI and product feeds, using an LLM to select the most valuable items, and delivering a concise Telegram-ready briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[min870809](https://clawhub.ai/user/min870809) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate a personalized daily AI news briefing, reduce low-signal feed noise, and highlight competitor, market, and monetization opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires API and Telegram credentials and can expose them if they are hard-coded or logged. <br>
Mitigation: Store API_HUB_KEY, Telegram credentials, and optional tool gateway tokens in environment variables or a secret store, and avoid committing configured copies of the script. <br>
Risk: Briefing content is sent through external RSS/tool services, an LLM API, and Telegram. <br>
Mitigation: Use only public or non-sensitive feeds unless those external processing and delivery paths are approved for the data. <br>
Risk: A misconfigured API_HUB_BASE_URL could route requests to an untrusted service. <br>
Mitigation: Confirm API_HUB_BASE_URL uses a trusted HTTPS provider before running scheduled jobs. <br>
Risk: Scheduled automation could repeatedly send incorrect, noisy, or unwanted Telegram briefings. <br>
Mitigation: Run the skill manually once and review the selected items before enabling the daily schedule. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/min870809/ai-morning-brief) <br>
- [Hugging Face Blog Feed](https://huggingface.co/blog/feed.xml) <br>
- [人人都是产品经理 Feed](https://www.woshipm.com/feed) <br>
- [OpenRouter Apps](https://openrouter.ai/apps) <br>
- [ClawdChat Tool Gateway](https://clawdchat.cn/api/v1/tools/call) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown-formatted Telegram message with setup commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces up to 10 selected briefing items and may truncate long Telegram messages near the platform message limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
