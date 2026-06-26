## Description: <br>
Find and shortlist third-party services using OpenSpend CLI marketplace search for discovery and comparison tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albertpurnama](https://clawhub.ai/user/albertpurnama) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to discover external service providers for a requested capability, compare up to five marketplace results, and present concise recommendations without setup, installation, or purchase steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace search may require OpenSpend authentication. <br>
Mitigation: Run with an existing session when possible and ask for explicit user confirmation before any login command. <br>
Risk: Returned services may require separate setup, paid usage, or account configuration. <br>
Mitigation: Review providers first, start with a small validation call, and request explicit approval before moving to any payment or setup flow. <br>
Risk: Using an untrusted OpenSpend CLI could expose the user to unsafe local tooling behavior. <br>
Mitigation: Use only a trusted OpenSpend CLI installation and avoid install or update commands within this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albertpurnama/find-services) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise service summaries and inline shell commands when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to five services in marketplace order with short match explanations and a recommended usage note.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
