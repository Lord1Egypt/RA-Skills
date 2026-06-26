## Description: <br>
Chat Distill analyzes exported conversation records to identify a target speaker's chat style and generate replies that mimic that voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengqiyu9](https://clawhub.ai/user/mengqiyu9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to parse chat exports, build a style profile for a chosen speaker, produce a structured analysis report, and draft replies in the learned style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat exports can contain sensitive personal, financial, location, or account information. <br>
Mitigation: Use only chats you own or have permission to analyze, redact sensitive content before analysis, and avoid storing reusable profiles in shared locations. <br>
Risk: Generated mimicry may be mistaken for the target speaker's authentic words. <br>
Mitigation: Use mimicry with consent, label generated text clearly when sharing it, and do not present generated replies as someone else's real communication. <br>
Risk: Small samples can produce unreliable style profiles. <br>
Mitigation: Follow the skill's minimum sample guidance and warn users when the target speaker has fewer than 20 messages. <br>


## Reference(s): <br>
- [Chat Distill Skill Page](https://clawhub.ai/mengqiyu9/chat-distill) <br>
- [Format Parsers](artifact/references/format-parsers.md) <br>
- [Output Templates](artifact/references/output-template.md) <br>
- [Style Dimensions](artifact/references/style-dimensions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis reports, plain-text mimic replies, optional compact JSON style profiles, and JSON message extraction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided chat export and target speaker; warns when the target speaker has fewer than 20 messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
