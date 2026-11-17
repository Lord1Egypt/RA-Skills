## Description:

Guides AI teams, RAG maintainers, and knowledge-base operators through a five-step workflow for turning raw materials into verified feed packs with source, applicability, and governing-standard checks for figures, limits, and clauses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and knowledge operations teams use this skill to register, verify, rewrite, partition, and receipt raw source material before adding it to knowledge bases, RAG corpora, or multi-agent feed packs. It emphasizes official-source verification, sensitive-data screening, and marking unsupported facts as pending verification rather than fabricating missing details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags the workflow for Review because broad raw agent-history inspection can expose sensitive or unrelated data.

Mitigation: Use task-scoped, redacted exports for verification and apply the skill's sensitive-data scan before adding material to any public or shared knowledge area.

Risk: The security review flags unattributed third-party content ingestion as a concern.

Mitigation: Preserve source and provenance metadata for third-party material, rewrite only public objective facts, and require explicit approval before cloud ingestion, publication, or external sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/feeding-workflow)
- [喂料包 · 模板（v1.0）](references/喂料包模板.md)
- [喂料纪律（全局，任何喂料行为必须遵守）](references/喂料纪律.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance, feed-pack templates, ledger notes, and verification receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only workflow; no executable code, dependency installation, automatic network calls, or automatic file operations are included in the release evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
