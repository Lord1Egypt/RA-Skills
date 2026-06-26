## Description: <br>
Docs Improver is a local Python documentation helper that analyzes documentation quality, generates missing technical docs, checks consistency with code, and produces prioritized improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerry-guo-mys](https://clawhub.ai/user/jerry-guo-mys) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical writers use this skill to audit project documentation, generate missing README, API, architecture, installation, contribution, and changelog files, check drift between docs and code, and plan improvements before releases or onboarding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write modes can replace or create project documentation files. <br>
Mitigation: Prefer analysis or check modes for read-only review; when generating docs, use an explicit output directory or version control and review diffs before relying on changes. <br>
Risk: Generated or suggested documentation may be incomplete or inaccurate for the target codebase. <br>
Mitigation: Review generated reports and files, run the consistency check, and validate examples, API details, and architecture descriptions against the source code. <br>


## Reference(s): <br>
- [Documentation Best Practices](references/best-practices.md) <br>
- [Documentation Style Guides](references/style-guides.md) <br>
- [Mermaid Diagram Templates](assets/diagrams/mermaid-templates.md) <br>
- [Documentation Templates](scripts/templates/templates.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, generated documentation files, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some modes write documentation files; use an explicit output directory or version control for generated output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
