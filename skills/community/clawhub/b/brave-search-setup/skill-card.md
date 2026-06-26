## Description: <br>
Configure Brave Search API and troubleshoot network/proxy issues for web_search functionality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingliu1617-art](https://clawhub.ai/user/qingliu1617-art) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure Brave Search, diagnose web_search or web_fetch failures, and set up macOS proxy access when direct network access fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes persistent proxy configuration steps that can change local shell or macOS environment behavior. <br>
Mitigation: Prefer session-only proxy exports first, and use launchctl, shell profile edits, or sudo proxychains configuration only when the user intends and knows how to reverse those changes. <br>
Risk: Brave Search setup requires an API key that could be exposed if pasted into shared logs, shell history, or public files. <br>
Mitigation: Use placeholder values in examples, store the real key only in the intended OpenClaw configuration, and avoid sharing command output that contains the key. <br>


## Reference(s): <br>
- [Brave Search API Docs](https://api.search.brave.com/app/docs) <br>
- [Brave Search API](https://brave.com/search/api/) <br>
- [OpenClaw Config](https://docs.openclaw.ai/config) <br>
- [Clash Verge](https://github.com/clash-verge-rev/clash-verge-rev) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
