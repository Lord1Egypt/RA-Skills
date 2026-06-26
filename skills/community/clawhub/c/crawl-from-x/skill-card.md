## Description: <br>
Crawl From X manages a list of X/Twitter accounts, crawls recent posts through an OpenClaw browser session, and exports the results as Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyingtimes](https://clawhub.ai/user/flyingtimes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to track selected X/Twitter accounts, collect current posts and media, and turn them into local Markdown records for review or downstream summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an already logged-in X/Twitter browser session to read timelines and collect post identifiers. <br>
Mitigation: Run it only with the intended browser profile, account, and authorization context, and confirm use is consistent with applicable X/Twitter terms and organizational policy. <br>
Risk: Crawled social posts can contain untrusted text, including prompt-injection attempts or misleading claims. <br>
Mitigation: Treat generated Markdown as untrusted input; review, quote, or sanitize it before feeding it to another AI agent or workflow. <br>
Risk: The skill saves crawled Markdown and downloaded media files locally. <br>
Mitigation: Store results in an appropriate local workspace, avoid publishing private captures unintentionally, and scan or review downloaded media before reuse. <br>


## Reference(s): <br>
- [Crawl From X on ClawHub](https://clawhub.ai/flyingtimes/crawl-from-x) <br>
- [OpenClaw Browser Relay Documentation](https://docs.openclaw.ai/guide/browser-relay) <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files, plain-text URL lists, and locally saved media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local users.txt account list and writes timestamped results under results/.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
