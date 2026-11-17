## Description:

Provides Chinese-first academic writing polishing, bilingual academic style refinement, logic review, and critical framework support for humanities and social science writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aymmo](https://clawhub.ai/user/aymmo)

### License/Terms of Use:

MIT

## Use Case:

External users and researchers use this skill to polish Chinese or English academic prose, identify reasoning gaps, refine argument structure, and build critique frameworks for humanities and social science writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated polishing or style-imitation guidance may be mistaken for original scholarship or proper citation.

Mitigation: Review outputs for academic integrity, attribution, and citation before using them in academic work.

Risk: Most guidance and checker output are Chinese-first, which may not match an English-only workflow unless requested clearly.

Mitigation: Specify the target language and publication style before asking the agent to revise or critique text.

Risk: The optional Node checklist can read local files when invoked with --file.

Mitigation: Pass only intended document paths to the checker and review results before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aymmo/skills/aymmo-academic-polish)
- [Project homepage](https://github.com/Aymmo/academic-polish)
- [Style guide](references/style-guide.md)
- [Dai Jinhua framework](references/dai-jinhua-framework.md)
- [Methodology overview](references/methodology-overview.md)
- [Questioning library](references/questioning-library.md)
- [Counter-arguments guide](references/counter-arguments.md)
- [Concept pairs guide](references/concept-pairs.md)
- [Resistance archaeology guide](references/resistance-archaeology.md)
- [Logic review guide](references/logic-review-guide.md)
- [English academic guide](references/english-academic-guide.md)
- [Wang Minan framework](references/scholars/wang-minan-framework.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance and revised prose, with optional local checklist output from the Node script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first guidance with English academic polishing support; the optional checker can read a local file only when explicitly invoked with --file.]

## Skill Version(s):

1.3.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
