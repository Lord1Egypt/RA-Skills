## Description:

Implement UCP broadcast of buyer intents to eligible nodes, including message signing, routing, and ack handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement UCP publish/subscribe behavior that broadcasts signed buyer intents to eligible nodes, tracks acknowledgements, and feeds responses into quote intake.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced runtime code may handle private keys, buyer intent data, target nodes, retries, and quote responses outside the reviewed artifact.

Mitigation: Before installing or using the skill, confirm that the separate runtime package is available and review that code independently.

Risk: Incorrect canonical serialization, signing, or retry handling could cause failed dispatch, invalid acknowledgements, or duplicate broadcast attempts.

Mitigation: Keep JSON serialization deterministic, attach the protocol version to every envelope, record per-node retry counters, and stop retries after a configured threshold.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown implementation guidance with suggested file paths, contracts, event mappings, guardrails, and validation commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is included in the reviewed artifact.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
