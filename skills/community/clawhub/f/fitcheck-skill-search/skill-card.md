## Description:

Find and retrieve available skills using keyword search, semantic search, or LLM-powered task matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[at6132](https://clawhub.ai/user/at6132)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to find relevant installed skills before loading them into an agent context. It supports keyword, semantic, and hybrid task matching over local skill metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local index may contain installed skill metadata and absolute skill paths.

Mitigation: Treat generated index and embedding cache files as local workspace data and avoid sharing them when paths or installed skill names are sensitive.

Risk: Search recommendations may overstate matching quality or return low-confidence candidates.

Mitigation: Use results as a candidate list, then inspect the matched SKILL.md before loading or executing another skill.

Risk: Documentation advertises AI-powered or BM25-style matching more strongly than the current local implementation supports.

Mitigation: Set user expectations that matching is heuristic and verify important recommendations manually.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/at6132/skills/fitcheck-skill-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text recommendation lists and Markdown usage guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations include scores or confidence labels and should be reviewed before loading or executing another skill.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
