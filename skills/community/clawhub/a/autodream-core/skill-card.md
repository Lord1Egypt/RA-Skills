## Description:

Universal Memory Consolidation Engine - adapter-based cross-platform memory organization that can deduplicate, merge, and prune stale memory entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigkingcn](https://clawhub.ai/user/bigkingcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to consolidate long-running agent memory, including OpenClaw MEMORY.md files and memory directories. It supports adapter-based memory scanning, session signal gathering, duplicate merging, stale entry pruning, and configuration for custom platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read OpenClaw memory and session files.

Mitigation: Use it first in a backed-up or test workspace and only grant access to workspaces where memory and session contents are acceptable to process.

Risk: The skill can rewrite persistent MEMORY.md content.

Mitigation: Back up MEMORY.md and review proposed or resulting memory changes before relying on the rewritten file.

Risk: The skill can write local analytics logs when analytics are enabled.

Mitigation: Disable analytics when local usage logging is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigkingcn/skills/autodream-core)
- [Publisher profile](https://clawhub.ai/user/bigkingcn)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Files, Configuration, Guidance]

**Output Format:** [JSON result summaries with Markdown memory updates and local state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rewrite MEMORY.md and write local state or analytics files in the configured memory directory.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
