## Description: <br>
Turns project material into case-study drafts by extracting background, actions, results, lessons, and reusable value. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content, marketing, and internal documentation teams use this skill to turn local project notes, evidence, and results into reviewable Markdown case studies with open questions and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated case-study drafts may include confidential or personal material supplied in local inputs. <br>
Mitigation: Use explicit approved input files, anonymize sensitive material before processing, and review drafts before sharing or publishing. <br>
Risk: Drafts can overstate customer endorsement, metrics, or outcomes when the source material is incomplete. <br>
Mitigation: Keep generated content reviewable, confirm evidence and metrics, and preserve open questions for missing facts instead of treating them as final claims. <br>
Risk: The optional local python3 helper reads user-supplied files and can write an output file. <br>
Mitigation: Run it only on approved local paths, use dry-run or stdout when appropriate, and inspect generated files before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/case-study-factory) <br>
- [Skill README](README.md) <br>
- [Case Study Specification](resources/spec.json) <br>
- [Output Template](resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown drafts, optional JSON from the local helper, and concise guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local input files; the optional helper requires python3 and no third-party dependencies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
