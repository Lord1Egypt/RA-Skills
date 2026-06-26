## Description: <br>
Assist community moderation with summaries, spam detection suggestions, rule reminders, and draft replies for Discord or Telegram without automatic enforcement actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External community managers and moderators use this skill to summarize Discord or Telegram activity, surface possible spam or rule violations, and draft moderator responses for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Community message exports or platform access may expose private user data. <br>
Mitigation: Use read-only access, restrict exports to the necessary channels and time range, keep identifiers minimal, and avoid retaining full message bodies beyond the analysis window. <br>
Risk: Spam or rule-violation suggestions may be false positives or may reflect biased labeling. <br>
Mitigation: Require moderator review, include rule citations and confidence levels, and adjust keyword lists or thresholds when false positives occur. <br>
Risk: Draft replies could be mistaken for final enforcement decisions. <br>
Mitigation: Keep outputs in draft form and do not use the skill to mute, ban, delete messages, modify roles, or call moderation actions. <br>
Risk: Bot tokens or webhook inputs may be over-scoped or mishandled. <br>
Mitigation: Restrict bot tokens to read-only scopes, do not store tokens in files, validate webhook payloads, and rate limit processing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/codedao12/community-mod-pack) <br>
- [Publisher Profile](https://clawhub.ai/user/codedao12) <br>
- [Overview](references/overview.md) <br>
- [Auth](references/auth.md) <br>
- [Endpoints](references/endpoints.md) <br>
- [Webhooks](references/webhooks.md) <br>
- [UX](references/ux.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Safety](references/safety.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries, flagged-message lists, confidence notes, draft replies, and suggested follow-up actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are draft-only and require human moderator review before action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
