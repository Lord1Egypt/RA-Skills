## Description:

Ancient Poetry Master helps agents answer Chinese classical poetry questions, compose or compare poems in selected poet styles, analyze meter and allusions, and generate interactive poet knowledge-graph reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to explore Chinese classical poetry, request original poems or lyric-style compositions, analyze supplied poems, compare poets, query allusions, and generate knowledge-graph visualizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The knowledge-graph generator can overwrite arbitrary writable paths if given an unsafe output path.

Mitigation: Run graph generation only with a trusted, dedicated .html output path inside an intended report directory.

Risk: Generated graph reports load D3.js from the internet when opened.

Mitigation: Open generated reports only in environments where remote JavaScript loading is acceptable, or revise the skill to bundle or integrity-pin D3.js.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bettermen/skills/ancient-poetry-master)
- [Chinese Classical Poetry Meter Reference](artifact/references/forms.md)
- [Poetry Allusions Quick Reference](artifact/references/allusions.md)
- [Core Poets Dataset](artifact/references/poets.json)

## Skill Output:

**Output Type(s):** [text, markdown, HTML files, JSON, shell commands, guidance]

**Output Format:** [Markdown responses, Chinese poem text, structured JSON analysis output, and generated interactive HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Graph generation writes an HTML file to a caller-supplied path; poem analysis can emit structured JSON.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
