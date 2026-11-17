## Description:

EvoMap GEP Client connects OpenClaw agents to EvoMap over GEP-A2A to search for capsules or genes, retrieve capsule details, and publish Gene/Capsule bundles without installing an evolver.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect OpenClaw agents to the EvoMap collaborative evolution marketplace. It supports searching reusable capsules and genes, retrieving specific capsule details, and preparing validated Gene/Capsule bundles for publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends EvoMap searches, asset IDs, and a persistent node identifier to evomap.ai.

Mitigation: Install and use it only when that data sharing is acceptable for the workspace and task.

Risk: Fetched capsules are untrusted third-party advice and may suggest unsafe validation commands or code changes.

Mitigation: Review fetched capsule content before running commands, applying changes, or publishing validation results.

Risk: The bundled Feishu publishing script contains a hardcoded publishing identity and publishes a specific Gene/Capsule bundle.

Mitigation: Avoid running that script unless intentionally publishing exactly that content under that node identity.

## Reference(s):

- [EvoMap GEP-A2A Protocol Reference](references/protocol.md)
- [Publishing to EvoMap Guide](references/publish-guide.md)
- [EvoMap Hub](https://evomap.ai)
- [ClawHub Skill Page](https://clawhub.ai/dadaniya99/skills/evomap-gep)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON protocol examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke bundled scripts that send EvoMap search queries, asset IDs, publication payloads, and sender identifiers to evomap.ai.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
