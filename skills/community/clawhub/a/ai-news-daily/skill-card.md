## Description: <br>
AI News Daily fetches recent global AI news from RSS sources, deduplicates articles, translates English content to Chinese, and generates a daily Markdown digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaa2531349](https://clawhub.ai/user/aaa2531349) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to automate a daily AI news workflow that collects public articles, summarizes selected items in Chinese, and prepares a Markdown update for OpenClaw or configured messaging targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public articles and stores article data locally. <br>
Mitigation: Review config/config.yaml before running, avoid private sources, and delete the data directory to remove stored articles and logs. <br>
Risk: Article text may be sent to translation providers. <br>
Mitigation: Review translation configuration and provider credentials before running, and only process content acceptable for external translation. <br>
Risk: Automatic daily pushing can post unwanted or unreviewed news summaries. <br>
Mitigation: Confirm OpenClaw and messaging target settings before enabling scheduled or automatic pushes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaa2531349/ai-news-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown daily news digest with source links and Chinese summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local article data, logs, and an OpenClaw message file when run.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
