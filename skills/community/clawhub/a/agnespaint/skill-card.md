## Description:

Agnes画影 helps an agent generate images or videos through the Agnes AI API using the AGNES_API_KEY environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn natural-language prompts into Agnes AI image or video generation requests, confirm prompts before submission, poll video jobs, and return generated media URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisting AGNES_API_KEY in shell startup files can broaden credential exposure.

Mitigation: Prefer scoped secrets or temporary environment variables, and only persist credentials in dotfiles after explicit user acceptance.

Risk: The skill can make authenticated requests to third-party image and video generation endpoints.

Mitigation: Confirm prompts before API submission, avoid exposing API keys in logs or prompts, and respect the documented video polling interval.

## Reference(s):

- [Agnes AI Platform](https://platform.agnes-ai.com/)
- [Agnes AI API Base](https://apihub.agnes-ai.com/v1)
- [API reference](artifact/modules/01-api-reference.md)
- [ClawHub skill page](https://clawhub.ai/fslong520/skills/agnespaint)
- [Publisher profile](https://clawhub.ai/user/fslong520)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown with inline shell commands and generated media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl requests, environment-variable setup steps, video polling status, and final image or video URLs.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
