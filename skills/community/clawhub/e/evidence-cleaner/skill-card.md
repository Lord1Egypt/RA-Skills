## Description:

Evidence Cleaner helps an agent clean raw search results, webpage snippets, OCR fragments, and similar source material into standardized evidence while reducing noise, duplicate content, pseudo-entities, and off-topic sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z1one0415](https://clawhub.ai/user/z1one0415)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent builders use this skill to prepare noisy raw evidence for downstream analysis by stripping technical clutter, detecting pseudo-entities, deduplicating related snippets, downranking weak sources, and preserving audit warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evidence may be dropped or downranked based on source-quality judgments.

Mitigation: Review removed_noise, downranked_items, and warnings before relying on the cleaned evidence.

Risk: The workflow is written primarily in Chinese, which may affect operators who cannot review the rules directly.

Mitigation: Use the skill only when the operator can understand or independently verify the cleaning rules and output.

## Reference(s):

- [Noise Pattern Recognition Guide](references/noise-patterns.md)
- [Clean, Downrank, and Drop Rules](references/clean-vs-drop-rules.md)
- [Evidence Cleaning Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON containing cleaned evidence, removed noise, downranked items, warnings, and cleaning statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is documentation-only and expects users to review dropped or downranked evidence before relying on the result.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
