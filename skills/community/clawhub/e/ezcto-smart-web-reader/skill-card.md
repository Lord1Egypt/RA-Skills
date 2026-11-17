## Description:

Agent web access acceleration layer that reads URLs as structured JSON, using cache-first retrieval before parsing page content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[takahashigy](https://clawhub.ai/user/takahashigy)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to let an agent read public web pages as structured data instead of raw HTML or screenshots. It supports URL summarization, page analysis, site-type detection, and downstream skill chaining.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically process shared URLs, send extracted page data to a third-party service, and cache results locally.

Mitigation: Use it only for public, non-sensitive URLs; avoid tokenized links, intranet URLs, localhost services, authenticated pages, and pages containing sensitive information.

Risk: Cached or contributed page data may be stale, incomplete, or unsuitable for high-impact decisions.

Mitigation: Refresh and independently verify source pages before relying on results for financial, crypto, security, legal, or other consequential decisions.

Risk: The scanner guidance warns not to trust documented contribution opt-out behavior without verification.

Mitigation: Verify contribution controls before deployment and avoid permanent trusted-skill approval unless permissions, contribution behavior, cache retention, URL validation, and temporary-file handling are reviewed.

## Reference(s):

- [EZCTO Output JSON Schema](artifact/references/output-schema.md)
- [Site Type Auto-Detection Rules](artifact/references/site-type-detection.md)
- [OpenClaw Integration Guide](artifact/references/openclaw-integration.md)
- [EZCTO Web Translation Prompt](artifact/references/translate-prompt.md)
- [Crypto / Web3 Extension Fields](artifact/references/extensions/crypto-fields.md)
- [E-commerce Extension Fields](artifact/references/extensions/ecommerce-fields.md)
- [Restaurant / Food Service Extension Fields](artifact/references/extensions/restaurant-fields.md)
- [EZCTO API Documentation](https://ezcto.fun/api-docs)
- [ClawHub Skill Page](https://clawhub.ai/takahashigy/skills/ezcto-smart-web-reader)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured JSON with metadata, agent suggestions, and an optional cached Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cache hits can return an existing structured result; cache misses may fetch, parse, validate, and cache page data.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
