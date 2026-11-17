## Description:

Xiaohongshu title strategy skill for Chinese creators that helps agents match topics, drafts, or existing titles to trigger families and formula IDs, then produce traceable title options with rationale and testing recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content strategists use this skill to turn Chinese Xiaohongshu topics, drafts, or existing titles into formula-attributed title packs. It helps an agent identify audience intent, select suitable trigger families, generate concise Chinese title options, and recommend the strongest candidates to test.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to Chinese Xiaohongshu-specific title strategy, which may be unsuitable for other platforms, languages, or bilingual deliverables.

Mitigation: State the desired platform, language, and format explicitly when using the skill outside its default Xiaohongshu Chinese context.

Risk: Formula-driven titles can overpromise if the underlying content does not support the selected hook or outcome.

Mitigation: Check the topic promise and body support before finalizing titles, and reject or revise options whose claims cannot be paid off by the content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cellinlab/skills/cell-xhs-title-selector)
- [Metadata homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/xhs-title-selector)
- [Title formula catalog](artifact/references/formula-catalog.md)
- [Trigger families reference](artifact/references/trigger-families.md)
- [Workflow reference](artifact/references/workflow.md)
- [Quality bar](artifact/references/quality-bar.md)
- [Title pack template](artifact/assets/title-pack-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown title strategy pack with formula IDs, rationale, ranked recommendations, and next-step advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese Xiaohongshu-oriented titles and requires formula attribution for generated options.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
