## Description:

DevOps Pipeline Management helps agents manage the lifecycle of quality-platform DevOps pipelines, including workspace lookup, pipeline creation and updates, execution, cancellation, status checks, logs, and templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaizhanhui](https://clawhub.ai/user/zhaizhanhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to find workspaces and pipelines, create or update pipeline definitions, trigger or cancel runs, inspect run status and details, and work from reusable pipeline templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, run, update, cancel, and delete real DevOps pipelines.

Mitigation: Install and use it only for accounts and environments where the agent is intended to operate pipelines, and require human review before destructive or production-impacting actions.

Risk: Pipeline data and API responses may contain sensitive operational details that can appear in logs or shared transcripts.

Mitigation: Avoid captured or shared logs for sensitive runs, remove verbose logging where possible, and treat pipeline configuration and run output as sensitive data.

Risk: A misconfigured DevOps API endpoint could send pipeline data or commands to the wrong service.

Mitigation: Pin DEVOPS_BFF_URL to the trusted HTTPS DevOps host before use and avoid untrusted endpoint overrides.

Risk: Non-interactive creation or execution paths can auto-fill parameters, auto-confirm choices, or run pipelines without the same level of operator review.

Mitigation: Prefer interactive mode for creation and execution, review generated configuration before saving, and avoid non-interactive operation unless defaults have been audited.

## Reference(s):

- [Skill README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [Pipeline Create Guide](artifact/references/pipeline-create.md)
- [Pipeline Run Guide](artifact/references/pipeline-run.md)
- [Pipeline Update Guide](artifact/references/pipeline-update.md)
- [Pipeline Delete Guide](artifact/references/pipeline-delete.md)
- [Pipeline API Overview](artifact/references/pipeline/openapi/00-api-overview.md)
- [Pipeline Data Structure](artifact/references/pipeline/01-pipeline-data-structure.md)
- [Pipeline Template Data Structure](artifact/references/pipeline/02-pipeline-template-data-structure.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and operational instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue or suggest Python command-line calls that operate against configured DevOps pipeline APIs]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
