## Description: <br>
Automatically generate NIH 2023-compliant Data Management and Sharing Plan (DMSP) drafts following FAIR principles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, grant writers, and research administrators use this skill to draft NIH Data Management and Sharing Plans from project details, repository choices, and data-sharing constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft plans can contain sensitive project, investigator, or institutional details saved in local files. <br>
Mitigation: Run the skill in a private workspace and review generated plans before sharing, committing, or submitting them. <br>
Risk: The output path writes a local file and could overwrite an important file if chosen carelessly. <br>
Mitigation: Choose --output deliberately and avoid pointing it at existing important files. <br>


## Reference(s): <br>
- [NIH Data Management and Sharing Policy](https://sharing.nih.gov/data-management-and-sharing-policy) <br>
- [NIH DMSP Template](references/nih_dmp_template.md) <br>
- [FAIR Principles](https://www.go-fair.org/fair-principles/) <br>
- [ClawHub Skill Page](https://clawhub.ai/AIPOCH-AI/data-management-plan-creator) <br>
- [AIPOCH-AI Publisher Profile](https://clawhub.ai/user/AIPOCH-AI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown DMSP draft, optional JSON wrapper, and local output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated drafts should be reviewed and customized before NIH submission.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
