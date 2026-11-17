## Description:

Create and manage Alibaba Cloud IMS video translation jobs via OpenAPI, including subtitle, voice, face processing, status polling, and job management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media operations teams use this skill to submit Alibaba Cloud IMS video translation jobs, choose subtitle, voice, or face translation settings, poll job status, and manage job records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may receive Alibaba Cloud credentials that can create, inspect, or delete IMS media jobs and access related OSS or VOD resources.

Mitigation: Use least-privilege Alibaba Cloud keys scoped to the required IMS, OSS, and VOD actions, and review any delete operation before execution.

## Reference(s):

- [IMS video translation parameter reference](artifact/references/fields.md)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-media-video-translation)
- [ClawHub publisher profile](https://clawhub.ai/user/cinience)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown guidance with API operation names, configuration fields, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize Alibaba Cloud API responses and evidence artifacts under the skill output directory.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
