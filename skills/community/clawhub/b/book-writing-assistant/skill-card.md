## Description:

A conversational OpenClaw skill for book authors that combines project organization with creative writing support across fiction and nonfiction projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and authors use this skill to organize book projects, track characters, plot or argument threads, chapter outlines, research notes, world-building, continuity, and writing progress. It also helps brainstorm ideas, draft passages, outline nonfiction arguments, and work through writer's block.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local book-data.json record can contain sensitive unpublished manuscript details, research notes, and continuity data.

Mitigation: Install only when local persistence is desired, and review or delete the stored project file according to the writer's privacy needs.

Risk: Drafted prose, continuity flags, and writing suggestions may be incomplete or misaligned with the author's intent.

Mitigation: Treat generated material as editorial assistance and review important manuscript decisions before incorporating them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chris/skills/book-writing-assistant)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Conversational Markdown responses with structured project records in local JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local book-data.json project data when the host agent supports skill data persistence.]

## Skill Version(s):

1.0.1 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
