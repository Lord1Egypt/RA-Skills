## Description:

Find the cheapest meaningful visible price for a product across major Chinese shopping platforms

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to compare visible prices for a named product across major Chinese e-commerce platforms and decide where to buy. It asks for clarification when product variants are ambiguous and gives cautious conclusions when platform access or listing comparability is weak.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may read a partial platform scan as a definitive full-market lowest-price guarantee.

Mitigation: State which platforms were checked, identify visible-price limits, and use a limited conclusion when coverage or comparability is weak.

Risk: The airfare example may activate the skill for travel-buying advice outside its main China e-commerce price-comparison scope.

Mitigation: Clarify or remove the airfare example before release if the intended scope is product shopping only.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/cheap)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown sections with price comparison results, match confidence, caveats, and final advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clarifying questions, visible-price evidence, comparable platform options, and limited conclusions when evidence is weak.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
