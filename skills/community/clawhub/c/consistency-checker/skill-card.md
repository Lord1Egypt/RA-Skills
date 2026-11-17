## Description:

Checks novel chapters for consistency issues in character names, traits, timelines, locations, and relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

External writers, editors, and agent workflows use this skill to check Chinese novel project files for inconsistent character naming, traits, timelines, locations, relationships, seasons, and ages before publication or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The LLM variant can send manuscript excerpts and character data to DashScope.

Mitigation: Use the documented local checker for private or unpublished writing, and run the LLM variant only after explicit opt-in and review of what content will be sent.

Risk: The release is marked suspicious by the authoritative security scan because the remote LLM behavior is under-disclosed.

Mitigation: Review the scripts before installation, pin dependencies in an isolated environment, and modify or remove the LLM script if remote processing is not required.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style consistency reports, terminal tables, and optional JSON issue reports from the LLM variant.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local checker reads project files from characters/ and chapters/ directories; the LLM variant can send summarized manuscript and character content to DashScope when explicitly run with DASHSCOPE_API_KEY.]

## Skill Version(s):

2.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
