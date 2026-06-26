## Description: <br>
Helps researchers draft, review, polish, and organize research fund proposals with writing templates, form checks, technical diagram guidance, and an optional daily check script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and academic grant writers use this skill to prepare research fund applications, especially drafting proposal sections, checking submission requirements, polishing academic language, and planning diagrams. It can also generate dated local check reports and Word document copies when the optional script is run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional daily_check.py script creates local dated reports and copies Word documents using hard-coded local paths. <br>
Mitigation: Inspect or edit the hard-coded paths and filenames before running the script, keep backups of important proposal documents, and run it only when local reports and copies are intended. <br>
Risk: Proposal guidance and checklists may be incomplete or mismatched to a specific fund program's current requirements. <br>
Mitigation: Review generated proposal text and form checks against the official fund instructions before submission. <br>


## Reference(s): <br>
- [Fund Proposal Assistant on ClawHub](https://clawhub.ai/jirboy/fund-proposal-assistant) <br>
- [jirboy publisher profile](https://clawhub.ai/user/jirboy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with templates, checklists, code snippets, and optional local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional daily_check.py script can create dated Markdown reports and Word document copies after local paths are reviewed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
