## Description:

Ezviz restaurant inspection skill. Captures device images and sends to Ezviz AI for food safety analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezviz-open](https://clawhub.ai/user/ezviz-open)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to run Ezviz camera-based restaurant safety inspections, capture configured device images, and receive AI analysis results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can perform remote camera and intelligent-agent actions, including image capture and agent creation.

Mitigation: Review the skill before execution, use dedicated Ezviz credentials with minimal permissions, and test with non-production devices first.

Risk: Captured images are sent to Ezviz AI analysis services and may leave the local device environment.

Mitigation: Use only approved devices and scenes, confirm data-handling requirements before use, and avoid capturing sensitive areas or regulated data unless explicitly approved.

Risk: Access tokens are cached under /tmp/ezviz_global_token_cache, and the security guidance says not to rely on EZVIZ_TOKEN_CACHE=0 to prevent persistence in this version.

Mitigation: Avoid shared or multi-user hosts, clear the token cache after testing, and isolate runs until token caching behavior is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ezviz-open/skills/ezviz-open-restaurant-inspection)
- [Publisher profile](https://clawhub.ai/user/ezviz-open)
- [Ezviz Open API domain](https://open.ys7.com)
- [Ezviz AI analysis domain](https://aidialoggw.ys7.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Console text with JSON inspection results and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Ezviz credentials and device serials; performs remote camera capture and AI analysis API calls.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
