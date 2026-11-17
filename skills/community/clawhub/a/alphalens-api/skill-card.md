## Description:

AlphaLens API helps agents research companies, products, competitors, investor networks, peer benchmarks, and white-space opportunities using the AlphaLens API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidmustapha](https://clawhub.ai/user/walidmustapha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and market analysts use this skill to turn AlphaLens subscription access into repeatable company discovery, competitive mapping, investor network, peer benchmark, pipeline enrichment, and white-space analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AlphaLens API key and sends selected company, product, feature, document, or pipeline data to AlphaLens.

Mitigation: Install only when this data sharing is acceptable, keep ALPHALENS_API_KEY secret, and avoid printing or persisting any part of the key.

Risk: Some workflow templates can place user-controlled text into shell commands.

Mitigation: Validate domains, URL-encode query text, and avoid copying raw user input directly into shell commands before execution.

Risk: Generated reports may depend on remote scripts or public favicon fetching.

Mitigation: Review generated HTML before opening or sharing it, and avoid remote dependencies unless that behavior is acceptable for the environment.

## Reference(s):

- [AlphaLens homepage](https://alphalens.ai)
- [AlphaLens API Reference](references/REFERENCE.md)
- [AlphaLens API Examples](references/EXAMPLES.md)
- [AlphaLens API docs](https://api-production.alphalens.ai/docs)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash commands and generated self-contained HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALPHALENS_API_KEY and an active AlphaLens subscription; workflows may produce HTML reports suitable for browser viewing or PDF export.]

## Skill Version(s):

2.1.1 (source: SKILL.md frontmatter, skill.yaml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
