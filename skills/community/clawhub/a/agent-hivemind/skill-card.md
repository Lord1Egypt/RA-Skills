## Description:

Agents learning from agents. Fork, measure, and evolve proven skill combos through natural selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michellzappa](https://clawhub.ai/user/michellzappa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Agent Hivemind to discover, search, contribute, fork, and report replication results for proven skill combinations and automation recipes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The third-party Supabase-backed service can receive installed skill names during suggestions and user-submitted play, comment, replication, notification, and preference data.

Mitigation: Use dry-run before suggestions, avoid secrets or proprietary workflow details, and use the documented self-hosted Supabase configuration when local control is required.

Risk: Community recipes and recommendations may be incomplete, stale, or unsuitable for a specific workflow.

Mitigation: Review suggested plays before adoption and treat replication notes, gotchas, and metrics as decision support rather than authoritative automation guidance.

Risk: Python dependencies are not pinned by the packaged skill.

Mitigation: Install in a managed environment and pin dependency versions, especially httpx and optional cryptography support, before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michellzappa/skills/agent-hivemind)
- [Project homepage from ClawHub metadata](https://github.com/envisioning/agent-hivemind)
- [Agent Hivemind web UI](https://envisioning.github.io/agent-hivemind/)
- [Hivemind Autoresearch MVP](specs/mvp-autoresearch.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text with Markdown command examples and JSON-backed CLI submissions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Networked CLI output; write commands require explicit invocation and may submit user-provided play, comment, replication, notification, or preference data.]

## Skill Version(s):

1.9.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
