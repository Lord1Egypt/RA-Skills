## Description:

把同一模板下签的多份合同按条款标题横向对齐，找出缺条、多条和条款正文差异，并输出带各方原文的条款对照结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, procurement, audit, and internal review users can compare multiple contracts created from the same template to spot omitted clauses and changed clause wording. The skill is for mechanical comparison and evidence organization, not legal advice or validity review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat mechanical clause comparison as legal advice or assume an unreported issue means the contracts are legally sound.

Mitigation: Present the output as comparison evidence only and require qualified legal review for legal effect, favorability, enforceability, signatures, and workflow questions.

Risk: The free version omits field, date, amount, placeholder, signature, and legality checks.

Mitigation: Review the listed withheld checks before relying on results and run separate review steps for out-of-scope issues.

Risk: Insufficient or poorly structured input can prevent reliable comparison.

Mitigation: Provide at least two substantive contract texts with recognizable clause headings or use the documented JSON input format.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/contract-comparison-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON containing executed checks, withheld checks, findings, summaries, clause comparison tables, evidence excerpts, and insufficient-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; accepts sample input, JSON contract arrays, or pasted contract text.]

## Skill Version(s):

1.0.57 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
