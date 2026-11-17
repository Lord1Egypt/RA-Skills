## Description:

Zero-vector AI memory engine with self-learning for local long-term memory, recall, and agent behavior adaptation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenroudeyu-collab](https://clawhub.ai/user/wenroudeyu-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add local memory storage, search, recall, and adaptive personalization to an assistant without requiring vector embeddings or cloud storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes private memory through local memory storage and retrieval.

Mitigation: Review before installing, use only on a trusted machine, avoid storing secrets, and delete or export memory data according to local policy.

Risk: A local API can expose memory data if bound beyond localhost or deployed without access controls.

Mitigation: Bind the API to localhost or add authentication before use on shared or networked systems.

Risk: Optional remote LLM or webhook settings can send memory data outside the device.

Mitigation: Enable remote LLM or webhook settings only after accepting the data-sharing implications for that endpoint.

Risk: The skill may change assistant identity, style, and long-term memory automatically.

Mitigation: Review behavior changes before deployment and monitor memory updates in workflows where consistency is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenroudeyu-collab/skills/cc-soul)
- [Project homepage](https://github.com/wenroudeyu-collab/cc-soul)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, code examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate through a local HTTP API and optional user-configured LLM endpoint.]

## Skill Version(s):

3.2.5 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
