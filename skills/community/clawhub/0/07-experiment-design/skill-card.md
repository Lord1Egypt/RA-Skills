## Description:

Use when the user has a method idea or Committed Method Design and reads papers to design tasks, datasets, baselines, metrics, ablations, human evaluation, user studies, or a claim-to-evidence experiment plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snake-fan](https://clawhub.ai/user/snake-fan)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, paper authors, and research engineers use this skill to turn a stable method or research question into a structured experiment plan with claim-evidence mapping, baselines, metrics, ablations, controls, and reviewer-facing failure interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads relevant local research files while preparing experiment-design artifacts.

Mitigation: Review the workspace root and source artifacts before use, and provide only research materials intended for the agent to inspect.

Risk: The skill writes multiple Markdown planning files that could be mistaken for final experimental evidence.

Mitigation: Use the built-in review gates and provisional-status markers before treating an experiment plan as final.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/07-experiment-design)
- [ClawHub skill page](https://clawhub.ai/snake-fan/skills/07-experiment-design)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown planning artifacts and concise decision packets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local experiment-design artifacts under a workspace root and keeps provisional work clearly marked until review gates pass.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
