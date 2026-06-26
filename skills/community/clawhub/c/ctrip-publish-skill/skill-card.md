## Description: <br>
Automates Ctrip content-center picture-text notes by gathering images, filling title and body fields, selecting destination metadata, and preparing or triggering publication in a logged-in browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ansike](https://clawhub.ai/user/ansike) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to draft and publish travel or food notes to Ctrip by automating image collection, form filling, destination selection, and browser actions. It is intended for users who can review the generated content and approve publication from an authenticated Ctrip account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a logged-in Chrome session and modify a live Ctrip publishing page. <br>
Mitigation: Run it in a separate browser profile where possible and keep the session limited to the Ctrip account needed for the post. <br>
Risk: Generated titles, body text, destination choices, and downloaded images may be inaccurate or unsuitable for publication. <br>
Mitigation: Review all generated text, selected images, and form fields before allowing final publication. <br>
Risk: The publication boundary is unclear because automation may click or prepare publish actions on a live page. <br>
Mitigation: Require explicit user approval for the exact final post before any publish confirmation is accepted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ansike/ctrip-publish-skill) <br>
- [Ctrip picture-text publishing page](https://we.ctrip.com/publish/publishPictureText) <br>
- [Ctrip creator backend](https://we.ctrip.com/publish/publishHome) <br>
- [Ctrip content management](https://we.ctrip.com/publish/contentManagement) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style guidance with Python, JavaScript, and shell command artifacts for browser automation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate a logged-in Chrome session, download images to local temporary storage, fill live web forms, and request or perform publishing actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
