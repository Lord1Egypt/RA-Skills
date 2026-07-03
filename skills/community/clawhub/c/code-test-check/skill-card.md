## Description: <br>
Analyzes local PRD documents or functional test cases against user-selected backend and frontend source code, then produces a Markdown verification report with code evidence and an implementation status matrix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxpfreesky](https://clawhub.ai/user/zxpfreesky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and reviewers use this skill to compare PRDs or functional test cases with selected source directories and identify implemented, partially implemented, missing, or requirement-divergent behavior. It also prompts for related impact analysis so regression testing can cover affected shared assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local PRD, test case, and source files that may contain confidential requirements or proprietary code. <br>
Mitigation: Run it only in workspaces where the agent is allowed to inspect those files, and confirm the specific source directories before analysis begins. <br>
Risk: The skill may create a Markdown report under docs or beside the requirement document. <br>
Mitigation: Confirm the report destination before execution, especially in repositories where generated files should be controlled. <br>
Risk: Static source analysis may miss runtime behavior such as feature flags, permissions, database-driven branches, asynchronous jobs, or third-party service responses. <br>
Mitigation: Use the report as review and test-design input, and pair it with runtime testing for critical or high-risk functions. <br>


## Reference(s): <br>
- [Tech Stack Guide](references/tech-stack-guide.md) <br>
- [Report Template](report/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown verification report with implementation matrix, code evidence, risk notes, and regression recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a report beside the requirement document or under docs when the user confirms the destination.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
