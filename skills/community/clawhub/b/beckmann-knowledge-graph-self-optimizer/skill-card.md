## Description:

Iterative self-optimization for knowledge graphs in 5 phases with 3 review gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthiasbeckmann987-spec](https://clawhub.ai/user/matthiasbeckmann987-spec)

### License/Terms of Use:

MIT

## Use Case:

Developers and knowledge-graph maintainers use this skill to guide a graph.json optimization cycle, create reviewable reports and subgraphs, build bridge relations, and merge validated updates back into the graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or unsanitized graph JSON could affect local browser tools or steer autonomous prompt phases.

Mitigation: Use trusted or sanitized graph files, avoid third-party graph JSON in the HTML overview tool, and review generated reports before approving workflow gates.

Risk: Merge and cleanup steps can alter the main knowledge graph.

Mitigation: Keep backups before merge or cleanup and review generated subgraph, relation, and merged graph files before replacing graph.json.

Risk: Graph content may be copied into generated output files and expose sensitive entity details.

Mitigation: Treat generated overview, split, report, subgraph, relation, and merged graph files as sensitive when source graph data is confidential.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/matthiasbeckmann987-spec/skills/beckmann-knowledge-graph-self-optimizer)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance, configuration]

**Output Format:** [Markdown guidance with generated text reports and JSON graph artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses explicit review gates before graph expansion, relation building, and final merge.]

## Skill Version(s):

1.1.0 (source: frontmatter, package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
