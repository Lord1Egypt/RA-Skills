## Description: <br>
Project Analyzer guides an agent through project discovery, architecture mapping, code-quality assessment, and structured reporting for existing codebases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a repository, identify its technology stack and architecture, assess quality and security concerns, and produce a prioritized Markdown report with actionable recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository contents, including sensitive files, may enter the agent context during analysis. <br>
Mitigation: Use the skill only on repositories intended for inspection and avoid running it on projects containing secrets unless that exposure is acceptable. <br>
Risk: Suggested shell commands or recommendations may be inappropriate for a specific repository. <br>
Mitigation: Review proposed shell commands and recommendations before execution or implementation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mtsatryan/ah-project-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown report with optional shell commands and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prioritized recommendations, estimated effort, and suggested follow-on agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
