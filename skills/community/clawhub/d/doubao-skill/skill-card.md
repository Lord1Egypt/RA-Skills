## Description:

Uses the ByteDance/Doubao Volcengine ARK API for text-to-image generation, image editing, text-to-video generation, and task status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenkangwei](https://clawhub.ai/user/wenkangwei)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to call Doubao/Volcengine ARK media generation APIs from an agent workflow, including image generation, authorized image editing, video generation, and task status lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and image URLs to Volcengine/Doubao APIs.

Mitigation: Only submit prompts and image URLs that the user is allowed to share with that external service.

Risk: The documentation normalizes watermark and logo removal examples.

Mitigation: Use image editing only on content where the user has explicit authorization for that edit.

Risk: Setup guidance includes unsafe installation or shell-sourcing patterns.

Mitigation: Install in an isolated virtual environment, avoid the npm install path, and do not source untrusted shell files such as ~/.basic.

Risk: ARK_API_KEY is required for operation and could be exposed if handled casually.

Mitigation: Set ARK_API_KEY directly through environment variables or a trusted secret manager and avoid committing or printing credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wenkangwei/skills/doubao-skill)
- [Volcengine ARK Documentation](https://www.volcengine.com/docs/82379)
- [Doubao API Console](https://console.volcengine.com/ark)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Quick Start Guide](references/README.md)
- [Detailed Skill Documentation](references/SKILL.md)
- [Integration Guide](references/INTEGRATION_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, API results]

**Output Format:** [JSON responses and Markdown guidance with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns media URLs, task identifiers, task status, prompts, and error messages from Volcengine ARK API calls.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact files also mention 1.0.0 and 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
