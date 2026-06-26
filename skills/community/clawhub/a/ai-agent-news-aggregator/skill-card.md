## Description: <br>
Collects AI Agent news from DuckDuckGo search and RSS sources, deduplicates and categorizes items, generates short summaries, and prepares daily or weekly Feishu briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiashuoji838-afk](https://clawhub.ai/user/jiashuoji838-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and teams tracking the AI Agent ecosystem use this skill to collect news, remove duplicates, classify items, summarize them, and prepare Feishu digests or scheduled briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Feishu channel ID could send posts to an unintended destination. <br>
Mitigation: Edit scripts/sources.json to remove or replace the channel ID before installation and confirm the recipient before enabling delivery. <br>
Risk: Scheduled execution can create recurring chat posts before recipients, cadence, and stop procedures are confirmed. <br>
Mitigation: Run the pipeline with --dry-run first, review the generated digest, and enable cron only after confirming who receives the messages and how to disable the schedule. <br>
Risk: The scripts describe live collection and delivery behavior that may be partial in standalone use. <br>
Mitigation: Treat live fetching and Feishu delivery as dependent on trusted OpenClaw tools or additional implementation, and validate end-to-end behavior before relying on the automation. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/jiashuoji838-afk/ai-agent-news-aggregator) <br>
- [Usage guide](scripts/README.md) <br>
- [Source configuration](scripts/sources.json) <br>
- [Anthropic Blog RSS](https://www.anthropic.com/news/rss.xml) <br>
- [OpenAI Blog RSS](https://openai.com/blog/rss/) <br>
- [Hugging Face Blog RSS](https://huggingface.co/blog/feed.xml) <br>
- [LangChain Blog RSS](https://blog.langchain.dev/rss/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown briefing text, JSON pipeline artifacts, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can be run in dry-run mode; Feishu posting depends on user-reviewed channel configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
