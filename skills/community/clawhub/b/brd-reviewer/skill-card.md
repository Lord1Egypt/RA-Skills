## Description: <br>
Reviews Business Requirements Documents in DOCX format by extracting paragraph-level context, drafting clarification questions, and producing a reviewed Word document with comments and tracked changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChipmunkRPA](https://clawhub.ai/user/ChipmunkRPA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, product owners, and implementation teams use this skill to review BRD DOCX files for ambiguity, incomplete requirements, inconsistent wording, and missing acceptance criteria before stakeholder review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BRD contents may contain confidential business information that is copied into the review JSON and reviewed DOCX outputs. <br>
Mitigation: Process only documents approved for local handling, choose output folders deliberately, and protect or delete review JSON files that contain sensitive text. <br>
Risk: Generated questions or replacement wording may misstate business intent or add requirements that stakeholders have not approved. <br>
Mitigation: Review all comments and tracked changes with the document owner before accepting revisions or relying on the updated BRD. <br>
Risk: Running the bundled pipeline from an unintended location or with unintended paths could write review artifacts somewhere unexpected. <br>
Mitigation: Run the script from the intended skill directory, consider a virtual environment for dependencies, and verify input and output paths before materializing the reviewed document. <br>


## Reference(s): <br>
- [Review JSON Schema](references/review-json-schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ChipmunkRPA/brd-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [DOCX and JSON files with supplemental text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces <name>.review.json and <name>.reviewed.docx beside the source BRD unless another output path is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
