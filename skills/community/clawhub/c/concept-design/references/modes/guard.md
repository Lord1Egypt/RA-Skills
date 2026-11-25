# Maintain specifications

For backfill, a path identifies code to inspect; a description proposes behavior.
Without a backfill target, discover candidates only.

| Mode | Work |
| --- | --- |
| `audit` | Read-only coverage and proposed repair plan below |
| `concept` / `sync` | [Reconstruct specifications](guard/reconstruct.md) |
| `drift` | [Read-only contract comparison](guard/drift.md) |
| `pipeline` | [Pipeline specification](guard/pipeline.md) |
| `map` | [Concept and Synchronization Diagram](../tool-diagram.md#usage): generate one ARCHITECTURE.md from CONCEPT/SYNCS in the [tool encoding](../tool-encoding.md) |
| `rules` | [Align project rules](guard/project-rules.md) |

- **Ownership**: colocate CONCEPT and concept-owned PIPELINE with their concept; put cross-concept pipelines in composition. Colocate one SYNCS with each business rule group; index all groups without duplicate rules.
- **Maintenance**: after authorized specification edits, update indexes and regenerate the diagram from content. Preserve human notes and confirmed legacy behavior. The diagram MUST NOT become an authoritative contract.

## Audit

Audit MUST NOT execute repairs.

- **Read**: scoped conventions, PRD/staged indexes, specifications, entries, state/schema/migrations, tests, manifests, and maps. Skip dependency/generated/build trees; include single-file core modules. Inspect ancestor content before claiming coverage.
- **Classify**: mark each module/flow as covered, staged, missing, support code, or unverified, naming its authoritative file and actual coverage, or evidence/skip gap. Report calls between concepts as coupling even through public APIs.
- **Report**: scope, measured counts, candidate locations, broken links, and migration work. Coverage percentages MUST enumerate their denominator.
- **Propose backfill**: order by actual code dependencies; handle cycles together and flag boundary problems. Each proposed command names mode, path, evidence, artifact, and prerequisite; sort paths within a batch.
