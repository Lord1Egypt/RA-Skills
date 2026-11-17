## Description:

Run evidence-backed multi-agent debates (A/B/Opponent3/Judge) with 20-40 rounds, loophole analysis, and universal actionable lesson extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kdylan1010-alt](https://clawhub.ai/user/kdylan1010-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run structured multi-agent debates that test claims with evidence, identify loopholes, and extract measurable lessons that transfer across domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow writes debate files on the Desktop and appends lessons to a Desktop notes file.

Mitigation: Confirm the output location before running, or ask the agent to use a project-specific directory when Desktop writes are not desired.

Risk: Debate outputs and generalized lessons can be misleading if openings lack evidence or lessons are overgeneralized.

Mitigation: Require Claim, Evidence, and Source for openings, then apply the judge continuation check and universal lesson quality gate before reusing lessons.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kdylan1010-alt/skills/debate-learning-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown debate files, daily index, and appended Markdown lessons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates topic and index files under ~/Desktop/debate and appends lessons to ~/Desktop/lessons.md unless the user chooses another location.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
