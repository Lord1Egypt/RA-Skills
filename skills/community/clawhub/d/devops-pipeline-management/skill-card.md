## Description: <br>
Expert for DevOps pipeline management that helps agents query workspaces and templates, create or update pipelines, execute or cancel runs, and inspect pipeline execution records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaizhanhui](https://clawhub.ai/user/zhaizhanhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to manage CI/CD pipeline lifecycle tasks, including workspace discovery, pipeline creation and updates, execution, cancellation, deletion, and run-detail inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run, cancel, delete, save, and update CI/CD pipelines. <br>
Mitigation: Install it only for trusted DevOps users, start with non-production or least-privilege accounts, and require explicit human confirmation before run, cancel, delete, save, or update actions. <br>
Risk: Non-interactive creation or execution helpers can change pipeline state with fewer prompts. <br>
Mitigation: Review generated pipeline configuration before use and prefer interactive or preview-based flows for production-impacting changes. <br>
Risk: Console logs may include request headers, request bodies, response bodies, or internal infrastructure details. <br>
Mitigation: Treat logs as sensitive, avoid sharing raw command output, and redact account, repository, pipeline, environment, or secret-like values before disclosure. <br>


## Reference(s): <br>
- [Pipeline Management Skill README](README.md) <br>
- [Pipeline Create Guide](references/pipeline-create.md) <br>
- [Pipeline Run Guide](references/pipeline-run.md) <br>
- [Pipeline Cancel Guide](references/pipeline-cancel.md) <br>
- [Pipeline Delete Guide](references/pipeline-delete.md) <br>
- [Pipeline OpenAPI Overview](references/pipeline/openapi/00-api-overview.md) <br>
- [Execute Pipeline API](references/pipeline/openapi/06-execute-pipeline-api.md) <br>
- [Pipeline Data Structure](references/pipeline/01-pipeline-data-structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured DevOps platform APIs and print request and response details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
