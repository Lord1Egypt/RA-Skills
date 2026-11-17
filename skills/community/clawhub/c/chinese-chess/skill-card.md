## Description:

Directs an agent to generate a new Chinese chess (Xiangqi) game or improve an existing one using pre-built local source directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianzhenjiu](https://clawhub.ai/user/tianzhenjiu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when asking an agent to create a Chinese chess game or enhance an existing Chinese chess game experience. The skill routes the work to one of two local source-template directories based on that intent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to read and copy from unaudited absolute local directories.

Mitigation: Use it only when those directories are trusted and reviewed, and inspect generated changes before running them.

Risk: The referenced absolute source directories may not exist or may differ outside the publisher's environment.

Mitigation: Verify the source paths or replace them with trusted project-local templates before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianzhenjiu/skills/chinese-chess)

## Skill Output:

**Output Type(s):** [Code, Files, Guidance]

**Output Format:** [Project files with a concise Markdown summary of created or modified files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill selects one of two local source directories before generating or improving the target project.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
