## Description:

Maps a plain-language mood or feeling to matching visual styles and the words that triggered them, for art direction and image-generation prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixi048](https://clawhub.ai/user/xixi048)

### License/Terms of Use:

MIT

## Use Case:

Artists, designers, and image-prompt authors can use the skill to translate a short mood description into visual-style vocabulary and ranked style references. Results provide direction for creative work rather than a single definitive artistic answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: With cloud access enabled, a description may be sent even when a local style match exists, contrary to the stated fallback rule.

Mitigation: For private descriptions, omit --allow-cloud or use --offline after caching the dictionary.

Risk: The optional MCP package adds a separately installed component.

Mitigation: Pin and review the optional MCP package before running it.

## Reference(s):

- [API contract](artifact/references/api-contract.md)
- [Feeling Search documentation](https://xiximm.cloud)
- [Quota documentation](https://xiximm.cloud/docs/quota.html)
- [ClawHub skill page](https://clawhub.ai/xixi048/skills/feeling-search)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides ranked style candidates with matched feeling words; candidates are reference points for human art direction.]

## Skill Version(s):

1.2.0 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
