## Description:

Extracts keywords, key phrases, and main topics from text for SEO, content tagging, and indexing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Developers and content teams use this skill to analyze supplied text and generate keyword, phrase, and topic metadata for SEO, tagging, indexing, and content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP mode can expose an unauthenticated OpenAI-backed HTTP endpoint using the operator's API key.

Mitigation: Bind HTTP mode to localhost or put it behind authentication, and use a restricted OpenAI key with spending limits.

Risk: Input text may be sent to OpenAI when the remote backend is used.

Mitigation: Use only non-sensitive text unless organizational policy permits sending that content to OpenAI, or run an approved local backend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-keyword-extract)
- [Publisher profile](https://clawhub.ai/user/aronchick)
- [Artifact README](artifact/README.md)
- [Artifact skill metadata](artifact/skill.yaml)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands]

**Output Format:** [JSON object containing keywords, phrases, topics, keyword_count, and metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts text input and an optional max_keywords value; CLI mode writes JSON to stdout and MCP mode returns a synchronous response.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
