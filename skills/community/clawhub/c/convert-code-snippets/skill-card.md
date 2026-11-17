## Description:

Converts code snippets, schemas, structured data, and code styles between programming languages, formats, and conventions while preserving semantic equivalence where possible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to convert code between supported languages, generate typed code from schemas, transform coding styles, and convert structured data formats with warnings for areas that need manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted code may be syntactically valid but not fully semantically equivalent for language-specific features or unavailable target libraries.

Mitigation: Review warnings, run target-language parsers or linters, and test converted code before using it in production.

Risk: The README contains stale template references to read/write modes and API_KEY configuration that are not supported by the current skill artifacts.

Mitigation: Do not provide credentials for this skill unless the publisher updates the artifacts with a supported integration and security model.

## Reference(s):

- [Metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills)
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/convert-code-snippets)
- [Reference index](references/index.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and structured conversion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source and target language labels, conversion metrics, warnings, and manual-review notes.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog report 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
