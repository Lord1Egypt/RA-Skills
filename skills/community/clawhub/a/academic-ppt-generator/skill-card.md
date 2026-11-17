## Description:

Guides agents through preparing academic-paper analysis JSON, generating a structured slide plan, and exporting a Chinese-language academic report PowerPoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziyi-z-z](https://clawhub.ai/user/ziyi-z-z)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and academic presenters use this skill to turn a reviewed paper analysis into a standard report deck covering background, methods, findings, limitations, and contributions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect or incomplete paper-analysis JSON can produce misleading academic slides.

Mitigation: Review the extracted paper facts and generated slide structure before presenting or sharing the deck.

Risk: The PowerPoint export depends on the external python-pptx package.

Mitigation: Use a virtual environment and pin python-pptx when reproducibility or stricter supply-chain controls are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziyi-z-z/skills/academic-ppt-generator)
- [Literature analysis guide](references/analysis_guide.md)
- [Example paper analysis JSON](references/example_analysis.json)
- [PPT template notes](assets/template_readme.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands, JSON slide structure, and PowerPoint .pptx output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-prepared or reviewed paper-analysis JSON and the python-pptx dependency.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
