## Description: <br>
Reviews Chinese contracts, identifies contract-type-specific risks, and prepares Word Track Changes revisions, comments, clean copies, reports, and structured change records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wux818738-alt](https://clawhub.ai/user/wux818738-alt) <br>

### License/Terms of Use: <br>
GPL-3.0 <br>


## Use Case: <br>
Legal, business, and operations users use this skill to review Chinese-language contracts, locate clause-level risks, draft revisions, add explanatory comments, and manage iterative negotiation rounds. Developers and agent operators can also use the bundled scripts and references to generate DOCX outputs, clean copies, review reports, and structured change logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify legal documents and generate revisions that may be inaccurate, incomplete, or unsuitable for the parties' legal position. <br>
Mitigation: Preserve original contracts and require a qualified legal reviewer to check generated revisions, comments, clean copies, and reports before relying on them. <br>
Risk: The skill may change the local Python environment or rely on optional OCR/document dependencies. <br>
Mitigation: Install only in a controlled workspace or virtual environment and preinstall reviewed OCR and document-processing dependencies instead of allowing runtime dependency changes. <br>
Risk: Security guidance warns against untrusted or unusual filenames until shell invocation is fixed. <br>
Mitigation: Use trusted input paths and simple filenames, avoid adversarial filenames, and run the workflow in a constrained workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wux818738-alt/contract-reviewer-wudi) <br>
- [Project homepage from clawdis metadata](https://github.com/wux818738-alt/contract-reviewer-wudi) <br>
- [Engine guide](references/engine-guide.md) <br>
- [Output specification](references/output-spec.md) <br>
- [Review playbook](references/review-playbook.md) <br>
- [Contract type reference](references/contract-types/README.md) <br>
- [Clause library index](references/clause-library/index.json) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [DOCX files with Word Track Changes and comments, clean DOCX copies, plain-text review reports, JSON change records, and command-oriented workflow guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create output directories for single-round or multi-round contract review workflows; original contracts should be preserved separately.] <br>

## Skill Version(s): <br>
2.9.5 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
