## Description:

Boss orchestrates a BMAD-style software delivery workflow from requirements through deployment by coordinating specialized PM, architecture, UI design, tech lead, scrum master, frontend, backend, QA, and DevOps agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echovic](https://clawhub.ai/user/echovic)

### License/Terms of Use:

MIT

## Use Case:

Developers use Boss to plan and execute new projects or feature work through a structured Chinese-language workflow. The skill produces planning, architecture, UI, task, QA, and deployment artifacts while coordinating specialist agents across the delivery cycle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can automatically modify projects, install or run tools, start services, and deploy or expose URLs with weak scoping.

Mitigation: Run it only in a disposable or version-controlled workspace, prefer --skip-deploy until the generated plan is reviewed, and require approval before package installs, global npm installs, docker-compose, service startup, deployment, or external URL exposure.

Risk: Broad trigger phrases and the --quick option can reduce user review before execution.

Mitigation: Use explicit /boss invocation, avoid --quick for normal work, and keep confirmation checkpoints for requirements and planning review.

## Reference(s):

- [Boss Skill on ClawHub](https://clawhub.ai/echovic/skills/boss-skill)
- [README](README.md)
- [Design Document](DESIGN.md)
- [BMAD Methodology](references/bmad-methodology.md)
- [Artifact Guide](references/artifact-guide.md)
- [Testing Standards](references/testing-standards.md)
- [Quality Gate](references/quality-gate.md)
- [Agent Browser](https://github.com/vercel-labs/agent-browser)
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
- [Agile Manifesto](https://agilemanifesto.org/)
- [EARS Requirements Syntax](https://www.iaria.org/conferences2013/filesICCGI13/ICCGI_2013_Tutorial_Terzakis.pdf)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese-language Markdown documents with inline code blocks, shell commands, and structured checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured project artifacts under .boss/<feature>/ and supports --skip-ui, --skip-deploy, and --quick options.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
