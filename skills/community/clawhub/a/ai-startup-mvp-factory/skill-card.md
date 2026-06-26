## Description: <br>
AI Startup MVP Factory orchestrates PRD creation, full-stack MVP code generation, PR review and wiki sync, and Docker CI/CD output for startup application prototypes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, product managers, and small startup teams use this skill to turn a product idea into a structured PRD, generated project code, review output, wiki documentation, and container deployment assets. It is intended for rapid MVP validation and startup prototype delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can trigger broad repository, wiki, container, and deployment-related actions without clear approval gates or scoping. <br>
Mitigation: Before execution, confirm the target repository, wiki space, container registry, credentials, and whether each external action should be dry-run, local-only, or published. <br>
Risk: The skill may require sensitive credentials for external services and deployment workflows. <br>
Mitigation: Use least-privilege credentials, keep secrets out of generated code and logs, and review generated configuration before running CI/CD or push steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/ai-startup-mvp-factory) <br>
- [README.md](artifact/README.md) <br>
- [workflow.json](artifact/workflow.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown, generated project files, Docker configuration, review reports, and deployment guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require repository, wiki, registry, and third-party API credentials depending on the selected workflow steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
