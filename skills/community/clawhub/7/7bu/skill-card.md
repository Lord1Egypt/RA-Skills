## Description:

7bu uploader helps an agent upload supported image files to the 7bu.top image hosting service using a user-provided TOKEN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[penndu](https://clawhub.ai/user/penndu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to prepare image-upload requests to 7bu.top for JPEG, JPG, PNG, GIF, BMP, ICO, and WEBP files with their own service token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images selected for upload and the user-provided TOKEN are sent to 7bu.top.

Mitigation: Use a token intended only for 7bu.top and avoid uploading sensitive images unless the provider's handling of that data is acceptable.

Risk: The release is marked by ClawHub quality metadata as low trust and quarantined for moderation review.

Mitigation: Complete moderation and quality review before listing or recommending the skill for broad use.

## Reference(s):

- [7bu.top](https://7bu.top)
- [7bu upload API](https://7bu.top/api/v1/upload)
- [ClawHub skill page](https://clawhub.ai/penndu/skills/7bu)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces upload guidance for user-selected image paths or URLs and a user-provided TOKEN.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
