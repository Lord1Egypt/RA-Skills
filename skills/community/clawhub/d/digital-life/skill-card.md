## Description:

Skill Box provides five Digital Life reflection tools that analyze a user's digital traces to produce personal profiles, readable reports, and follow-up questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wildbyteai](https://clawhub.ai/user/wildbyteai)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke the skill to reflect on their social-media posts, private-chat exports, screenshots, and other digital-history inputs through tools for legacy audits, cringe archaeology, AI clone profiles, past-life narratives, and epitaphs. The skill guides collection, analysis, summary review, and local profile file generation after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose sensitive social-media history, private chats, screenshots, and derived personal traits to the agent.

Mitigation: Prefer redacted pasted excerpts, use narrow platform/date/content limits, and avoid third-party private conversations unless everyone involved consents.

Risk: Browser-based collection can inspect logged-in personal accounts more broadly than intended.

Mitigation: Use the minimum necessary account pages, confirm public URLs belong to the user before fetching, and keep all browser activity read-only.

Risk: Generated profiles and backups can retain sensitive local inferences after the session.

Mitigation: Inspect generated profile files after use and delete profiles or backups that should not be retained.

Risk: The unpinned npx install command can resolve to mutable installer behavior.

Mitigation: Install from a trusted release source and verify the selected package version before use.

## Reference(s):

- [Digital Life Skill Page](https://clawhub.ai/wildbyteai/skills/digital-life)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [AI Clone Method Reference](artifact/references/ai-clone.md)
- [Cringe Archaeology Method Reference](artifact/references/cringe-archaeology.md)
- [Epitaph Method Reference](artifact/references/epitaph.md)
- [Legacy Audit Method Reference](artifact/references/legacy-audit.md)
- [Past Life Method Reference](artifact/references/past-life.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown summaries and reports with JSON profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped local profile files after user confirmation; supports append, correction, rollback, list, and delete flows.]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
