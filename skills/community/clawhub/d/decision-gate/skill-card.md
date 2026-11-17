## Description:

Tamper-evident decision logging for AI agents that commits a hash-chained local record before high-stakes actions run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vaahl-dev](https://clawhub.ai/user/vaahl-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a required pre-action decision record before irreversible or high-stakes actions such as transfers, releases, deployments, configuration changes, or transaction signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local hash chain is not independently tamper-proof against a party that can edit the log file.

Mitigation: Use independent signing, timestamping, or reviewed third-party verification for high-stakes compliance, financial, or irreversible workflows.

Risk: A pre-action record can still be misleading if the logged evidence classes or source snapshots do not reflect what was actually checked.

Mitigation: Log bounded evidence classes and versioned source_refs, and review the decision schema so action legality depends on the committed claim content.

Risk: The separate premium verifier is referenced by the skill but is not part of this artifact.

Mitigation: Review the verifier package separately before depending on external verification receipts.

## Reference(s):

- [Decision Gate on ClawHub](https://clawhub.ai/vaahl-dev/skills/decision-gate)
- [Decision Gate homepage](https://soulscore.xyz/decision-gate?src=clawhub)
- [Zero Trust for AI Agents analysis](https://mnemehq.com/insights/zero-trust-for-ai-agents-architectural-governance/)
- [soulscore methodology](https://soulscore.xyz/methodology?src=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python usage examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JSONL decision and outcome records when its Python helper is used]

## Skill Version(s):

1.4.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
