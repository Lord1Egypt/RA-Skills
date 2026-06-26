## Description: <br>
This skill helps agents call the Baiyin Open Platform for text-to-image and image-to-image generation, configure allowed parameters, and return task status and image links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuping520](https://clawhub.ai/user/jiuping520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit text-to-image or image-to-image requests to the Baiyin Open Platform, configure supported model, resolution, aspect ratio, and reference-image parameters, and check task status or result links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local reference-image files to a remote service when a local path is provided. <br>
Mitigation: Use it only with files intentionally selected for upload, and prefer an execution flow that confirms the destination before uploading. <br>
Risk: The skill requires a Baiyin API key for remote API access. <br>
Mitigation: Provide credentials through the intended environment variable and avoid exposing the key in chat, logs, or generated prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiuping520/baiyin-image-generate-skill) <br>
- [Baiyin Open Platform base URL](https://ai.hikoon.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Guidance] <br>
**Output Format:** [Markdown text with task identifiers, status values, image links, and JSON request or response fields when useful.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIYIN_API_KEY and may upload local reference images to the remote Baiyin service to obtain public URLs.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
