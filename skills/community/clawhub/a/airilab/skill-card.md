## Description:

AIRILAB helps agents use AiriLab image generation and task management workflows for MJ creative rendering, creative upscaling, and atmosphere conversion while handling login, project selection, task submission, status polling, and result delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tatekii](https://clawhub.ai/user/tatekii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to submit AiriLab image generation, upscaling, and atmosphere conversion jobs, maintain the required account and project context, and receive asynchronous job results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a background worker across sessions and store local account tokens and job data.

Mitigation: Review worker autostart before installation, use a protected AIRILAB_HOME location, and clear token and project data when finished.

Risk: Images and local files may be uploaded to AiriLab services as part of generation, upscaling, or atmosphere conversion workflows.

Mitigation: Avoid using sensitive files as inputs and confirm that the AiriLab service is acceptable for the intended data before running jobs.

## Reference(s):

- [AiriLab service](https://cn.airilab.com)
- [ClawHub skill page](https://clawhub.ai/tatekii/skills/airilab)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Files]

**Output Format:** [Markdown guidance with command output summaries and generated image result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local token, project, job, worker log, and worker pid files under the configured AIRILAB_HOME runtime directory.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
