## Description:

Pyramid multi-agent orchestration for OpenClaw: routes objectives from a CEO agent down through departments, services, and employees via sessions_send / sessions_spawn, collects and merges results, enforces handoff contracts, and writes the final deliverable back to the originating session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams using OpenClaw use this skill to coordinate multi-agent task execution across strategy, engineering, quality, and operations sessions, then merge delegated outputs into a final deliverable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate and spawn other OpenClaw sessions, so broad objectives can create excess delegation or unclear accountability.

Mitigation: Review the requested departments, delegated objectives, and spawned-session count during use; the artifact specifies a maximum of 20 spawned sessions per orchestration run.

Risk: Merged outputs from multiple sessions may be incomplete when departments time out or report blockers.

Mitigation: Use the documented convergence behavior: accept partial results only with explicit timeout or blocker status, then require human validation before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/romainsantoli-web/skills/firm-orchestration)
- [ClawHub Publisher Profile](https://clawhub.ai/user/romainsantoli-web)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or task-specific deliverable assembled from child session results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include run summaries, department statuses, blockers, and a required human-validation disclaimer.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
