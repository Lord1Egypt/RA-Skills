## Description:

Dan Koe Writer helps an agent break down popular writing into reusable creative building blocks, generate content ideas, and assemble drafts for channels such as WeChat, Xiaohongshu, Twitter, and newsletters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alleliu](https://clawhub.ai/user/alleliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writing-focused agents use this skill to analyze source articles, build a reusable writing knowledge base, produce idea directions, and prepare prompts or context for original long-form and short-form content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article fetching can browse arbitrary user-provided URLs without network safeguards.

Mitigation: Use only trusted public URLs and avoid localhost, private-network, untrusted, or sensitive local-file targets.

Risk: Fetched or loaded article content is fed into model prompts and can influence extracted building blocks.

Mitigation: Review extracted JSON and knowledge entries before reusing them in future prompts or adding them to durable knowledge files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alleliu/skills/dan-koe-writer)
- [Dan Koe official site](https://www.dankoe.com)
- [Dan Koe newsletter](https://thedankoe.com/letters)
- [Knowledge index](references/knowledge/index.md)
- [Attention hooks](references/knowledge/hooks.md)
- [Paradoxes](references/knowledge/paradoxes.md)
- [Transformation arcs](references/knowledge/arcs.md)
- [Core problems](references/knowledge/core_problems.md)
- [Golden phrases](references/knowledge/golden_phrases.md)
- [Structures](references/knowledge/structures.md)
- [Perspectives](references/knowledge/perspectives.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON containing writing prompts, idea directions, reusable building blocks, and writing context.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts can read local text or fetch a user-provided article URL; model-based generation is performed by the calling agent.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
