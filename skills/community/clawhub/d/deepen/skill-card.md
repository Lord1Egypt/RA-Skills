## Description:

Point at any topic to build a compounding, domain-general expertise knowledge base: a high-fidelity source corpus, track-record-weighted experts, reconciled falsifiable stances, failure modes, benchmarks, and a proven playbook - built as evergreen notes a future agent can load and reason over.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianhkerr](https://clawhub.ai/user/brianhkerr)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to build and maintain a durable research knowledge base for deeply mastering a topic, including source digests, expert weighting, disagreements, failure modes, benchmarks, and a reusable playbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a durable local research notebook, which can persist sensitive or unwanted material if pointed at the wrong directory.

Mitigation: Choose the knowledge-base directory deliberately before running it, and avoid private vaults unless persistent storage there is intended.

Risk: Research connector usage can expose provider credentials if keys are placed in command arguments or saved notes.

Mitigation: Use provider authentication patterns that keep API keys out of command arguments and generated knowledge-base files.

Risk: Broad research synthesis can add incorrect or misleading claims to a reusable knowledge base.

Mitigation: Review source digests, citations, confidence labels, and contested stances before relying on the generated notes for important work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brianhkerr/skills/deepen)
- [Connector recipes](CONNECTORS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes and concise status summaries, with optional shell command snippets for research connectors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a persistent local knowledge base under a resolved topic directory when a writable filesystem is available.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
