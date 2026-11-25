## Description:

Guides developers in integrating Didit's standalone Face Match API to compare two face images and handle its similarity score and approval decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write backend integrations that compare a selfie or other user image with a reference face through Didit's Face Match API. It explains how to submit images, configure the decision threshold, and handle the returned score and status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face images are sent to Didit, and requests are saved with both images by default.

Mitigation: Confirm the service's data handling is suitable for the images. Set save_api_request=false when session storage is not needed, and minimize retention of biometric data.

Risk: The integration requires a Didit API key, and the security guidance calls for protecting it.

Mitigation: Provide DIDIT_API_KEY through a secret store or protected environment variable and limit who can access it.

## Reference(s):

- [Didit Face Match API Reference](https://docs.didit.me/standalone-apis/face-match)
- [Didit Face Match Feature Guide](https://docs.didit.me/core-technology/face-match/overview)
- [Didit Pricing](https://docs.didit.me/getting-started/pricing)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python and TypeScript examples, JSON response examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples require two face image files and a DIDIT_API_KEY; requests can optionally set a decline threshold, image rotation, metadata, and whether the request is saved.]

## Skill Version(s):

1.6.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
