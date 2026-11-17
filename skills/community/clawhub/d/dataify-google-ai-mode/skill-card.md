## Description:

Search with Google AI Mode when the user explicitly requests AI Mode or AI-generated Google search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Google AI Mode searches through the Dataify Scraper API and receive compact, source-preserving search results. It is intended for explicit AI Mode or AI-generated Google search requests, not ordinary Google SERP lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Localized setup guidance may encourage storing API tokens permanently in plaintext shell startup files.

Mitigation: Use a session-scoped DATAIFY_API_TOKEN or a proper secret manager; rotate the token if it has already been stored in shell dotfiles or synced backups.

## Reference(s):

- [Dataify Google AI Mode API Reference](references/google_ai_mode_api.md)
- [Dataify Scraper API request endpoint](https://scraperapi.dataify.com/request)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-google-ai-mode)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands]

**Output Format:** [Concise Markdown summaries by default, with raw JSON or HTML when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source links, distinguishes missing fields from empty values, and uses DATAIFY_API_TOKEN for authenticated API calls.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
