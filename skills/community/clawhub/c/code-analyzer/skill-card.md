## Description: <br>
Analyzes codebases to summarize architecture, execution flow, data flow, business rules, external dependencies, data models, and Domain-Driven Design patterns across common languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerry-guo-mys](https://clawhub.ai/user/jerry-guo-mys) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect unfamiliar codebases, prepare architecture documentation or code reviews, evaluate technical debt, and generate DDD-focused analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can summarize private architecture, business logic, dependencies, and code quality issues. <br>
Mitigation: Review reports before sharing them and avoid running the skill on repositories or directories that contain sensitive material unless that disclosure is acceptable. <br>
Risk: The analysis scripts read a user-selected local path and write Markdown reports to a user-selected output path. <br>
Mitigation: Run the scripts only against intended project paths, use the documented exclude option for irrelevant or sensitive directories, and choose output locations deliberately. <br>
Risk: Static analysis findings and DDD pattern detection may be incomplete or require domain review. <br>
Mitigation: Treat reports as analysis aids, then validate important findings against the source code and project maintainers before making architecture or remediation decisions. <br>


## Reference(s): <br>
- [Code Analysis Best Practices](references/best-practices.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes analysis report files to user-specified output paths; reports may include metrics, issue lists, Mermaid diagrams, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
