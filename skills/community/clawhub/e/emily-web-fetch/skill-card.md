## Description:

Fetches static webpage content over HTTP or HTTPS and returns up to 5000 characters for analysis, summarization, or information extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emilyzhang01](https://clawhub.ai/user/emilyzhang01)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill when an assistant needs to retrieve static webpage content, then summarize, analyze, or extract information from the returned text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary caller-supplied HTTP or HTTPS URLs from the agent runtime, including local, private-network, or cloud metadata services.

Mitigation: Run it in a sandbox with network egress controls that block localhost, private networks, and cloud metadata endpoints.

Risk: Large or streaming responses may consume more resources than the advertised 5000-character return limit suggests.

Mitigation: Use request timeouts, response-size controls, and runtime resource limits when enabling outbound network access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/emilyzhang01/skills/emily-web-fetch)
- [Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or HTML excerpt returned as a string, with downstream assistant responses typically in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns at most 5000 characters from a static HTTP/HTTPS GET response; JavaScript-rendered content is not processed.]

## Skill Version(s):

1.0.5 (source: server release metadata; package.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
