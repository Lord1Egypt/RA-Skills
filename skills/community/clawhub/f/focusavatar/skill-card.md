## Description:

A CLI skill for submitting FocusAvatar digital-human video generation jobs from MP3/MP4 media and text, then checking results by order number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lintqiu](https://clawhub.ai/user/lintqiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate digital-human videos by submitting media URLs and text to a FocusAvatar backend, or to check existing generation jobs by order number.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and job data can be sent to any backend URL configured through FOCUSAVATAR_API, and the security evidence notes no host or HTTPS checks.

Mitigation: Install only if you trust the publisher and backend; leave FOCUSAVATAR_API unset unless it points to a trusted HTTPS service.

Risk: The accessKeySecret can be exposed if it is stored permanently in shell startup files or shared environments.

Mitigation: Prefer a temporary session or secret manager for accessKeySecret, and rotate the key if it may have been exposed.

Risk: Installer and Python dependency resolution can change over time.

Mitigation: Pin installer and Python dependency versions where possible before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lintqiu/skills/focusavatar)
- [Publisher profile](https://clawhub.ai/user/lintqiu)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [FocusAvatar console](https://login.joycoreai.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [CLI prompts, status text, JSON API responses, and video URL output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires accessKeyId/accessKeySecret credentials and network access to a trusted FocusAvatar backend; generation can take several minutes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
