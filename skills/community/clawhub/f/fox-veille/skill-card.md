## Description: <br>
RSS feed aggregator, deduplication engine, LLM scoring, and output dispatcher for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinthqod](https://clawhub.ai/user/qinthqod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to fetch RSS/Atom articles, remove duplicate URLs and topics, optionally score articles with an OpenAI-compatible LLM, and send digests to configured destinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public RSS content and can pass article text into LLM scoring or digest generation. <br>
Mitigation: Treat feed text as untrusted content and keep the provided untrusted-content wrapping and prompt guidance in place. <br>
Risk: Enabled outputs can send digests externally or write files without interaction when scheduled. <br>
Mitigation: Keep outputs disabled until recipients, file paths, token scope, and companion skills are reviewed. <br>
Risk: LLM scoring requires an API key when enabled. <br>
Mitigation: Store API keys in the configured secret file, verify file permissions, and leave LLM scoring disabled unless needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qinthqod/fox-veille) <br>
- [Publisher profile](https://clawhub.ai/user/qinthqod) <br>
- [Skill homepage](https://github.com/Rwx-G/openclaw-skill-veille) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Cron prompt template](references/cron_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON and Markdown digests with CLI output and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local digest files and dispatch to Telegram, email, Nextcloud, or file outputs when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
