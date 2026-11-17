## Description:

Ai-Deodorizer rewrites AI-generated text to make English and Chinese drafts sound more natural and human-written.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xx235300](https://clawhub.ai/user/xx235300)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to humanize AI-generated or draft text, review writing for common AI patterns, and rewrite content with selectable light, medium, or strong editing strength.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text and an API key are sent to a configurable external LLM endpoint.

Mitigation: Avoid confidential, regulated, or private drafts unless remote processing is acceptable; keep API_BASE unset or restrict it to the intended MiniMax HTTPS endpoint and use a revocable API key.

Risk: The rewriting prompts may add voice, opinions, or emphasis not present in the source text.

Mitigation: Review rewritten output against the original before publishing or using it in factual, legal, medical, financial, or compliance-sensitive contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xx235300/skills/ai-deodorizer)
- [Ai-Deodorizer project homepage](https://github.com/xx235300/ai-deodorizer)
- [MiniMax platform](https://platform.minimaxi.com/)
- [Methodology](scripts/METHODOLOGY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text or Markdown rewritten content, with shell commands and configuration examples when used through the CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write output to a user-specified UTF-8 file; sends submitted text to a MiniMax-compatible remote API.]

## Skill Version(s):

2.0.0 (source: frontmatter, README.md, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
