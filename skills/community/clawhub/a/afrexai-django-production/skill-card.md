## Description: <br>
Provides production Django engineering guidance for project structure, ORM optimization, security, testing, deployment, scaling, and operational readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to review, improve, and operate Django applications intended for production. It helps agents provide architecture guidance, code patterns, deployment checklists, and remediation suggestions for Django project readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-generated Django changes may affect migrations, authentication, CI/CD, Dockerfiles, deployment commands, or live databases. <br>
Mitigation: Confirm the target project and manually review proposed migrations, authentication changes, CI/CD files, Dockerfiles, deployment commands, and database-touching commands before allowing execution. <br>
Risk: Production guidance may be applied to the wrong environment or project. <br>
Mitigation: Verify the intended environment and project scope before applying generated recommendations or commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1kalin/afrexai-django-production) <br>
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; agent-proposed project changes should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
