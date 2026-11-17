## Description:

Run a Duolingo-like multi-topic learning system with AGENTS routing, lesson loops, streaks, and spaced review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External learners and agents use this skill to run short daily lessons across one or more topics, including placement, micro-challenges, progress tracking, streaks, and spaced review in a local ~/duolingo workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps persistent learning state, curricula, attempts, and review queues under ~/duolingo/.

Mitigation: Install it only when a persistent local learning workspace is desired, and review or remove that workspace before sharing machine state or backups.

Risk: Broad AGENTS routing examples could cause the skill to activate for more learning requests than intended.

Mitigation: Keep trigger topics specific, review the generated AGENTS snippet, and apply routing changes manually.

Risk: Topic names used directly in shell-based setup could create unsafe or invalid paths.

Mitigation: Use simple validated topic slugs with lowercase letters, numbers, and hyphens, and avoid passing raw topic names into shell commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/duolingo)
- [Skill Homepage](https://clawic.com/skills/duolingo)
- [Setup Flow](artifact/setup.md)
- [Filesystem Blueprint](artifact/blueprint.md)
- [Lesson Runtime Loop](artifact/lesson-loop.md)
- [Multi-Topic Retention Operations](artifact/retention-ops.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with interactive lesson prompts, setup commands, routing snippets, and local file templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates a local ~/duolingo workspace when the user asks the agent to bootstrap or run lessons.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
