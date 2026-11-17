## Description:

Find Skills Combo helps agents decompose complex user requests and recommend skill combinations using maximum-quality and minimum-dependency strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloml0326](https://clawhub.ai/user/helloml0326)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to break multi-capability tasks into subtasks, search for relevant skills, and compare recommended skill portfolios. It is intended for planning skill combinations and producing install guidance for the selected strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recommend unpinned, unattended global installation of third-party skills.

Mitigation: Review each recommended skill's publisher, source, and contents before installation; prefer pinned versions and avoid global unattended installs unless deliberately required.

Risk: Recommendation output may be incomplete or misleading if candidate skill metadata is stale or weakly matched to the user's task.

Mitigation: Treat recommendations as planning guidance, verify the selected skills against the actual task requirements, and scan skills before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helloml0326/skills/find-skills-combo)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with tables and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation commands for recommended skills; review each command and selected skill before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
