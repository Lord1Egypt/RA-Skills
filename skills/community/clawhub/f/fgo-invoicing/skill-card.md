## Description:

Issue FGO.ro invoices through the FGO API with local automation for validating invoice payloads, issuing invoices, checking invoice status, getting print links, cancelling or deleting invoices, creating storno reversals, and fetching nomenclature lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-ai-tech](https://clawhub.ai/user/maverick-ai-tech)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to automate FGO.ro invoice workflows from agent-managed JSON payloads while preserving FGO-specific authentication, response, numbering, and rate-limit rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue, cancel, delete, or reverse real invoices.

Mitigation: Require explicit human approval before any final invoice operation, run a dry-run first, and use the FGO UAT endpoint for testing.

Risk: FGO credentials or customer invoice data may be exposed through prompts, logs, debug output, or full payload display.

Mitigation: Keep FGO_COD_UNIC and FGO_CHEIE_PRIVATA out of prompts and logs, avoid FGO_DEBUG and full payload output with real customer data, and run in a constrained environment.

Risk: A wrong API host or unsafe execution environment could send accounting actions to an unintended destination.

Mitigation: Verify the configured FGO API host before each real operation and install only when the publisher and runtime environment are trusted.

Risk: Parallel or excessive invoice operations can violate FGO operational constraints.

Mitigation: Execute FGO API calls sequentially and respect the documented one-call-per-second invoice operation rate limit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-ai-tech/skills/fgo-invoicing)
- [FGO API Notes](references/fgo-api.md)
- [Invoice example](references/invoice-example.json)
- [FGO production API](https://api.fgo.ro/v1)
- [FGO UAT API](https://api-testuat.fgo.ro/v1)
- [FGO API testing UI](https://api.fgo.ro/v1/testing.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON payloads, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus FGO_COD_UNIC and FGO_CHEIE_PRIVATA environment variables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
