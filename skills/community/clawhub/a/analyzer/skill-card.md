## Description: <br>
Analyzes an existing project to produce a detailed, structured report on its architecture, patterns, technical debt, and key areas for downstream work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cankocakulak](https://clawhub.ai/user/cankocakulak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and downstream agents use Analyzer when starting work on an existing or unfamiliar codebase, especially before feature planning, onboarding, or product requirements work. It creates a repository-level project snapshot with structure, conventions, risks, opportunities, and a handoff contract. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The analysis can include sensitive implementation details from the selected repository. <br>
Mitigation: Choose the project_path deliberately and review the generated analysis before sharing it or using it as downstream agent context. <br>
Risk: Downstream agents may rely on an incomplete or outdated project snapshot. <br>
Mitigation: Review the analysis for accuracy and refresh it when the codebase changes materially. <br>


## Reference(s): <br>
- [Analyzer ClawHub listing](https://clawhub.ai/cankocakulak/analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis document with a machine-readable YAML summary and handoff contract] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes docs/[project-name]/analysis.md when used as directed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
