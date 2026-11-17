## Description:

Track your entire garden with structured memory for plants, zones, tasks, harvests, and climate-aware planning that compounds over seasons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use Garden to help an agent track plants, garden zones, activities, harvests, diagnosis notes, and season-aware planning in local garden memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Garden notes accumulate in a local ~/garden/ folder and may reflect user-specific garden context over time.

Mitigation: Install only when ongoing local garden memory is desired, keep storage local, and ask before writing outside ~/garden/.

Risk: Broad activation or auto-logging language could treat casual plant mentions as trackable garden activity.

Mitigation: During setup, choose direct-invocation mode when the user only wants Garden to activate on explicit requests.

## Reference(s):

- [Garden ClawHub listing](https://clawhub.ai/ivangdavila/skills/garden)
- [Garden homepage](https://clawic.com/skills/garden)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and updates local garden memory files when the user consents; no external APIs, telemetry, or network calls are described.]

## Skill Version(s):

1.1.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
