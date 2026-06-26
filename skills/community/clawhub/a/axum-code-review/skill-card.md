## Description: <br>
Reviews axum web framework code for routing patterns, extractor usage, middleware, state management, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Rust HTTP services that use axum, tower, or hyper, with checks for routing, extractors, state, middleware, and error handling before reporting findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent to inspect Rust project files for review evidence. <br>
Mitigation: Use it in environments where reading the target codebase is acceptable. <br>
Risk: The workflow references a separate review-verification-protocol skill for category-specific checks. <br>
Mitigation: Use that referenced skill only when it is available and trusted in the review environment. <br>
Risk: Code review findings can be misleading when they are not grounded in the current project tree. <br>
Mitigation: Require Cargo.toml version and edition checks plus current file-line citations before reporting findings. <br>


## Reference(s): <br>
- [Routing](references/routing.md) <br>
- [Extractors](references/extractors.md) <br>
- [Middleware](references/middleware.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown code review findings with file-line citations and severity labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should cite current-tree evidence and include severity.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
