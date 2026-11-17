## Description:

Interact with the arXiv Crawler API to fetch papers, read reviews, submit comments, search papers, and import papers from arXiv URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxrys](https://clawhub.ai/user/zxrys)

### License/Terms of Use:


## Use Case:

External users and developers use this skill for non-sensitive arXiv paper discovery and review workflows: listing papers, viewing details and comments, searching by title, submitting comments, and importing arXiv URLs through the configured API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default API endpoint uses unencrypted HTTP, which can expose API keys and submitted review content in transit.

Mitigation: Use the skill only for non-sensitive paper searches and comments until the API base URL is changed to HTTPS and API keys are protected.

Risk: Any API key already used with the default HTTP endpoint may have been exposed.

Mitigation: Rotate any key previously used through that endpoint before continuing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxrys/skills/arxiv-paper-reviews)
- [Configured arXiv Crawler API endpoint](http://weakaccept.top:8000/)
- [arXiv paper URL example](https://arxiv.org/abs/2602.09012)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command-line client output may include paper metadata, abstracts, comments, import status, and HTTP error text.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
