## Description:

Helps agents create and track Aholo 3D reconstruction or generation tasks from user-provided media or prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohao17501671450-lgtm](https://clawhub.ai/user/xiaohao17501671450-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Aholo users can ask an agent to reconstruct 3D scenes or objects from images or video, generate 3D content from a prompt or image, and check task progress and results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media and task metadata are shared with Aholo under the user's API key.

Mitigation: Upload only media the user authorizes and protect the API key; review accessible task metadata before using the list action.

Risk: Creating tasks can consume credits, especially when generating separate tasks for multiple videos or retrying an uncertain request.

Mitigation: Confirm separate-task choices and potential charges upfront; avoid duplicate creates and inspect existing tasks before retrying.

Risk: Disabling TLS verification can expose media and credentials to interception.

Mitigation: Keep TLS verification enabled and use a trusted CA bundle rather than AHOLO_INSECURE_SKIP_VERIFY.

Risk: Unpinned Python dependencies can change between installations.

Mitigation: Pin and audit dependencies before production use.

## Reference(s):

- [Aholo skill release on ClawHub](https://clawhub.ai/xiaohao17501671450-lgtm/skills/aholo-3dgs-recon-global)
- [Aholo API keys](https://labs.aholo.ai/api-keys)
- [Aholo pricing](https://www.aholo.ai/pricing)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with task IDs, status updates, viewer links, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Completed tasks may provide links to 3D asset files.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
