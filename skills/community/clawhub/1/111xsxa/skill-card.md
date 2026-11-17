## Description:

Helps an agent use UAPI's GET /ai/translate/languages endpoint to retrieve supported AI translation languages, translation style options, context options, and performance information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill when a request specifically needs UAPI AI translation configuration or supported-language lookup through GET /ai/translate/languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms may cause the skill to be selected for general language or translation requests.

Mitigation: Confirm the user specifically needs UAPI AI translation language or configuration lookup before applying this skill.

Risk: Authenticated use may rely on a UAPI key for stable or rate-limit-resilient calls.

Mitigation: Only provide a UAPI key when authenticated access is intentional and needed for the request.

Risk: Anonymous or public use can hit quota or rate-limit responses.

Mitigation: If UAPI returns a quota or 429 response, suggest registering for a UAPI account and retrying with a free UAPI key.

## Reference(s):

- [Quick Start](references/quick-start.md)
- [AI Translate Languages Operation](references/operations/get-ai-translate-languages.md)
- [Translate Resource](references/resources/Translate.md)
- [UAPI API Base](https://uapis.cn/api/v1)
- [UAPI](https://uapis.cn)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint, authentication, parameter, and response-code details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The wrapped endpoint has no explicit parameters; guidance may recommend a UAPI key for authenticated or rate-limit-resilient use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
