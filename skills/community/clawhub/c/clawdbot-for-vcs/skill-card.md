## Description:

Automates venture capital partner workflows for email triage, Affinity CRM updates, investment memo generation, calendar management, and daily briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lindsay-pettingill](https://clawhub.ai/user/lindsay-pettingill)

### License/Terms of Use:

MIT

## Use Case:

Venture capital investment partners, solo GPs, and emerging fund managers use this skill to prioritize deal-flow email, draft responses, keep Affinity CRM records current, prepare investment memos, and manage meeting logistics with user approval before external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs sensitive Gmail, Google Calendar, and Affinity CRM access.

Mitigation: Grant the narrowest available OAuth scopes and API permissions, review requested access before use, and keep user approval required for outbound or record-changing actions.

Risk: Credential exposure could occur if Affinity API keys or gog keyring passwords are copied into configuration files, shell startup files, logs, or notes.

Mitigation: Store credentials in an OS keychain or secret manager, keep them out of shared files and logs, and rotate any secret that may already have been exposed.

Risk: Installing an unpinned third-party CLI can expand account access without a reviewed version boundary.

Mitigation: Pin and review the gog CLI version before granting OAuth access, then upgrade deliberately after reviewing changes.

Risk: Auto-archive and auto-log workflows can hide email or write incorrect CRM records if rules are too broad.

Mitigation: Leave auto-archive and auto-log disabled until explicit rules, audit checks, and an easy rollback process are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lindsay-pettingill/skills/clawdbot-for-vcs)
- [README.md](README.md)
- [BOOTSTRAP.md](BOOTSTRAP.md)
- [SKILL.md](SKILL.md)
- [gog CLI](https://github.com/martynsmith/gog)
- [Affinity CRM](https://www.affinity.co)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, draft email text, CRM and calendar action plans, investment memo content, and daily briefing summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may propose Gmail, Google Calendar, and Affinity actions; outbound email and external record changes should remain approval-gated.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact skill.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
