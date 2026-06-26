## Description: <br>
Build lightweight, minimal CI/CD scaffolding around a small project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyharry](https://clawhub.ai/user/hyharry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add proportionate GitHub Actions, smoke checks, release artifacts, and minimal Docker scaffolding to small repositories without introducing heavyweight deployment complexity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CI/CD files can change repository automation, including triggers, package install commands, artifact uploads, or later deploy-related behavior. <br>
Mitigation: Review generated workflow and Docker files before committing, and confirm triggers, installs, artifact uploads, deploy changes, and secret usage are intentional. <br>
Risk: A minimal template may not fully match the repository's actual runtime, package manager, or test setup. <br>
Mitigation: Inspect existing README and config first, then run the same cheap checks locally when practical before relying on the pipeline. <br>


## Reference(s): <br>
- [Minimal CI/CD templates](references/templates.md) <br>
- [Easy CI/CD on ClawHub](https://clawhub.ai/hyharry/easy-ci-cd) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, Dockerfile, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concise repository changes and verification notes; no bundled executable code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
