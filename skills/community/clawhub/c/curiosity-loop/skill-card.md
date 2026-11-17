## Description:

Intrinsic curiosity-driven continuous learning: detect gaps between expected and actual results, treat them as curiosity signals, and update skills accordingly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guiguid](https://clawhub.ai/user/guiguid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn repeated gaps, failed outcomes, or missing knowledge into structured research, integration, and curriculum-building cycles. It is intended for agents that should maintain learning records, propose skill updates, and diversify problem-solving approaches over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to keep local learning records and may propose persistent memory writes or skill changes.

Mitigation: Require explicit confirmation before memory writes, skill patching, or skill creation, and define a retention policy for local delta records.

Risk: Periodic source scanning can introduce untrusted external content into the learning loop.

Mitigation: Restrict scan sources to trusted allowlists and treat all fetched content as untrusted until reviewed.

Risk: Scheduled scanning may persist or update learning state without adequate operator oversight.

Mitigation: Avoid cron or other unattended scheduling until the storage path, review workflow, and retention policy are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guiguid/skills/curiosity-loop)
- [Key Concepts — Flowers Lab, INRIA](references/flowers-lab-concepts.md)
- [Flowers Lab, INRIA](https://www.robots.org/flowers-lab/)
- [Flowers INRIA YouTube channel](https://www.youtube.com/channel/UCrBNVs3u3mwlRsm2v3EKuXA)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local delta records, memory updates, skill patches, new skills, and optional source-scanning commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
