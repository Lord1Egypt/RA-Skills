## Description: <br>
ctx-shrink is a codebase analyzer that generates smart context maps for AI agents and catches packaging mistakes before they leak. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etherman-os](https://clawhub.ai/user/etherman-os) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run ctx-shrink on a project, read its AI-CONTEXT.md or JSON output, and summarize architecture, endpoints, models, dependencies, and publish-safety findings with actionable fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running a local project scanner can surface sensitive file names or contents in generated reports if users share the output without review. <br>
Mitigation: Keep real secrets out of test repositories, review generated reports before sharing them, and confirm file contents are not uploaded unless explicitly intended. <br>
Risk: Optional PATH setup or symlink commands can change which ctx-shrink executable an agent runs later. <br>
Mitigation: Read the README before installation and only add the helper to a user-controlled PATH location when global access is desired. <br>
Risk: Agent-proposed fixes based on ctx-shrink findings may be incomplete or incorrect for a specific project. <br>
Mitigation: Review proposed fixes and rerun the scanner before publishing or deploying the project. <br>


## Reference(s): <br>
- [ClawHub ctx-shrink listing](https://clawhub.ai/etherman-os/ctx-shrink) <br>
- [ctx-shrink install instructions](https://github.com/etherman-os/ctx-shrink#install) <br>
- [ctx-shrink releases](https://github.com/etherman-os/ctx-shrink/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; ctx-shrink output may be Markdown or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ctx-shrink to already be available on PATH and reads the generated AI-CONTEXT.md or custom output file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
