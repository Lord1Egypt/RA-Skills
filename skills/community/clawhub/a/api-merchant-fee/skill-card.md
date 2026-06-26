## Description: <br>
Queries merchant fee and rate information through a merchant API when the user provides agent, API key, merchant, and terminal identifiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sgfa005](https://clawhub.ai/user/sgfa005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Merchant operators, support staff, and agents use this skill to retrieve merchant card, scan payment, terminal, and management fee details from an API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Merchant API credentials are saved locally in plaintext for reuse. <br>
Mitigation: Prefer per-session credentials or a secure secret store; if local reuse is required, restrict file permissions and rotate or delete the API key on shared or synced machines. <br>
Risk: The skill depends on a configured merchant API endpoint before sending encrypted merchant lookup requests. <br>
Mitigation: Confirm the endpoint and network path before installation and use only an approved merchant API environment. <br>
Risk: Merchant fee lookups can expose sensitive business information if prompts or outputs are shared broadly. <br>
Mitigation: Limit use to authorized merchant-support workflows and redact credentials or merchant identifiers from shared transcripts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sgfa005/api-merchant-fee) <br>
- [Publisher profile](https://clawhub.ai/user/sgfa005) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown text with merchant fee details, validation prompts, or error summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store agentNo and API key locally in scripts/.auth.json for reuse.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
