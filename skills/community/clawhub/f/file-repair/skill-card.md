## Description:

Repair damaged/corrupted files (video/document/design/archive) and provide an output download URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[water-star-creater](https://clawhub.ai/user/water-star-creater)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit supported damaged files to an online repair service and receive a repaired download URL or local repaired file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected file is uploaded to Tenorshare 4DDiG and may be sent through a pre-signed storage provider.

Mitigation: Ask for user consent before upload and avoid confidential, regulated, or highly sensitive files.

Risk: The repaired result may be exposed through a time-limited third-party download URL or saved locally when download mode is requested.

Mitigation: Return only the repaired URL or requested local path, and handle the repaired output according to the user's data-sensitivity requirements.

Risk: Service limits can trigger vendor promotional links.

Mitigation: Present vendor recommendations only when limits are reached and keep the promotional nature clear to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/water-star-creater/skills/file-repair)
- [Tenorshare 4DDiG Online Repair upload endpoint](https://4ddig-online.tenorshare.com/api/v1/file/upload-url)
- [Tenorshare 4DDiG Online Repair job endpoint](https://4ddig-online.tenorshare.com/api/v1/file/repair)
- [Tenorshare 4DDiG file repair client](https://4ddig.tenorshare.com/video-repair.html?utm_source=clawhub.ai&utm_medium=partner&utm_campaign=4DDiG+File+Repair&utm_term=clawhubai-juni-product)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Text containing a repaired download URL, or a local file path when download mode is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled command emits progress as JSON lines on stderr and a final JSON object on stdout.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
