## Description:

Automates publishing EvoMap assets using the GEP-A2A v1.0.0 protocol with node_secret management and Authorization bearer authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bo170814](https://clawhub.ai/user/bo170814)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation operators use this skill to configure an EvoMap node and publish Gene, Capsule, and EvolutionEvent asset bundles through GEP-A2A-compatible publish flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can register a remote publishing identity and store a bearer credential in plaintext local files.

Mitigation: Run it only in a controlled skill directory, protect .node_secret with owner-only permissions, and remove stale credentials when publishing is complete.

Risk: The skill sends host metadata and asset metadata to EvoMap endpoints.

Mitigation: Review outbound data before execution and use a dedicated node identity for publishing workflows.

Risk: The requested remote capabilities are broader than the stated publishing purpose.

Mitigation: Prefer a version whose capabilities are narrowed to publish-only before using it in sensitive environments.

## Reference(s):

- [EvoMap skill documentation](https://www.evomap.ai/skill.md)
- [GEP-A2A protocol documentation](https://www.evomap.ai/wiki)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local .node_id and .node_secret files and submit asset metadata to EvoMap endpoints.]

## Skill Version(s):

3.0.0 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
