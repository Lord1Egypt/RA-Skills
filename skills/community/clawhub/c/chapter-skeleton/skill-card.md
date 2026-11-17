## Description:

Builds a retrieval-informed chapter-level outline skeleton from taxonomy and scope hints before stable H3 decomposition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-writing agents use this skill to create `outline/chapter_skeleton.yml` from `outline/taxonomy.yml` and optional `GOAL.md`, stabilizing chapter intent before H3 or subsection decomposition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle includes broader research-pipeline machinery beyond the stated chapter-skeleton task.

Mitigation: Review installed files before use and enable only the chapter-skeleton workflow needed for trusted workspaces.

Risk: The script path surface should be confined to workspace-relative inputs and the documented chapter skeleton output.

Mitigation: Run the script only against intended workspaces, keep inputs and outputs workspace-relative, and verify writes are limited to `outline/chapter_skeleton.yml`.

## Reference(s):

- [Chapter Skeleton Overview](artifact/references/overview.md)
- [Output Contract](artifact/assets/output_contract.json)
- [ClawHub Skill Page](https://clawhub.ai/willoscar/skills/chapter-skeleton)

## Skill Output:

**Output Type(s):** [configuration, shell commands, guidance]

**Output Format:** [YAML file with concise execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one chapter record per core topic with id, title, rationale, seed_topics, and target_h3_count; preserves existing non-placeholder output.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version is 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
