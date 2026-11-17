## Description:

Evaluates whether a workflow has enough information, permission, tools, evidence, and safety boundaries to proceed or should be clarified, reviewed, narrowed, or refused.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a pre-workflow readiness gate before multi-step tasks, tool use, file changes, external actions, or high-impact decisions. It helps decide whether to start, ask for missing details, retrieve evidence, request approval, route to review, narrow scope, or refuse unsafe work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The readiness gate can introduce extra clarification or approval steps before work begins.

Mitigation: Use it where deliberate pre-workflow checks are valuable, especially around private data, external actions, money, production systems, or other higher-impact workflows.

Risk: Readiness payloads could include unnecessary private or sensitive details if the caller over-shares context.

Mitigation: Send only minimal redacted summaries and omit secrets, credentials, raw private records, full logs, full transcripts, and unrelated private data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mindbomber/skills/aana-workflow-readiness-check)
- [README](artifact/README.md)
- [Workflow Readiness Check Schema](artifact/schemas/workflow-readiness-check.schema.json)
- [Redacted Workflow Readiness Check Example](artifact/examples/redacted-workflow-readiness-check.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with an optional structured readiness payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; does not install dependencies, execute commands, call services, write files, or persist memory.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
