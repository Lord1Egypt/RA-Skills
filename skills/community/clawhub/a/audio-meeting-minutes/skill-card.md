## Description: <br>
Audio Meeting Minutes helps agents transcribe meeting recordings with Alibaba Cloud NLS, summarize the transcript, and generate a formatted HTML meeting-minutes document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[namedsir](https://clawhub.ai/user/namedsir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to turn local meeting recordings into transcript-backed HTML minutes and action summaries. It is best suited for meetings that can be sent to Alibaba Cloud NLS under the user's organizational data policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting recordings and transcripts may contain sensitive information and are sent to Alibaba Cloud NLS for speech recognition. <br>
Mitigation: Use the skill only for recordings approved for that data flow, and avoid confidential, regulated, or personal data unless organizational policy permits it. <br>
Risk: Speech-service credentials may be exposed if pasted into chat or stored in logs. <br>
Mitigation: Prefer environment variables, a secret store, or local configuration files, and use short-lived, scoped credentials whenever possible. <br>
Risk: Generated summaries, decisions, or action items may omit context or misstate meeting outcomes. <br>
Mitigation: Review the generated minutes against the transcript before sharing or using them for follow-up decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/namedsir/audio-meeting-minutes) <br>
- [Alibaba Cloud NLS app and token console](https://nls-portal.console.aliyun.com/applist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands, transcript text, structured summary data, and generated HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces transcript.txt and an HTML meeting-minutes file; runtime use requires Alibaba Cloud NLS credentials and local audio tooling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
