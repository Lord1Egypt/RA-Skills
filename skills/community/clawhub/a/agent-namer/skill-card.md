## Description: <br>
Generates and tracks internal agent names in the "货xx" format so teams can avoid duplicate active names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cxlhyx](https://clawhub.ai/user/cxlhyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and internal agent maintainers use this skill to propose role-appropriate "货xx" candidate names, check whether a name is already active, and record active or retired names in a local registry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Add or kill operations change the local name registry. <br>
Mitigation: Review registry-changing commands before running them and inspect scripts/used_names.json after updates. <br>
Risk: Role descriptions used for naming could include sensitive operational details. <br>
Mitigation: Avoid putting secrets or sensitive internal details in role descriptions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON registry updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Name registry operations can update scripts/used_names.json when the helper commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
