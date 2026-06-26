## Description: <br>
Sanitizes email and calendar content before it reaches an AI agent context window by stripping risky markup, URLs, hidden Unicode, encoded payloads, and known prompt-injection patterns while returning structured safety signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DiscoDaddy](https://clawhub.ai/user/DiscoDaddy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill when an AI agent reads email, calendar events, or other untrusted text and needs sanitized JSON plus safety flags before adding content to model context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper scripts can read configured Gmail and Calendar accounts through gog. <br>
Mitigation: Review account configuration and environment variables before running the wrappers, and grant only the mailbox or calendar access needed for the agent workflow. <br>
Risk: Local audit summaries may record metadata about checks. <br>
Mitigation: Use raw output when audit summaries are not desired and review local audit-log files according to the user's retention requirements. <br>
Risk: Sanitized output may still contain private message or event details. <br>
Mitigation: Treat sanitized JSON as sensitive data and limit downstream sharing, logging, and model-context inclusion to the minimum needed. <br>
Risk: Pattern-based sanitization may miss semantic or novel injection attempts. <br>
Mitigation: Keep agent policies that avoid executing commands, visiting URLs, or calling APIs based solely on email or calendar content, especially when output is flagged suspicious or sender trust is unknown. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DiscoDaddy/agent-mail-guard) <br>
- [Publisher profile](https://clawhub.ai/user/DiscoDaddy) <br>
- [Project homepage](https://github.com/DiscoDaddy/agent-mail-guard) <br>
- [gog CLI](https://github.com/liamg/gog) <br>
- [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) <br>
- [Morris II self-replicating AI worm](https://sites.google.com/view/compromptmized) <br>
- [Anthropic computer use safety analysis](https://www.anthropic.com/research/claude-computer-use-safety) <br>
- [Indirect prompt injection paper](https://arxiv.org/abs/2302.12173) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON records or arrays with sanitized email and calendar fields, sender trust tiers, suspicion flags, and truncation metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Email bodies are capped at 2000 characters, unknown senders receive reduced detail, and wrapper scripts can write local audit summaries unless raw output is requested.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter, pyproject.toml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
