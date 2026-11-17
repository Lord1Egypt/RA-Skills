## Description:

Assist community moderation with summaries, spam detection suggestions, and draft replies for Discord or Telegram. Use when a user wants moderation help, rule reminders, or daily summaries without automatic enforcement actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

External community moderators use this skill to summarize Discord or Telegram activity, surface possible spam or rule violations, and draft rule reminders or moderator replies. It supports human-reviewed moderation workflows and does not perform enforcement actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Community message analysis can expose personal data or exceed a community's privacy rules if moderators provide broad logs or credentials.

Mitigation: Use only approved channels, time windows, rules, and read-only access; minimize identifiers and avoid storing tokens or full message bodies beyond the analysis window.

Risk: Spam or rule-violation flags may be incorrect, biased, or missing context.

Mitigation: Keep outputs as drafts with rule citations and confidence levels, and require human moderator review before any action.

Risk: Suggested actions could be mistaken for automated enforcement.

Mitigation: Do not call moderation endpoints or modify roles, messages, mutes, bans, or kicks; provide only summaries, flags, and draft responses.

## Reference(s):

- [Overview](artifact/references/overview.md)
- [Auth](artifact/references/auth.md)
- [Endpoints](artifact/references/endpoints.md)
- [Safety](artifact/references/safety.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [UX](artifact/references/ux.md)
- [Webhooks](artifact/references/webhooks.md)
- [ClawHub skill page](https://clawhub.ai/codedao12/skills/community-mod-pack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries, flagged-message lists, confidence labels, and draft replies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs remain advisory drafts for human moderators and should cite the triggered rule where applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
