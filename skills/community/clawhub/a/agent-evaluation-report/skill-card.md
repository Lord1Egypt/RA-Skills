## Description: <br>
Generates standardized evaluation reports for intelligent agent systems from user-provided test data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luiciferyi](https://clawhub.ai/user/luiciferyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA teams, and project stakeholders use this skill to turn agent test data into a standardized evaluation report covering scope, environment, execution results, defects, business validation, risk assessment, and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write generated reports to a preset Feishu location or local path without a clearly documented confirmation step. <br>
Mitigation: Confirm the destination and filename before allowing any local write or Feishu document update. <br>
Risk: Evaluation inputs may include confidential project, test, defect, or business-risk details. <br>
Mitigation: Share only data appropriate for the configured workspace and verify Feishu permissions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luiciferyi/agent-evaluation-report) <br>
- [Publisher profile](https://clawhub.ai/user/luiciferyi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown report and optional Word document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save reports under output/effect-reports/ or write to a configured Feishu document destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
