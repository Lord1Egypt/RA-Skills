## Description: <br>
Calculates gestational age and follow-up date windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and healthcare workflow operators can use this skill to calculate gestational age from an LMP date and estimate follow-up date windows from a start date. Outputs should be reviewed before clinical use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write a JSON result to a user-specified output path. <br>
Mitigation: Use a dedicated workspace output path, avoid pointing output at important existing files, and review generated files before sharing them. <br>
Risk: Date calculations may be used in clinical workflows where incorrect dates could affect downstream decisions. <br>
Mitigation: Treat results as calculation aids and have qualified users review outputs before clinical use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/date-calculator) <br>
- [Date Calculator references](references/guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [JSON results written to stdout or to a user-specified output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports gestational and follow-up calculation modes with date, weeks, window-days, and optional output-file parameters.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
