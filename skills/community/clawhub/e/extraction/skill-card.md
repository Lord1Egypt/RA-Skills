## Description: <br>
Extract design systems, architecture patterns, and methodology from codebases into reusable skills and documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to analyze existing repositories, identify reusable design, architecture, workflow, and methodology patterns, and turn those patterns into project-agnostic documentation or agent skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation or skills may include confidential project details, secrets, or incorrect guidance from the analyzed repository. <br>
Mitigation: Review diffs, scan generated files before committing, and remove sensitive or misleading content before sharing or deploying the outputs. <br>
Risk: The workflow can create or update docs/extracted/ and ai/skills/ files in the target repository. <br>
Mitigation: Run it only on repositories approved for analysis and inspect file changes before committing them. <br>
Risk: Optional staging copy commands can move generated content to another local path. <br>
Mitigation: Confirm the destination path and copied content before running staging commands. <br>


## Reference(s): <br>
- [Methodology Values](references/methodology-values.md) <br>
- [Extraction Categories](references/extraction-categories.md) <br>
- [Skill Quality Criteria](references/skill-quality-criteria.md) <br>
- [Extraction Validation Checklist](references/validation-checklist.md) <br>
- [Design System Template](references/output-templates/design-system.md) <br>
- [Project Summary Template](references/output-templates/project-summary.md) <br>
- [Skill Template](references/output-templates/skill-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown documents, skill files, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update docs/extracted/ and ai/skills/ files in the target repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
