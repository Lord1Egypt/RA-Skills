## Description: <br>
AI News Pusher collects AI industry news from RSS and optional search APIs, scores items for product value, stores review queues, and can format or push selected news to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kern1x](https://clawhub.ai/user/kern1x) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and AI news curators use this skill to fetch recent AI news, score and categorize items, review borderline stories, and optionally push summaries to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook URLs, API keys, and gateway tokens can enable paid API use, message posting, or external scheduling if exposed. <br>
Mitigation: Provide only the environment variables needed for the intended mode, keep secrets out of source control and logs, and protect FEISHU_WEBHOOK_URL and OPENCLAW_GATEWAY_TOKEN. <br>
Risk: Automated scoring and scheduled pushes can publish low-quality, stale, or misclassified news without human review. <br>
Mitigation: Start with RSS-only or dry-run mode, review LLM-scored items before enabling scheduled pushes, and use the review queue for borderline items. <br>
Risk: Local JSON data can accumulate news history, feedback, filtered items, and push records. <br>
Mitigation: Periodically inspect or delete the local data directory and apply normal access controls for the runtime environment. <br>


## Reference(s): <br>
- [AI News Pusher on ClawHub](https://clawhub.ai/kern1x/ai-news-pusher) <br>
- [kern1x publisher profile](https://clawhub.ai/user/kern1x) <br>
- [Brave Search API endpoint](https://api.search.brave.com/res/v1/web/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, and optional JSON or text news output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local JSON data for review queues, feedback, filtered items, pushed items, and configuration when its scripts are run.] <br>

## Skill Version(s): <br>
2.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
