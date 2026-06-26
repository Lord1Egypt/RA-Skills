## Description: <br>
Set up and query business data across 100+ sources, including Stripe, HubSpot, and Salesforce, via SQL with agent-driven setup, cross-source joins, and mutations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kappa90](https://clawhub.ai/user/kappa90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Dinobase to initialize local or cloud-backed business data connections, sync source data, inspect schemas, run SQL queries across tools, and preview write-back mutations before confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dinobase connects to business systems using API keys or OAuth, so credentials and source permissions can expose sensitive account data if over-scoped or handled carelessly. <br>
Mitigation: Use least-privilege or test credentials where possible, avoid pasting production secrets into visible command lines when a safer secret mechanism is available, and review connected sources before sync or query work. <br>
Risk: Dinobase can write data back to upstream systems through UPDATE or INSERT workflows. <br>
Mitigation: Treat mutation previews as the approval point and confirm only changes the user explicitly intends to apply. <br>


## Reference(s): <br>
- [Dinobase homepage](https://dinobase.ai) <br>
- [ClawHub skill page](https://clawhub.ai/kappa90/dinobase) <br>
- [Publisher profile](https://clawhub.ai/user/kappa90) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, Code] <br>
**Output Format:** [Markdown with inline bash, JSON, and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents through Dinobase CLI setup, source connection, sync, schema discovery, SQL querying, and mutation preview or confirmation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
