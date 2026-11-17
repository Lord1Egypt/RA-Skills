## Description:

Search the Apple App Store, read a full app listing by App Store id or bundle id, and pull user reviews as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and app marketers use this skill to search App Store listings, retrieve app metadata, and collect review data for ASO, competitor research, catalogue audits, and bulk metadata workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: App Store query terms, app identifiers, and the Scavio API key are sent to Scavio for external API calls.

Mitigation: Use a revocable API key, avoid sensitive queries where third-party API use is not acceptable, and deploy only in environments approved for Scavio access.

Risk: API calls consume Scavio credits, and optional SDK installation introduces third-party dependency exposure.

Mitigation: Monitor credit usage, prefer direct HTTPS examples or isolated SDK environments, and review dependency installation before use.

## Reference(s):

- [Scavio App Store Search Documentation](https://scavio.dev/docs/app-store-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=apple-app-store-api)
- [Scavio Rate Limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=apple-app-store-api)
- [ClawHub Skill Listing](https://clawhub.ai/scavio-ai/skills/apple-app-store-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, Python, JavaScript, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses are structured JSON; calls require SCAVIO_API_KEY and consume Scavio credits.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
