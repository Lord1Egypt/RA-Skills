## Description:

Collect comments from a known Facebook post URL. Do not use for the post body, personal profiles, or events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify collection jobs for comments on a known Facebook post URL, monitor the asynchronous task, and return the collected result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill submits Facebook URLs and collection settings to Dataify, creating an external collection job.

Mitigation: Use it only when the user intends to submit a Dataify job for the specified Facebook post URL and understands that Dataify will process the request.

Risk: The skill uses a Dataify API TOKEN that may be saved in the local environment.

Mitigation: Keep the token out of chat and logs, verify only whether DATAIFY_API_TOKEN is present, and avoid printing or persisting credentials without user confirmation.

Risk: Security evidence notes loose target validation and an adjacent unreviewed runtime import that could see the API token.

Mitigation: Review the helper script and adjacent task runtime before installation or execution, and run it only in an environment where token exposure risk is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-facebook-comment-by-url)
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill)
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON task/result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a task identifier, task status, normalized collection parameters, or final collected JSON results.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
