## Description:

Stress-tests one selected Research Question Card to determine whether its problem is real, evidence-backed, externally grounded, safely motivated, and worth keeping as a research motivation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snake-fan](https://clawhub.ai/user/snake-fan)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and writing-focused agents use this skill to interrogate a single research question's problem motivation against local evidence, collect user responses, and produce a Problem Reality Check Report and summary artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads local research-question and field-map artifacts that may contain unpublished research notes.

Mitigation: Use it only in research workspaces you are comfortable sharing with the agent.

Risk: The workflow creates or updates review files under the selected workspace, so incorrect routing can affect the wrong card's check artifacts.

Mitigation: Confirm the selected Research Question Card and workspace root before allowing the check to proceed.

Risk: The skill produces motivation judgments and problem-validity guidance that can be wrong if local evidence is incomplete.

Mitigation: Review the transcript and final Problem Reality Check Report before relying on its verdict.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snake-fan/skills/03-problem-reality-check)
- [Server-Resolved GitHub Provenance](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/03-problem-reality-check)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown files and turn-by-turn text prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local research-question-check artifacts for one selected card per run.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
