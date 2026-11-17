## Description:

Guides agents through sequential thinking for complex tasks, including task decomposition, dynamic revisions, branching exploration, and hypothesis validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paibwhgs](https://clawhub.ai/user/paibwhgs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to structure complex requests into ordered steps, revise earlier reasoning, explore branches, and validate candidate solutions during planning and execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted thinking records may contain private data, credentials, business plans, or other sensitive context.

Mitigation: Require explicit user consent before saving thinking records, avoid persisting raw reasoning or secrets, and redact sensitive content before storage.

Risk: Automatic activation on complex tasks may create thinking records when the user did not expect long-lived notes.

Mitigation: Define clear activation rules and retention limits before installing the skill in workflows that handle sensitive work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paibwhgs/skills/agent-sequential-thinking)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sequential thinking records and optional branch or revision metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
