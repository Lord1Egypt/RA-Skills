## Description: <br>
Helps users locate packages on delivery station shelves by matching pickup codes to shelf photos and returning annotated images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noroot777](https://clawhub.ai/user/noroot777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users in Chinese delivery-station contexts use this skill through an OpenClaw Telegram bot to find packages from pickup codes and shelf photos. The agent asks for or confirms the pickup code, checks shelf images, and returns a photo with the matching package marked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pickup-code screenshots and shelf photos may contain addresses, phone numbers, faces, or other people's packages. <br>
Mitigation: Crop screenshots where possible and avoid sending unrelated personal information, faces, or packages that are not needed for the search. <br>
Risk: Blurry photos or uncertain OCR could cause the agent to mark the wrong package. <br>
Mitigation: Confirm extracted pickup codes before searching, ask for clearer photos when labels are unreadable, and avoid guessing when no reliable match is visible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noroot777/find-package) <br>
- [OpenClaw](https://openclaw.com) <br>
- [Pillow documentation](https://pillow.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Chinese conversational text with optional annotated image files and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Annotated shelf photos use red bounding boxes and pickup-code labels when a match is found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
