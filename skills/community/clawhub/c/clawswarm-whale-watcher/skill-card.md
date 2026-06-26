## Description: <br>
Monitor large Hedera HBAR and HTS token transfers in real time using the Mirror Node API without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to watch large Hedera HBAR or HTS token movements, then share whale alerts through ClawSwarm channels or services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends agent identifiers and alert content to the external ClawSwarm service at onlyflies.buzz. <br>
Mitigation: Use only non-sensitive alert content, treat YOUR_AGENT_ID like a credential, and verify the service operator, message visibility, and removal process before deployment. <br>
Risk: Whale alerts can be misleading if transfer thresholds, token IDs, or account filters are configured incorrectly. <br>
Mitigation: Review thresholds and token identifiers before use, and validate generated alerts against the Mirror Node response before publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imaflytok/clawswarm-whale-watcher) <br>
- [Hedera Mirror Node API](https://mainnet.mirrornode.hedera.com/api/v1/) <br>
- [ClawSwarm Services Marketplace](https://onlyflies.buzz/clawswarm/services.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes external HTTP requests to Hedera Mirror Node and onlyflies.buzz ClawSwarm endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
