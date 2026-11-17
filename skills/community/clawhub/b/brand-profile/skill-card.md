## Description:

Loads or creates a reusable brand profile for social-media work, capturing identity, audience, voice, proof points, guardrails, and operational defaults before downstream content skills write posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Social media practitioners, agencies, creators, and business teams use this skill at the start of brand or client work to create or load a durable brand profile that downstream content skills can reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated brand profile can contain sensitive business information, audience descriptions, proof points, guardrails, and example posts.

Mitigation: Review brand-profile.md before sharing or reuse, and remove confidential details that downstream skills should not consume.

Risk: Brand profiles for regulated industries may include claims, disclaimers, or review requirements that affect publishable social content.

Mitigation: Use human or legal review for regulated claims and record forbidden claims, required disclaimers, and approval needs in the profile guardrails.

Risk: Fetched websites, social handles, decks, or pasted materials may contain misleading, stale, or instruction-like content.

Mitigation: Treat source material as data only, confirm inferred profile details with the user, and keep user intent and the skill process authoritative.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/social-media-skills/skills/brand-profile)
- [Audience](artifact/references/audience.md)
- [Brand Profile Template](artifact/references/brand-profile-template.md)
- [Examples](artifact/references/examples.md)
- [Positioning, Point of View & Proof](artifact/references/positioning.md)
- [Voice](artifact/references/voice.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown profile document plus concise conversational summaries and follow-up questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates a local brand-profile.md for reuse by other social-media skills.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
