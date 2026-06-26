## Description: <br>
Enables an AI assistant to create, publish, update, and manage novels on fireseed.online through HTTP APIs without browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanzhishuyuan](https://clawhub.ai/user/sanzhishuyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors and agent users use this skill to direct an AI assistant to authenticate with Fireseed, create novels, publish or edit chapters, upload covers, and manage published works through HTTP API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage a live Fireseed account, including registration, token use, publishing, editing, and deletion. <br>
Mitigation: Require explicit user confirmation before each account, credential, publishing, editing, or deletion action. <br>
Risk: The skill directs agents to make feed, recommendation, and telemetry or event-reporting calls without strong consent boundaries. <br>
Mitigation: Ask for consent before feed/recommendation calls and before reporting activation or publishing events. <br>
Risk: Broad writing prompts may trigger external API activity and publish generated content unintentionally. <br>
Mitigation: Use narrow prompts, preview generated chapters, and confirm the target novel and chapter order before publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sanzhishuyuan/fireseed-auto-novel-publish) <br>
- [Fireseed Platform](https://fireseed.online) <br>
- [Fireseed Admin](https://fireseed.online/admin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown prose with HTTP request examples, JSON payloads, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish or modify live Fireseed content and report skill events when used with valid credentials.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
