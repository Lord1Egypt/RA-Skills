## Description: <br>
Skill Forge generates task_suite.yaml test suites from existing SKILL.md files, generates SKILL.md plus task_suite.yaml from skill_spec.yaml files, and can optionally run local evaluation and improvement workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use Skill Forge to generate test suites for existing agent skills, create new skills from structured specifications, and inspect coverage gaps against generated scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills or task suites may include incorrect, incomplete, or misleading guidance. <br>
Mitigation: Review generated SKILL.md and task_suite.yaml outputs before relying on them or publishing them. <br>
Risk: Optional --evaluate and --auto-improve modes call local improvement tools. <br>
Mitigation: Use those modes only when the local improvement-evaluator and improvement-orchestrator installations are trusted. <br>
Risk: Documented calibration and judge-selection safeguards may not be fully implemented in code. <br>
Mitigation: Treat generated suites as drafts and inspect whether tasks actually measure skill-specific behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/auto-skill-forge) <br>
- [Skill Spec Format](references/spec-format.md) <br>
- [Code Review Spec Example](references/examples/code-review-spec.yaml) <br>
- [Release Notes Spec Example](references/examples/release-notes-spec.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown and YAML files with optional command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task_suite.yaml, generated SKILL.md files, and optional evaluation reports depending on mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
