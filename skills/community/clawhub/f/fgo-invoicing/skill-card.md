## Description: <br>
Issue FGO.ro invoices through the FGO API with local automation for validating invoice payloads, issuing invoices, checking status, getting print links, cancelling or deleting invoices, creating storno reversals, and fetching nomenclature lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Maverick-AI-Tech](https://clawhub.ai/user/Maverick-AI-Tech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and finance operations teams use this skill to prepare, validate, issue, inspect, cancel, delete, and reverse FGO.ro invoices through a local CLI workflow. It is intended for controlled invoice operations where final mutations require explicit human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mutate real invoice records by issuing, cancelling, deleting, or reversing invoices. <br>
Mitigation: Require explicit human approval before any final invoice mutation and use dry-run validation before issuing invoices. <br>
Risk: Production FGO credentials grant access to invoice operations. <br>
Mitigation: Install only where the agent is permitted to use FGO production credentials, and prefer the UAT base URL for testing. <br>
Risk: Debug logging can expose sensitive business data from requests or responses. <br>
Mitigation: Avoid `FGO_DEBUG` and `--debug` when handling real customer or production invoice data. <br>
Risk: Invoice operation calls may exceed documented rate or sequencing constraints. <br>
Mitigation: Run FGO API calls sequentially and observe the documented one-call-per-second invoice operation limit. <br>


## Reference(s): <br>
- [FGO API Notes](references/fgo-api.md) <br>
- [Invoice Example JSON](references/invoice-example.json) <br>
- [FGO production API base URL](https://api.fgo.ro/v1) <br>
- [FGO UAT API base URL](https://api-testuat.fgo.ro/v1) <br>
- [ClawHub skill page](https://clawhub.ai/Maverick-AI-Tech/fgo-invoicing) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local validation output, dry-run payloads, and FGO API response summaries; final invoice mutations require explicit approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
