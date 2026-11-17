## Description:

Visualize the current context window usage by estimating token use across the system prompt, tools, workspace files, messages, and free space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[furukama](https://clawhub.ai/user/furukama)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect how much of the current context window is occupied and which components contribute to token use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects local workspace and memory files to estimate token usage, which may expose sensitive local file names or content-derived estimates in the response.

Mitigation: Review before installing or running in workspaces whose memory directory may contain private notes or sensitive records, and use only where local inspection is acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with monospace charts and optional JSON from the bundled token-estimation script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token counts are estimates based on approximately four characters per token and local workspace inspection.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
