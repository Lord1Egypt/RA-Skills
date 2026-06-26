## Description: <br>
AI-Driven Development Life Cycle (AI-DLC) is an adaptive workflow for software development that guides agents through workspace detection, requirements, planning, design, code generation, and build/test tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sydpz](https://clawhub.ai/user/sydpz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Aidlc to run an adaptive, approval-gated software development workflow for new projects, features, bug fixes, refactoring, and migrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans the workspace and can create or update many workflow files. <br>
Mitigation: Run it in a dedicated repository or branch and review generated state, documentation, and code before committing changes. <br>
Risk: The workflow requires persistent audit logging of user input, which can retain secrets, credentials, private URLs, or proprietary snippets if they are provided during use. <br>
Mitigation: Instruct the agent not to record raw secrets or sensitive material in audit.md, and avoid providing credentials or confidential snippets during workflow prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sydpz/aidlc) <br>
- [Skill definition](SKILL.md) <br>
- [Process overview](references/common/process-overview.md) <br>
- [Question format guide](references/common/question-format-guide.md) <br>
- [Content validation](references/common/content-validation.md) <br>
- [Workspace detection](references/inception/workspace-detection.md) <br>
- [Requirements analysis](references/inception/requirements-analysis.md) <br>
- [Workflow planning](references/inception/workflow-planning.md) <br>
- [Code generation](references/construction/code-generation.md) <br>
- [Build and test](references/construction/build-and-test.md) <br>
- [Security baseline](references/extensions/security/baseline/security-baseline.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, implementation plans, generated code, command guidance, and workflow state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates workflow documentation under aidlc-docs and may generate application code in the workspace root.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
