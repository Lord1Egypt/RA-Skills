## Description: <br>
Helps agents rewrite or remove code comments so they are concise Chinese notes focused on rationale, edge cases, algorithm intent, and risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhongm](https://clawhub.ai/user/yhongm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill when writing, editing, reviewing, or refactoring code to keep comments concise, Chinese-only, and focused on why the code exists rather than restating what it does. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is broad and opinionated, so it may remove comments that a repository expects to preserve. <br>
Mitigation: Review diffs carefully and explicitly preserve license notices, generated-file markers, lint directives, public API documentation, TODOs, and required English or mixed-language comments. <br>
Risk: Chinese-only comment rewriting may conflict with project documentation standards or team language requirements. <br>
Mitigation: Use the skill only in repositories where concise Chinese comments are desired, or provide task-level instructions for exceptions before applying changes. <br>
Risk: Comment cleanup can reduce useful context when comments explain non-obvious behavior, operational risk, or API contracts. <br>
Mitigation: Keep comments that explain business rationale, complex algorithms, edge cases, fallback behavior, side effects, performance traps, or concurrency risk. <br>


## Reference(s): <br>
- [ClawHub Code Comment skill page](https://clawhub.ai/yhongm/code-comment) <br>
- [ClawHub yhongm publisher profile](https://clawhub.ai/user/yhongm) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Guidance] <br>
**Output Format:** [Markdown code block containing a complete runnable source file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Only comments are changed; executable logic, names, and imports are intended to remain unchanged.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
