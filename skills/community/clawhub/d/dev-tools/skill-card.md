## Description: <br>
A developer toolbox skill for managing project specifications, running pre-commit checks, diagnosing errors, tracking technical debt, comparing code differences, generating refactoring suggestions, and analyzing dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lf951515851](https://clawhub.ai/user/lf951515851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill during repository work to manage coding specifications, check changes before commit, diagnose failures, track technical debt, compare diffs, plan refactors, and analyze dependency boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan local project code and write reports or project-support files. <br>
Mitigation: Install it only for repository development workflows and review generated .ads/ and docs/ files before committing or sharing them. <br>
Risk: The shell helper writes boundary-check reports relative to the active project root. <br>
Mitigation: Run the helper from the intended repository root or set PROJECT_ROOT explicitly before execution. <br>
Risk: Refactoring suggestions and apply-style workflows may produce changes that need human validation. <br>
Mitigation: Review diffs, generated reports, and any refactor-apply changes before merging. <br>


## Reference(s): <br>
- [Dev Tools ClawHub release page](https://clawhub.ai/lf951515851/dev-tools) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact prompt](artifact/prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and text guidance with command examples, code snippets, generated reports, and optional JSON or HTML exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write project reports under .ads/ and docs/ paths, and the shell helper writes boundary-check reports under docs/boundary-checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
