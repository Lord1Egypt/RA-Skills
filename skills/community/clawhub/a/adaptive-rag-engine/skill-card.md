## Description:

Adaptive RAG Engine helps agents decide when and how to retrieve memory, pre-filter capsule indexes, evaluate retrieval quality with CRAG-style checks, and verify answers before generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luaqnyin](https://clawhub.ai/user/luaqnyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add adaptive retrieval behavior for complex questions, memory search, capsule pre-filtering, retrieval quality evaluation, and answer verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can index private memory content into a plaintext local capsule index.

Mitigation: Use it only in workspaces where the memory folder contents are appropriate to index, and review or remove sensitive notes before rebuilding the capsule index.

Risk: The skill relies on local protocol files that may shape agent retrieval behavior.

Mitigation: Review and control the referenced protocol file before enabling the skill, especially in shared or untrusted workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luaqnyin/skills/adaptive-rag-engine)
- [Publisher profile](https://clawhub.ai/user/luaqnyin)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, json]

**Output Format:** [Markdown guidance with bash commands and JSON or plaintext evaluation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or refresh a plaintext local capsule index and may classify retrieval results by score and recommended action.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
