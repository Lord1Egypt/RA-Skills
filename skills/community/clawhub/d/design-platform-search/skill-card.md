## Description:

Run public design search flows on Dribbble, Pinterest, and Behance without login, and extract normalized result fields such as title, search-page cover image, author, source URL, and publish time when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyyyy0430](https://clawhub.ai/user/joeyyyy0430)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect public design inspiration from Dribbble, Pinterest, and Behance with a lightweight, search-page-first workflow. It is useful for trend observation, inspiration retrieval, and normalized public result aggregation without relying on accounts, cookies, or private data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation and proxy use for public design pages can fail or produce partial results in restricted or unstable network environments.

Mitigation: Verify platform reachability first, reduce detail-page backfill when connections are unstable, and keep missing fields nullable instead of fabricating data.

Risk: Public design platform pages can change DOM structure or expose inconsistent author, publish time, or metrics fields.

Mitigation: Prefer search-page fields, treat missing metadata as normal, and review selectors before relying on outputs in downstream workflows.

Risk: Using public third-party platform data may create compliance concerns if private, authenticated, or high-resolution assets are collected.

Mitigation: Keep collection limited to public pages, avoid login-only APIs, cookies, authenticated sessions, and unnecessary high-resolution image enrichment.

## Reference(s):

- [Platform Methods](references/platform-methods.md)
- [Tag Guidance](references/tag-taxonomy.md)
- [ClawHub Skill Page](https://clawhub.ai/joeyyyy0430/skills/design-platform-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON record shape, public search URLs, selector notes, and network troubleshooting steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalized public result records may include nullable fields for missing authors, publish times, metrics, or unstable platform data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
