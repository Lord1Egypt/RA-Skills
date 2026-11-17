## Description:

Apicheck helps agents construct API requests, generate curl commands and mock data, draft API documentation, and explain HTTP status codes and headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Apicheck to ask an agent for API request examples, curl commands, mock JSON data, endpoint documentation, and quick HTTP status or header explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags a purpose-mismatched workflow script that can write command arguments to persistent local history.

Mitigation: Review the package before installation, avoid passing secrets or tokens to its commands, and prefer installation after the publisher removes or clearly documents the extra workflow script and local logging.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/skills/apicheck)
- [BytesAgain Homepage](https://bytesagain.com)
- [API Tester Reference](artifact/tips.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated API examples, curl variants, mock JSON, API documentation, and HTTP/header explanations.]

## Skill Version(s):

2.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
