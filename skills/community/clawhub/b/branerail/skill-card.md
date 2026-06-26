## Description: <br>
CTO-level architectural advisor for AI-native development that helps Claude Code review design decisions, resilience, scaling, state ownership, observability, dependencies, and system design before and during implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uditakhourii](https://clawhub.ai/user/uditakhourii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan and audit AI-generated systems for architecture, state ownership, failure handling, observability, scaling, dependencies, concurrency, and migration risk. It also provides templates for architectural specs, design system documentation, and code review checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may cause the skill to activate frequently during normal engineering conversations. <br>
Mitigation: Narrow activation to explicit architecture, design review, resilience, migration, or system planning requests when deploying in a shared agent environment. <br>
Risk: The bundled packaging script creates and copies release files and should not be run blindly in a production workspace. <br>
Mitigation: Inspect the script and run it only in a disposable or version-controlled working directory after confirming the generated files are desired. <br>
Risk: Logging examples include operational and payment-context fields that could be adapted in ways that capture secrets, payment data, or unnecessary personal identifiers. <br>
Mitigation: Redact credentials and sensitive personal or payment data before applying the logging patterns; keep only identifiers needed for debugging and compliance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uditakhourii/branerail) <br>
- [Architectural Specification Template](artifact/references/spec_template.md) <br>
- [Code Review Checklist](artifact/references/code_review_checklist.md) <br>
- [DESIGN Template](artifact/references/DESIGN_template.md) <br>
- [Google design.md](https://github.com/google-labs-code/design.md) <br>
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, templates, example code, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce architectural recommendations, specs, review findings, deployment checklists, and design-system documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
