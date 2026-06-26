## Description: <br>
Generates junior high school math review HTML documents with knowledge summaries, embedded SVG diagrams, exercises, and step-by-step answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangmange](https://clawhub.ai/user/wangmange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, parents, tutors, and educators use this skill to create structured junior high math review materials and practice sets for geometry, linear functions, inverse functions, and similar chapters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated HTML review documents into the current workspace. <br>
Mitigation: Use explicit output requests and review generated file paths and contents before relying on or sharing the documents. <br>
Risk: The skill records a short local memory entry with task paths and summaries after generation. <br>
Mitigation: Disable or avoid the memory step when local retention of paths or summaries is not desired. <br>
Risk: Generated math explanations and exercises may still need human review even after validator checks. <br>
Mitigation: Review the final HTML and validator results before using the material for instruction or assessment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangmange/ch-math-review-generator) <br>
- [README](artifact/README.md) <br>
- [Template guide](artifact/references/template_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [HTML files with embedded CSS and SVG, plus concise Markdown delivery notes and local validator command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes files in the active workspace, runs bundled Python validators, and may append a local memory note.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
