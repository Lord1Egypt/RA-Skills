## Description:

Queries repository information through DeepWiki MCP, including answers to questions, documentation structure, and documentation contents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoxj](https://clawhub.ai/user/autoxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to ask DeepWiki questions about a repository, inspect its documentation structure, or retrieve documentation contents for a selected topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command templates that interpolate repository names, questions, or topics can lead to unintended local command execution when copied into a shell with untrusted text.

Mitigation: Invoke the script with a shell-free argument array when possible, and use only repository, question, and topic text that has been reviewed for the target environment.

Risk: The @file question option can send local file contents to DeepWiki, including secrets or private notes if used carelessly.

Mitigation: Avoid @file unless the file was intentionally prepared for external submission and contains no credentials, private source, or internal notes.

Risk: Repository identifiers, questions, and topics are submitted to DeepWiki for processing.

Mitigation: Use this skill only for repositories and prompts that are appropriate to send to DeepWiki.

## Reference(s):

- [DeepWiki MCP endpoint](https://mcp.deepwiki.com/mcp)
- [DeepWiki Ask release page](https://clawhub.ai/autoxj/skills/deepwiki-ask)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON with text result fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on DeepWiki indexing, network availability, configured timeout, and retry settings.]

## Skill Version(s):

1.1.0 (source: server release evidence and artifact history, released 2026-03-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
