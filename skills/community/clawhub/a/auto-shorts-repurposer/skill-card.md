## Description:

Repurpose long-form video or audio into short-form clip plans with timestamps, hooks, captions, and packaging notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

External creators, editors, and marketing teams use this skill to convert long videos, podcasts, streams, or transcripts into short-form clip plans with hooks, captions, titles, hashtags, thumbnail notes, and editor cut lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The source media may include rights, consent, privacy, or sensitive personal data issues.

Mitigation: Confirm rights and consent before reuse, avoid private or sensitive recordings, and keep source media within the user-provided context.

Risk: Using third-party transcription services may expose private or sensitive recordings.

Mitigation: Prefer local processing when possible, use user-managed API keys, avoid storing keys in files, and send only minimal transcription requests to trusted providers.

Risk: Outputs could be mistaken for approved publishing actions or account automation.

Mitigation: Treat all clip plans, captions, titles, hashtags, and thumbnail notes as drafts only, and do not request posting credentials or publish content.

## Reference(s):

- [Overview](references/overview.md)
- [Auth](references/auth.md)
- [Endpoints](references/endpoints.md)
- [Webhooks](references/webhooks.md)
- [UX](references/ux.md)
- [Troubleshooting](references/troubleshooting.md)
- [Safety](references/safety.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown clip cards with timestamps, draft copy, metadata suggestions, and editing notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only outputs; no publishing, uploading, account access, or credential handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
