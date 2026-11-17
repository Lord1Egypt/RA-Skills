## Description:

Optimizes articles, landing pages, docs, and brand content for visibility, citation, and recommendation in generative AI answer systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhuadeng](https://clawhub.ai/user/jinhuadeng)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams, marketers, editors, and agents use this skill to audit or rewrite pages, articles, docs, FAQs, comparisons, and Chinese content so it is clearer, more extractable, and more likely to be cited or summarized by AI answer engines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make content sound more likely to appear in AI-generated answers than the evidence supports.

Mitigation: Keep claims framed as improvements to structure, extractability, citation likelihood, and answer-engine fitness; do not promise rankings, placement, or guaranteed traffic.

Risk: Helper scripts read local content files supplied by the user.

Mitigation: Run the scripts only on files intended for content analysis and review the generated audit or rewrite JSON before using it in published materials.

Risk: Chinese GEO playbooks and rewrite helpers may produce Chinese or mixed Chinese/English output.

Mitigation: Adapt the final output to the user's requested language and market before delivery.

## Reference(s):

- [GEO Principles](references/geo-principles.md)
- [Query Patterns](references/query-patterns.md)
- [Rewrite Playbook](references/rewrite-playbook.md)
- [Chinese GEO Playbook](references/chinese-geo-playbook.md)
- [Chinese GEO Templates](references/chinese-geo-templates.md)
- [Demo Use Cases](references/demo-use-cases.md)
- [Sales Positioning](references/sales-positioning.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance and structured JSON from optional helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Chinese or mixed Chinese/English output when using Chinese GEO mode or the bundled rewrite scripts.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
