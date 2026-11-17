## Description:

Argus helps agents preserve durable conversation and work context by routing decisions, evidence, commitments, preferences, and project state to canonical Git-backed records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and repository-aware agents use Argus to checkpoint durable decisions, evidence, commitments, preferences, and project state into existing canonical archives after meaningful milestones. It is intended for controlled local knowledge work where the user wants selected context preserved without archiving full conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist selected durable decisions, commitments, preferences, evidence, and project state into local archives.

Mitigation: Install it only in workspaces where that persistence is desired, review the default checkpoint prompt before broad use, and require confirmation or repository rules for sensitive personal, business, legal, financial, or budget records.

Risk: Private archive paths, backlinks, or local registry details could be exposed if copied into public outputs.

Mitigation: Keep registries private, follow the documented public privacy exception, and use public URLs in public artifacts while preserving private provenance only in private records.

Risk: Commitments or resource records could be duplicated into the wrong durable surface.

Mitigation: Route commitments through the configured commitment system, use the configured budget authority for resource records, and ask rather than guess when archive ownership is ambiguous.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antreasantoniou/skills/argus-skill)
- [Home-anchor and backlink contract](references/backlink-contract.md)
- [Recommended agent checkpoint](references/checkpoint-prompt.md)
- [Routing durable context](references/routing.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file-editing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead the agent to update selected local Git-backed archive records when checkpointing is authorized.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
