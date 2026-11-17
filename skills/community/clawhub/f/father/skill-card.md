## Description:

Father.skill helps users preserve and organize memories of their father, including life lessons, work ethic, problem-solving patterns, and unspoken expressions of care.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to capture memories, lessons, personality details, and complicated or grief-sensitive reflections about their father in a private local archive. It is intended for legacy preservation and understanding, not daily parenting coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store sensitive family memories, grief details, or relationship history in local files.

Mitigation: Treat the ~/.father-skill/ folder as private data, restrict local access, and delete the folder when the archive is no longer wanted.

Risk: Conversational responses about what a father might say could be emotionally sensitive or feel more certain than the recorded memories support.

Mitigation: Ground responses in user-supplied memories, preserve uncertainty, and avoid fabricating details that were not recorded.

## Reference(s):

- [Understanding Your Father - A Guide](references/understanding-guide.md)
- [Father Profile Template](templates/FATHER-PROFILE.md)
- [ClawHub Skill Page](https://clawhub.ai/realteamprinz/skills/father)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSONL, Guidance, Configuration]

**Output Format:** [Markdown and JSONL entries with conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local files are described under ~/.father-skill/; no external transmission is described in the evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
