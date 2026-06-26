## Description: <br>
AI-DLC provides an adaptive AI-driven software development lifecycle workflow for new projects, features, bug fixes, refactoring, migration, and other development tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sydpz](https://clawhub.ai/user/sydpz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to guide software work through adaptive inception, construction, and operations phases with requirements analysis, planning, design, code generation, build, and test steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly activates for ordinary coding tasks and may shape many development workflows. <br>
Mitigation: Install it only where a structured AI-DLC process is desired, and review the generated workflow plan and approval gates before continuing. <br>
Risk: The skill records user input verbatim in aidlc-docs/audit.md, which can capture secrets or sensitive project information. <br>
Mitigation: Avoid pasting secrets, treat audit.md as sensitive, consider excluding audit files from version control, and prefer sanitized summaries if the workflow is customized. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sydpz/ai-dlc) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Process overview](artifact/references/common/process-overview.md) <br>
- [Requirements analysis](artifact/references/inception/requirements-analysis.md) <br>
- [Workflow planning](artifact/references/inception/workflow-planning.md) <br>
- [Code generation](artifact/references/construction/code-generation.md) <br>
- [Build and test](artifact/references/construction/build-and-test.md) <br>
- [Security baseline extension](artifact/references/extensions/security/baseline/security-baseline.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents, implementation plans, code changes, test/build guidance, and shell command recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates AI-DLC workflow documentation under aidlc-docs when used by an agent.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
