## Description: <br>
Automatically reviews code to identify critical bugs, security flaws, performance issues, and style violations before human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill as a first-pass reviewer after significant changes, before merges, and during code review to surface bugs, security problems, performance issues, and style concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repo-wide, CI, or pre-commit review examples may send source code to the configured OpenClaw/model tooling. <br>
Mitigation: Enable those modes only after confirming the project is approved for that tooling and model path. <br>
Risk: The GitHub Actions example uses an API key for model-backed review. <br>
Mitigation: Store the API key only in the intended CI secret store and avoid placing credentials in source files. <br>
Risk: Automated review can miss issues or produce misleading findings. <br>
Mitigation: Use the skill as a first-pass prompt aid and keep human review for critical code paths. <br>


## Reference(s): <br>
- [Autonomous Code Review on ClawHub](https://clawhub.ai/1477009639zw-blip/autonomous-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown checklist and structured JSON issue reports with optional shell and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review scope can be a file, diff, staged changes, or full repository as documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
