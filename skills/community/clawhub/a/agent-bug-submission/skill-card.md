## Description: <br>
Agent Bug Submission helps users submit defects to TeamCycle, track defect status, and record defect details in Feishu Docs and Bitable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luiciferyi](https://clawhub.ai/user/luiciferyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA teams use this skill to collect defect details, format bug reports, submit them to TeamCycle through a local helper skill, and keep related tracking records in Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate local bug-reporter helper to submit data externally. <br>
Mitigation: Review the bug-reporter helper and confirm the TeamCycle and Feishu destinations are appropriate before installation or use. <br>
Risk: The artifact includes command examples that normalize passing passwords on the command line. <br>
Mitigation: Use a token, secret manager, SSO/OAuth flow, or another protected credential path instead of command-line passwords. <br>
Risk: Bug reports may contain secrets, confidential product information, or sensitive incident details. <br>
Mitigation: Redact secrets and confidential data before submitting defect reports or writing records to external systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luiciferyi/agent-bug-submission) <br>
- [TeamCycle platform](https://teamcycle.100credit.cn) <br>
- [Feishu defect tracking table](https://my.feishu.cn/wiki/FWYmwGwgziQGzBkxETHctCg5nDK?table=tblt64TGQqsHqcSu&view=vewqJU0Fv4) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown defect templates, command examples, and status summaries with defect links and IDs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call TeamCycle and Feishu destinations and depends on a separate local bug-reporter helper for submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
