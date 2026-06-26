## Description: <br>
A reusable agent skill for multi-round review of Chinese management-oriented master's theses, especially MBA, MEM, and MPA, with applicability to similar professional and applied research theses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wmpluto](https://clawhub.ai/user/wmpluto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to review Chinese master's thesis drafts, run first-pass or iterative re-review workflows, and produce strict but actionable revision feedback in Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a user-provided thesis document and saves extracted thesis text and review notes locally. <br>
Mitigation: Use a clean working folder, protect the generated files according to the thesis sensitivity, and delete review_artifacts after review when retention is not needed. <br>
Risk: An existing review_results.md triggers iterative re-review and may affect how prior issues are checked. <br>
Mitigation: Before re-review, confirm that any existing review_results.md belongs to the same thesis and review cycle. <br>
Risk: Plain-text extraction from .docx can lose figures, table structure, formulas, and some cross-reference context. <br>
Mitigation: Manually check the original Word document for visual material, formulas, tables, and cross-references that cannot be verified from extracted text alone. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wmpluto/academic-thesis-review) <br>
- [Repository URL](https://github.com/wmpluto/academic-thesis-review-skill) <br>
- [Author GitHub profile](https://github.com/wmpluto) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Chinese Markdown review report with local text and Markdown working files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates review_results.md and timestamped review_artifacts files for extracted thesis text and working notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence, target metadata, and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
