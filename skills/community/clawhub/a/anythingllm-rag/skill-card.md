## Description:

Query local documents via AnythingLLM RAG when a user asks about private or local documents, uploaded files, or their knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianmaomao](https://clawhub.ai/user/tianmaomao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to query, list, and upload documents through a local AnythingLLM RAG workspace, then present answers with source citations when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an embedded API key in the skill.

Mitigation: Remove and rotate the embedded key before use, and require users to provide their own AnythingLLM API token through environment configuration.

Risk: The security evidence reports a reachable shell-injection flaw in the script's curl construction.

Mitigation: Review and replace eval-based command construction before installing or running the skill.

Risk: The skill uploads and queries private documents through a local AnythingLLM instance.

Mitigation: Use only a trusted AnythingLLM endpoint and confirm URL, transport security, and storage behavior before uploading sensitive documents.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query responses may include textResponse and sources from the AnythingLLM workspace.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
