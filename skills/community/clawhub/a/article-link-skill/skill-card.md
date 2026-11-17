## Description:

Article Link Skill submits supported media article URLs to pick-read.vip, returns matched English article text when available, or queues extraction with quota-aware status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1787812757](https://clawhub.ai/user/1787812757)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit supported publisher article links, check quota and job status, and retrieve available English article content through the provided CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends an Import Token and article URLs to a remote API while TLS certificate and hostname verification are disabled.

Mitigation: Restore TLS verification before using real tokens, restrict API_BASE to the intended HTTPS host, and treat tokens used with this version on untrusted networks as exposed.

Risk: A configurable API_BASE can redirect token-bearing requests away from the intended service.

Mitigation: Use the default pick-read.vip endpoint or enforce an allowlist for the API host before deployment.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/1787812757/skills/article-link-skill)
- [Publisher Profile](https://clawhub.ai/user/1787812757)
- [pick-read.vip](https://pick-read.vip)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON response examples; runtime commands return JSON with article text, quota, media, job, or status data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Article content may be returned as HTML; most operations require an Import Token and are subject to daily quota limits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
