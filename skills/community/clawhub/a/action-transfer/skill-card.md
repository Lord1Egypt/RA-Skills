## Description:

Generates action-transfer video results from a reference image and an input video by calling the third-party a7w action_transfer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit and monitor paid action-transfer video jobs that apply motion from an input video to one or more reference character images. It is most useful when the user already has public media URLs and an a7w API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided public image/video URLs and an a7w API key to a third-party paid media service.

Mitigation: Use a limited and revocable API key, avoid sensitive media unless it is appropriate for the third-party service, and review the service terms before use.

Risk: The bundled client is broader than the action-transfer purpose and can call other marketplace apps or a caller-supplied host.

Mitigation: Constrain agent use to action_transfer submit/query commands and do not use --host or A7W_HOST unless the destination is explicitly trusted.

Risk: Submitting jobs can freeze or spend account points, and repeated submissions may duplicate charges.

Mitigation: Confirm media URLs, mode, duration, and account limits before submission; query existing task IDs instead of resubmitting the same job.

Risk: Generated media may require rights, consent, or content compliance review.

Mitigation: Use only authorized source media and review generated outputs under the user's applicable content and legal policies.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/2253128/skills/action-transfer)
- [Getting started](references/getting-started.md)
- [Action transfer submit API](references/api-submit.md)
- [Action transfer query API](references/api-query.md)
- [a7w API portal](https://api.a7w.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance, shell commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns task identifiers, task status, usage details, and generated video URLs when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
