## Description: <br>
Extracts decisions, owners, deadlines, assumptions, and reversal conditions from meeting notes, chat excerpts, or project materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, project leads, and governance reviewers use this skill to turn meeting notes, chat records, and document excerpts into reviewable decision ledgers for decision tracking, audit trails, and retrospectives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ledgers may misstate or overstate decisions if the source material is incomplete or ambiguous. <br>
Mitigation: Review the output before relying on it, and keep uncertain items in the explicit confirmation section. <br>
Risk: Input meeting notes or project documents may contain personal or sensitive information. <br>
Mitigation: Use local files you are authorized to process, prefer stdout or dry-run for sensitive material, and redact inputs before publication. <br>
Risk: The helper can write output files when invoked with an output path. <br>
Mitigation: Choose output locations deliberately and inspect the generated file before using it for governance, legal, or external publication decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/decision-ledger) <br>
- [Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README](README.md) <br>
- [Output Template](resources/template.md) <br>
- [Specification](resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown or JSON decision ledger; optional local script can write the result to a file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured sections include confirmed decisions, items to confirm, owners and deadlines, assumptions, reversal conditions, and dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
