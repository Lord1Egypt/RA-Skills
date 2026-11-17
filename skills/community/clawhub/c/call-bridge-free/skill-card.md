## Description: <br>
Call Bridge Free helps an agent place a single outbound call to a United States phone number through the Call Bridge API, then return call status, transcript, outcome, and recording link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and automation users use this skill to delegate bounded phone tasks, such as merchant inquiries, reservations, appointment requests, and quote collection, to a voice AI phone agent. The agent prepares the call task, makes one outbound United States call, polls for completion, and summarizes the returned transcript, outcome, and recording link. <br>

### Deployment Geography for Use: <br>
Global; outbound calls are limited to United States +1 phone numbers. <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger text could cause ordinary coding or deployment prompts to route into a real outbound-calling workflow. <br>
Mitigation: Invoke the skill only for explicit outbound-call requests, and confirm the target number and call task before any API call is made. <br>
Risk: Phone tasks, transcripts, and recording links may contain personal, financial, medical, or regulated information. <br>
Mitigation: Keep call instructions minimal, avoid sensitive data unless retention is understood, and review returned transcripts and recording links before sharing them. <br>
Risk: The skill can persist an API key and user phone number under ~/.config/call-bridge/key.json. <br>
Mitigation: Use restrictive file permissions such as mode 600, avoid printing the key in logs, and do not commit the key file to version control. <br>
Risk: Incorrect phone numbers or poorly timed calls can create unwanted outbound contact. <br>
Mitigation: Validate that the number is a complete +1 United States number and confirm appropriate calling hours before dialing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/call-bridge-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [SkillHub homepage](https://skillhub.cn) <br>
- [Call Bridge API base](https://api.call-bridge.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON request and response examples; call results include status, transcript, outcome, and recording URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist a Call Bridge API key and user phone number in ~/.config/call-bridge/key.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
