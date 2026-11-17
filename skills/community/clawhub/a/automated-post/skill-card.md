## Description:

Automated Post coordinates copywriting and image-generation agents to prepare illustrated posts, publish them after confirmation, and archive the content and images to Feishu documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yifeiwang1981](https://clawhub.ai/user/yifeiwang1981)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators use this skill to create image-and-text posts through either step-by-step confirmation or a mostly automated workflow with final approval. It also supports post-publication archival of copy and images into daily Feishu documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content and archive materials to an external Feishu workspace.

Mitigation: Require final human approval before publishing, and confirm or disable Feishu archival when content should not be stored externally.

Risk: Topics, generated copy, tags, prompts, document content, and file paths may be unsafe inputs for command execution.

Mitigation: Treat those values as untrusted and use argument-array APIs or structured tool calls instead of shell string substitution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces posting workflow steps, agent prompts, command examples, timing summaries, and archival guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
