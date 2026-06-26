## Description: <br>
Guides users through a structured workflow to compose, draft, and review a clinical trial Data Validation Plan for CRO or sponsor data management contexts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unfallenwill](https://clawhub.ai/user/unfallenwill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical data management teams use this skill to turn study materials, protocol details, CRF information, and review decisions into a structured Data Validation Plan. It supports phased collection, validation strategy, check design, alignment, drafting, Excel generation, and internal quality review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to overwrite files under dvp_workspace during normal workflow execution. <br>
Mitigation: Run it in a fresh project or back up existing DVP outputs before use, and review generated files before relying on them. <br>
Risk: The scanner verdict is suspicious because of explicit overwrite behavior, even though no credential or tool-risk findings were reported. <br>
Mitigation: Review the workspace changes and generated DVP content before deployment or distribution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/unfallenwill/dvp-composer) <br>
- [DVP Document Structure Catalog](references/section-catalog.md) <br>
- [Excel Output Specification](references/excel-spec.md) <br>
- [Example DVP Output](references/example-output.md) <br>
- [Phase 1: Collection](references/stages/phase-1-collection.md) <br>
- [Phase 2: Scope & Strategy](references/stages/phase-2-strategy.md) <br>
- [Phase 3: Design Check Content](references/stages/phase-3-design.md) <br>
- [Phase 4: Alignment](references/stages/phase-4-alignment.md) <br>
- [Phase 5: Draft](references/stages/phase-5-draft.md) <br>
- [Phase 6: Internal Review](references/stages/phase-6-review.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, Excel workbook, and workspace file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates phase deliverables under dvp_workspace/ and generates a final DVP Excel workbook.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
