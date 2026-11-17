## Description:

抖音复刻蒸馏写作 analyzes an author's articles to reconstruct thinking patterns and writing style, then produces a dedicated writing persona sub-skill and style prompt for Douyin-oriented content workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, operators, and style researchers use this skill to analyze authorized source articles, distill an author's writing identity, and generate a reusable persona for same-style drafting or style study.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect content and read local files while building a writing corpus.

Mitigation: Use only content the user is authorized to analyze, and avoid broad private directories or unrelated local files.

Risk: The skill relies on RedFox API access through the REDFOX_API_KEY environment variable.

Mitigation: Confirm key source, scope, expiry, and revocation path; do not expose the key in prompts, logs, code, or output files.

Risk: The skill may install or update a persistent writing persona under the local skills directory.

Mitigation: Inspect the generated SKILL.md before allowing installation or updates, then scan the resulting skill before deployment.

Risk: Generated writing personas can imitate identifiable authors in ways that may confuse readers or exceed permitted use.

Mitigation: Limit use to authorized style analysis and disclose or constrain persona use where attribution, consent, or platform policy requires it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/redfox-data/skills/douyin-copywrite-alchemy)
- [Core workflow](artifact/references/core_workflow.md)
- [Writing style and thinking framework](artifact/references/7-dimensions-framework.md)
- [Persona template](artifact/references/persona-template.md)
- [Writing formulas](artifact/references/writing-formulas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown analysis, reusable style prompt, and generated SKILL.md persona content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install or update a local writing persona sub-skill after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
