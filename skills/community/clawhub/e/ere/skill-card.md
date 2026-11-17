## Description:

Editorial Refinement Engine transforms LLM-generated text into editorially refined prose with more natural rhythm, lexicon, structure, and style while preserving facts, entities, and quotes in English and Portuguese (pt-BR).

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickkbarbosa](https://clawhub.ai/user/rickkbarbosa)

### License/Terms of Use:

MIT

## Use Case:

Writers, editors, marketers, documentation authors, and agent users use this skill to refine AI-generated drafts into publishable editorial prose while preserving factual details, entities, numbers, dates, and quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented analysis workflow stores submitted text in predictable shared temporary file paths.

Mitigation: Avoid confidential drafts until the workflow uses a private temporary directory with cleanup, or adapt local usage to write files in a restricted temporary directory.

Risk: Fact-preservation claims are editorial guidance and still require human review.

Mitigation: Before publication, compare the original and refined text and verify names, numbers, dates, entities, and quoted language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rickkbarbosa/skills/ere)
- [AI writing patterns catalog](references/patterns.md)
- [Classics' writing principles catalog](references/writing-principles.md)
- [Portuguese (pt-BR) writing principles](references/portuguese-writing-principles.md)
- [Editorial Refinement Engine architecture](references/ERE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Refined prose in plain text or Markdown, with optional JSON analysis metrics and diffs from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports editorial profiles and refinement levels; outputs should preserve supplied facts, entities, dates, numbers, and quotes.]

## Skill Version(s):

1.4.0 (source: frontmatter, manifest.json, release.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
