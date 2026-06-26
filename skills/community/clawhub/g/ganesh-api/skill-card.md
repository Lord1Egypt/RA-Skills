## Description: <br>
Ganesh Image Hosting API for image hosting. Use when user mentions "Ganesh", "upload image", "image hosting", or asks about image sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidbergman121](https://clawhub.ai/user/davidbergman121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to work with Ganesh image hosting: uploading images, obtaining shareable URLs, and embedding hosted images in Markdown, articles, or documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images uploaded through Ganesh are sent to an external hosting service and may become shareable outside the user's current workspace. <br>
Mitigation: Confirm the exact image before upload and avoid private or confidential images unless the user intends to share them through that service. <br>
Risk: Ganesh API endpoints and parameters may change over time. <br>
Mitigation: Verify the current Ganesh API documentation before sending data or relying on a specific endpoint. <br>


## Reference(s): <br>
- [Ganesh Official API Documentation](https://ishortn.ink/ganesh-official-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text guidance for using the Ganesh API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include shareable image URLs after the agent helps the user use the external Ganesh hosting service.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
