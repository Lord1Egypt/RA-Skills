## Description:

Use the Knowhere OpenClaw plugin to ingest local files or URLs, search stored documents, inspect parsed results, check jobs, and clean up stored document state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erickthoughts](https://clawhub.ai/user/erickthoughts)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Knowhere to work with documents through the Knowhere OpenClaw plugin: ingesting local files or URLs, searching stored content, inspecting parsed result files, checking import jobs, and cleaning up stored document state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ingested local files or URLs may be stored in the Knowhere scope for later retrieval.

Mitigation: Ingest only documents appropriate for that storage scope, and use remove or clear actions when stored document state should be deleted.

Risk: The skill depends on a third-party OpenClaw plugin being installed and enabled.

Mitigation: Install and enable the plugin only after confirming trust in the publisher and plugin source.

## Reference(s):

- [Knowhere OpenClaw Plugin](https://github.com/Ontos-AI/knowhere-openclaw-plugin)
- [Knowhere ClawHub Skill](https://clawhub.ai/erickthoughts/skills/clawhub-knowhere)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relies on the Knowhere OpenClaw plugin and the current scope's stored document state.]

## Skill Version(s):

0.1.0-beta.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
