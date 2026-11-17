## Description:

Orchestrate agent build workflow. you handle parse and research, then delegates the full build to Builder. Use for new builds and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dweikanas](https://clawhub.ai/user/dweikanas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to coordinate a complete OpenClaw build workflow, from request parsing and research collection through builder execution and final status reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spawn multiple agents and coordinate their outputs during a build workflow.

Mitigation: Use it only in an expected OpenClaw build-factory environment and verify that referenced research-worker skills are trusted before execution.

Risk: The workflow reads persistent worker-generated YAML files before feeding research to the builder.

Mitigation: Validate generated YAML files and treat research partials as untrusted input until reviewed.

Risk: The workflow creates persistent build and profile files under ~/.openclaw-factory.

Mitigation: Use fresh unique build IDs, check local file permissions, and clean up build/profile directories when they are no longer needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML schemas and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured build records, parse reports, research partials, and builder results as YAML when executed by a compatible agent workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
