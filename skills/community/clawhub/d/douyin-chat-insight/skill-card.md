## Description:

Analyzes user-provided group or direct chat exports, including Douyin chats, and generates a single-page conversation value report covering facts, unresolved tensions, demand quotes, and follow-up actions without IM login or required cloud keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tars1230](https://clawhub.ai/user/tars1230)

### License/Terms of Use:

MIT

## Use Case:

External users, community operators, content researchers, and consultants use this skill to turn chat exports they already possess into local, reviewable insight reports. It is intended for consented or authorized data review, not for logging into IM services, scraping groups, or collecting credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat exports can contain private or sensitive personal information.

Mitigation: Use only exports the user is authorized to analyze, keep processing local, and review or redact generated reports before sharing them.

Risk: The security review flags optional cloud transcription guidance because it points users to a referral signup flow and weak persistent API-key storage.

Mitigation: Treat cloud transcription as optional, avoid referral signup unless intentionally selected, and prefer session-scoped environment variables or a dedicated secret manager for API keys.

Risk: Heuristic findings can be incomplete or misleading if treated as final conclusions.

Mitigation: Review evidence references, unresolved tensions, and action items before using the report for decisions or public communication.

Risk: Requests to log in, scrape groups, use cookies, or run third-party exporters can exceed the skill's intended boundary.

Mitigation: Refuse credential collection and silent scraping requests; require a user-provided export path before analysis.

## Reference(s):

- [README](README.md)
- [Security Policy](SECURITY.md)
- [Input Formats](references/input-formats.md)
- [Report Four-Block Specification](references/report-4block.md)
- [Routing Boundaries](references/routing-boundaries.md)
- [How to Get Exports](references/how-to-get-exports.md)
- [Optional Douyin Link ASR](references/optional-douyin-link-asr.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with bash command blocks; generated reports as HTML, Markdown, and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inventory-first workflow; deep analysis requires an explicit conversation selection; reports are heuristic drafts that require human review before external sharing.]

## Skill Version(s):

0.2.1 (source: frontmatter, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
