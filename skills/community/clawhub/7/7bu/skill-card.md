## Description: <br>
Uploads user-selected images to the 7bu.top image hosting service using a user-provided TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[penndu](https://clawhub.ai/user/penndu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to upload JPEG, PNG, GIF, BMP, ICO, or WEBP images to 7bu.top by supplying an image file path or URL and a 7bu TOKEN. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images are uploaded to 7bu.top. <br>
Mitigation: Install only if you trust 7bu.top with the images you upload, and verify the exact file or URL before invoking the skill. <br>
Risk: The 7bu TOKEN may be exposed if placed in shared logs or public chats. <br>
Mitigation: Treat the TOKEN like a password, avoid sharing it in logs or chats, and rotate it if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/penndu/7bu) <br>
- [7bu.top image hosting service](https://7bu.top) <br>
- [7bu.top upload API endpoint](https://7bu.top/api/v1/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided 7bu TOKEN and an image file path or URL; supported formats are JPEG, JPG, PNG, GIF, BMP, ICO, and WEBP.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
