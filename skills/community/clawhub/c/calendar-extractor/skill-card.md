## Description: <br>
Extracts calendar events from recent recording and keyboard transcripts and sends each event to the user's iOS chat as an individual markdown card. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuel-wei](https://clawhub.ai/user/samuel-wei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External HiJavis users use this skill to turn spoken or typed scheduling mentions into pending calendar-event cards in iOS chat. It supports on-demand extraction and automatic extraction after a completed recording or keyboard unit matches scheduling content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically analyzes recent spoken and typed transcripts, which may include sensitive personal or business information. <br>
Mitigation: Enable it only for users and environments where transcript scanning for scheduling content is acceptable. <br>
Risk: A correction made in an event's chat thread confirms that calendar row without a separate approval step. <br>
Mitigation: Use this only where chat-based confirmation is an acceptable approval signal; otherwise keep the skill disabled or require external review before relying on confirmed rows. <br>
Risk: Automatically extracted events may be incomplete or incorrect. <br>
Mitigation: Treat newly extracted events as pending and review Confirm/Discard choices before using them as committed calendar entries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samuel-wei/skills/calendar-extractor) <br>
- [HiJavis iPhone App](https://apps.apple.com/us/app/hijavis/id6745134765) <br>
- [Route Contract](references/route-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown cards, JSON event arrays, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Extracted events are initially pending; in-thread corrections can confirm an existing card.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
