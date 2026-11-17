## Description:

Save up to 90% on Token costs. One agent explores, all agents benefit. Cloud-cached workflows with zero inference cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ainclaw](https://clawhub.ai/user/ainclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use ClawMind to reuse cached browser workflow patterns before invoking LLM exploration, and to contribute successful session traces back to the shared workflow cache when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser intent, URL, session identifiers, DOM hashes, and sanitized workflow traces may be sent to the configured cloud service.

Mitigation: Use the skill only where sharing those workflow signals is acceptable, verify the endpoint and retention policy, and disable auto_contribute for private, regulated, internal, or confidential workflows.

Risk: Matched workflows returned from the cloud may be replayed with limited consent and verification controls.

Mitigation: Restrict use on sensitive sites and review the workflow validation controls before allowing cached workflows to execute automatically.

## Reference(s):

- [ClawMind ClawHub listing](https://clawhub.ai/ainclaw/skills/ainclaw-mind)
- [Publisher profile](https://clawhub.ai/user/ainclaw)
- [Configured cloud API endpoint](https://api.workflowcache.dev)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [Agent responses and replayed Lobster workflow commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May pass through to normal agent handling when no cached workflow is available or execution fails.]

## Skill Version(s):

1.0.5 (source: evidence.release.version, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
