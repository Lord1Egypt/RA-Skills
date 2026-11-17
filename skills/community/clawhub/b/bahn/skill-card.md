## Description:

Search Deutsche Bahn train connections using the bahn-cli tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobiasbischoff](https://clawhub.ai/user/tobiasbischoff)

### License/Terms of Use:


## Use Case:

Travel planners and agent users use this skill to search Deutsche Bahn connections between German stations, including departure and arrival times, platforms, duration, changes, stops, and train numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to install and run code from an unspecified local project path outside the reviewed skill package.

Mitigation: Use it only after verifying the local bahn-cli project and its dependencies; prefer a release that bundles the CLI or pins an official repository, commit, and lockfile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobiasbischoff/skills/bahn)
- [ClawHub publisher profile](https://clawhub.ai/user/tobiasbischoff)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and train connection text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Train connection details may include departure and arrival times, platforms, duration, changes, intermediate stops, and train numbers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
