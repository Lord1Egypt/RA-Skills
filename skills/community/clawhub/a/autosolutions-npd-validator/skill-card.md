## Description:

Runs a full new product development validation pipeline on a product concept using research coordination, independent evaluators, adversarial review, and consensus synthesis to produce a GO, CONDITIONAL GO, REVISIT, or NO-GO recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac)

### License/Terms of Use:

MIT-0

## Use Case:

Product, brand, and commercial teams use this skill to evaluate whether a product concept is ready to launch, needs revision, or should be stopped. The skill is suited to concept validation workflows that require market, competitive, brand-fit, commercial, consumer-trend, and adversarial perspectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product concepts and internal business data may be saved into workspace files during validation.

Mitigation: Provide only necessary data, review generated data and user_provided files after use, and delete sensitive files when validation is complete.

Risk: Validation reports may influence product investment decisions using external research and model-generated synthesis.

Mitigation: Review cited sources, confidence labels, and assumptions before using recommendations for launch or investment decisions.

## Reference(s):

- [NPD Methodology Reference](artifact/npd-methodology/SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/autosolutionsai-didac/skills/autosolutions-npd-validator)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown reports and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes concept briefs, evaluation reports, adversarial analysis, and a final validation report into workspace files.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
