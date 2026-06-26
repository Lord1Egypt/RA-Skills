## Description: <br>
Flova Video Generator lets AI agents create, edit, and export videos through Flova's conversational video generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flova](https://clawhub.ai/user/flova) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an AI assistant manage Flova video projects, send creative instructions, upload assets, export videos, and handle subscription or credit flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an assistant operate a Flova account, upload user media, export or download project assets, and trigger credit-affecting subscription or purchase flows. <br>
Mitigation: Store FLOVA_API_TOKEN in an environment variable or secret manager, not ordinary chat, and require user confirmation before project creation, uploads, exports, downloads, subscription checkout, credit purchases, or actions involving sensitive media. <br>
Risk: The security review found broad account, file-transfer, and credit-affecting authority with weak user-control boundaries. <br>
Mitigation: Use the skill only when the user intends to delegate Flova account actions to the assistant, review each proposed action before execution, and stop if the requested media or account action is unexpected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/flova/flova-video-generator) <br>
- [Flova homepage](https://www.flova.ai) <br>
- [Flova documentation](https://www.flova.ai/docs/) <br>
- [Flova token management](https://www.flova.ai/openclaw/?action=token) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FLOVA_API_TOKEN and curl; produces time-sensitive project, export, download, checkout, and asset URLs from live Flova API calls.] <br>

## Skill Version(s): <br>
0.2.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
