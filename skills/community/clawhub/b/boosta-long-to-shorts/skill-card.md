## Description:

Create, monitor, and troubleshoot Boosta API video-processing jobs from natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundevmode](https://clawhub.ai/user/hundevmode)

### License/Terms of Use:

MIT

## Use Case:

Creators, agencies, developers, and automation teams use this skill to submit long-form video URLs to Boosta, monitor asynchronous processing jobs, and return generated short-clip URLs with clear status and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends submitted video URLs to the external Boosta API for processing.

Mitigation: Submit only video URLs that the user is allowed to share with Boosta.

Risk: The skill requires a Boosta API key and uses it for authenticated API requests.

Mitigation: Store BOOSTA_API_KEY as an environment variable and avoid exposing it in logs, prompts, or command output.

Risk: Unpinned install examples can resolve to changing upstream code.

Mitigation: Prefer the ClawHub package or a pinned commit or release before installation.

## Reference(s):

- [Boosta homepage](https://boosta.pro)
- [Boosta API getting started](https://docs.boosta.pro/api/getting-started)
- [Boosta API authentication](https://docs.boosta.pro/api/authentication)
- [Boosta API endpoints](https://docs.boosta.pro/api/endpoints)
- [Boosta API video types](https://docs.boosta.pro/api/video-types)
- [Boosta API errors](https://docs.boosta.pro/api/errors)
- [API reference](references/api-reference.md)
- [Error handling playbook](references/errors.md)
- [Video type selection](references/video-types.md)
- [ClawHub skill page](https://clawhub.ai/hundevmode/skills/boosta-long-to-shorts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include job IDs, job status, progress details, clip URLs, usage summaries, and retry or troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
