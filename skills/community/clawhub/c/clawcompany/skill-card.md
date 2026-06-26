## Description: <br>
AI virtual team collaboration system with PM/Dev/Review agents for automated software development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felix-miao](https://clawhub.ai/user/felix-miao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use ClawCompany to turn feature or application requests into a coordinated PM, development, and review workflow that can generate or modify project files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically edit files in a project through its development agent workflow. <br>
Mitigation: Run it in a clean repository or branch, use dry-run first where practical, and manually inspect all diffs before accepting changes. <br>
Risk: Verbose logs or agent session output may expose API or session details. <br>
Mitigation: Keep verbose logs private and avoid pasting secrets or sensitive project data into requests. <br>
Risk: The built-in review agent may approve changes that still require human review. <br>
Mitigation: Treat the review output as advisory and perform a separate manual code and security review before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/felix-miao/clawcompany) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [GLM API documentation](https://open.bigmodel.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON and markdown-style agent progress summaries with generated file paths and code artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify files in the configured project path; dry-run mode can be used to preview workflow behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
