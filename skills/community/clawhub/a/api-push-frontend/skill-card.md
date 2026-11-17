## Description:

Pushes backend API interface definitions to a frontend data interface platform for API documentation synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowzhouj](https://clawhub.ai/user/snowzhouj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and backend engineers use this skill to prepare, validate, and push backend API definitions to a frontend interface documentation platform. It supports JSON, Swagger/OpenAPI, and related backend interface descriptions for synchronization between backend and frontend teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API definitions may contain sensitive internal metadata and are uploaded to a fixed external service.

Mitigation: Use the skill only with an approved destination service, and review and redact API definitions before upload.

Risk: Saved push history may contain raw response data that is sensitive if loaded by agents or committed to source control.

Mitigation: Remove, relocate, or sanitize push-history records before sharing the skill or committing generated history.

Risk: The artifact includes an unused shell-execution helper.

Mitigation: Review the script before deployment and avoid enabling or extending shell execution paths unless they are explicitly required and controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snowzhouj/skills/api-push-frontend)
- [Frontend API platform documentation](references/frontend-api-docs.md)
- [API definition standard](references/api-definition-standard.md)
- [Push history record](references/push-history.md)
- [Frontend API upload endpoint](https://jffe.techgp.cn/md/api/uploadV4)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls, files]

**Output Format:** [Markdown guidance with JSON payloads, Python command examples, API calls, and push-history entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send API metadata to a fixed external service and append raw push responses to a Markdown history file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
