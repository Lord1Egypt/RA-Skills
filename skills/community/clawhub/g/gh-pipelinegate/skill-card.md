## Description:

Pipelinegate chains Green Helix tools into configurable multi-step pipelines for scanning text, scanning skills, checking scope, validating JSON, diffing text, checking environments, and converting JSON or YAML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Pipelinegate to run ordered Green Helix tool checks through a local API and collect step-by-step results for security, validation, comparison, environment readiness, and format conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local PipelineGate API exposed beyond localhost could accept untrusted pipeline payloads.

Mitigation: Keep the service bound to localhost, or place authentication and request limits in front of it.

Risk: Pipeline payloads may contain text, skill content, schemas, or environment requirements that users did not intend to disclose.

Mitigation: Avoid sending secrets in pipeline payloads and keep inputs bounded to the intended review material.

Risk: Unpinned dependencies can change behavior between installations.

Mitigation: Pin and review dependencies before production use.

## Reference(s):

- [Pipelinegate on ClawHub](https://clawhub.ai/mirni/skills/gh-pipelinegate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pipeline responses include success, total_steps, completed_steps, and per-step results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
