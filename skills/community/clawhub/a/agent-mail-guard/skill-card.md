## Description:

Sanitize email and calendar content before it reaches an AI agent context by stripping common injection and exfiltration patterns, classifying sender trust, and returning structured JSON with suspicion flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[discodaddy](https://clawhub.ai/user/discodaddy)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill when an AI agent reads email, processes calendar events, or handles other untrusted message text. It prepares JSON that helps the agent decide whether to summarize, skip, or route suspicious content for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detected prompt-injection text can still be returned in model-facing fields.

Mitigation: Enforce the suspicious flag before adding body_clean, description_clean, titles, or previews to an AI context; exclude or isolate flagged content until a human reviews it.

Risk: Configured email and calendar accounts and local audit logs may expose mailbox or calendar metadata.

Mitigation: Review which gog accounts are configured and decide whether local audit logging is acceptable; use the raw output mode or separate log controls where audit records are not appropriate.

Risk: Pattern-based sanitization may miss semantic, novel, multi-message, image-based, or sender-spoofing attacks.

Mitigation: Use the sanitizer as defense in depth with sender authentication, agent policies that do not execute commands or call APIs from message content, and periodic pattern updates backed by tests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/discodaddy/skills/agent-mail-guard)
- [Agent Mail Guard project homepage](https://github.com/DiscoDaddy/agent-mail-guard)
- [gog CLI](https://github.com/liamg/gog)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON objects or arrays with command-line and integration guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes suspicion flags, sender or organizer trust tiers, summary level, sanitized text fields, and body truncation metadata.]

## Skill Version(s):

1.4.0 (source: SKILL.md frontmatter, pyproject.toml, CHANGELOG released 2026-02-27, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
