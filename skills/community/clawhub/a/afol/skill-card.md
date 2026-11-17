## Description:

Use this orchestration skill to choose the right AFOL provider skill for catalog lookup, marketplace pricing, collection management, valuation, and cross-provider workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musketyr](https://clawhub.ai/user/musketyr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AFOL collection agents use this skill to route broad LEGO collector requests to the right provider skill for catalog lookup, marketplace pricing, collection management, valuation, and cross-provider ID workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider skills may access private collection, marketplace, store, order, valuation, or sales-ledger data.

Mitigation: Limit provider credentials, summarize private data, and avoid exposing raw account or collection payloads.

Risk: An agent could treat available credentials as permission to make marketplace or collection changes.

Mitigation: Require explicit current-conversation user approval, review the exact provider command, and use dry-run plus provider guard flags before any write.

## Reference(s):

- [AFOL Router Prompt](references/prompts/afol-router.txt)
- [AFOL Metadata OpenAPI Placeholder](references/openapi/afol.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes tasks to provider skills; the local CLI reports routing and credential readiness without calling provider APIs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
