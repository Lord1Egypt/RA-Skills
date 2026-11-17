## Description:

Provides a direct link to download Chinese translations of arXiv papers using an arXiv ID or arXiv URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyan](https://clawhub.ai/user/skyan)

### License/Terms of Use:


## Use Case:

Developers, researchers, and other agent users can use this skill to turn an arXiv paper ID or URL into a direct link for an external Chinese translation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends users to an external translation service.

Mitigation: Review the generated hjfy.top link before opening it, especially when the input came from an untrusted source.

Risk: Invalid or unexpected input may be echoed into the generated URL.

Mitigation: Prefer validated arXiv IDs or canonical arXiv URLs, and reject malformed inputs before using generated links in higher-trust workflows.

## Reference(s):

- [arXiv](https://arxiv.org/)
- [Chinese arXiv translation service](https://hjfy.top/arxiv/)
- [ClawHub skill page](https://clawhub.ai/skyan/skills/arxiv-translate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style terminal text with a direct URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated link uses the extracted arXiv ID and points users to an external on-demand translation service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
