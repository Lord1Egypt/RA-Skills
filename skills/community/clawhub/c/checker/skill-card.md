## Description:

QA and peer review agent that reviews output from other agents before delivery and produces pre-delivery QA verdicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honeybee1130](https://clawhub.ai/user/honeybee1130)

### License/Terms of Use:


## Use Case:

External users and agent teams use Checker to review content, research, outreach, image, or other deliverables before delivery. It applies checklist-based QA and returns a binary approval or revision verdict with specific issues and required fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes QA verdict files and names a specific output path, which may not match every agent workspace.

Mitigation: Confirm the output location before use and adjust the workflow if the target workspace stores artifacts elsewhere.

Risk: The workflow assumes named peer agents and a specific team handoff pattern.

Mitigation: Map the review source and reporting destination to the local agent team before relying on the verdict workflow.

## Reference(s):

- [Checker ClawHub skill page](https://clawhub.ai/honeybee1130/skills/checker)
- [honeybee1130 publisher profile](https://clawhub.ai/user/honeybee1130)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Guidance]

**Output Format:** [Markdown QA review verdict saved as a file and summarized to the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review files follow the documented review-[source-agent]-[topic]-[YYYY-MM-DD].md naming pattern.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
