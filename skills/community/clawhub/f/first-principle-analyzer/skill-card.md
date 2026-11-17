## Description:

Use this skill when analyzing complex problems through first principles with a structured 7-phase framework for assumptions, basic truths, and solution generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, entrepreneurs, researchers, and decision makers use this skill to break complex technical, business, product, career, or academic questions into assumptions, first principles, and candidate solutions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Bash and Exec even though first-principles analysis normally only needs conversational guidance.

Mitigation: Remove or limit shell/process execution permissions before installation unless a reviewed deployment requires them.

Risk: Users may provide sensitive business, personal, financial, legal, or medical context during analysis.

Mitigation: Avoid entering confidential details unless data sharing, export behavior, and model-provider handling have been reviewed.

Risk: Generated analysis can be persuasive but incomplete or wrong for high-stakes decisions.

Mitigation: Use outputs as decision support and require domain expert review before acting on legal, medical, financial, or major business recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pagoda111king/skills/first-principle-analyzer)
- [First Principle Analyzer Documentation](https://docs.cloud-shrimp.com/first-principle-analyzer)
- [ClawHub Skill Docs](https://clawhub.ai/skills/first-principle-analyzer/docs)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, 5 Why decomposition, basic truths, solution options, comparisons, and decision guidance.]

## Skill Version(s):

2.4.2 (source: server release metadata; artifact SKILL.md and package.json report 2.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
