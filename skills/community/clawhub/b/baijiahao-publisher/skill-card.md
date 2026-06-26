## Description: <br>
Automates Baijiahao article publishing through the OpenClaw browser, including login, title and body entry, cover upload, AI-content disclosure, and publish or draft handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[279458179](https://clawhub.ai/user/279458179) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and publishing teams use this skill to prepare and submit Baijiahao articles from an authenticated browser session. It is intended for workflows where an agent can fill article fields, upload a cover image, mark AI-generated content when applicable, and either publish or save a draft for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an authenticated Baijiahao publishing session and submit content on the user's behalf. <br>
Mitigation: Review the target account, title, body, cover image, and AI-content declaration before submission; prefer saving a draft unless publication is explicitly confirmed. <br>
Risk: The artifact describes cookie injection as an alternate login path, which can expose account credentials or bypass normal authentication handling. <br>
Mitigation: Use normal QR login and do not provide or inject cookies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/279458179/baijiahao-publisher) <br>
- [Baijiahao publishing console](https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Browser automation actions, File uploads, Status messages] <br>
**Output Format:** [Instructional workflow with browser tool calls and publishing status outcomes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw browser session and an authenticated Baijiahao account; may upload a local or generated cover image.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
