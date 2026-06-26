## Description: <br>
Your 24/7 AI front desk. Polly answers incoming calls, filters spam, takes messages, and routes important calls, so you never miss what matters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hi-yox](https://clawhub.ai/user/hi-yox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and small teams use this skill to activate a PollyReach phone number, make outbound calls, retrieve call results, and manage incoming call summaries. It is suited to receptionist-style call handling, spam filtering, voicemail capture, booking, customer-service, and follow-up workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and uses a persistent PollyReach token that can control account actions. <br>
Mitigation: Keep the token in the configured credential file, restrict file permissions, avoid pasting or printing it, and rotate it if exposure is suspected. <br>
Risk: Outbound calls and inbound prompt changes can affect real people, account settings, and paid credits. <br>
Mitigation: Confirm every outbound call request and prompt change with the user before execution, and present call outcomes, credit use, and remaining balance after completion. <br>
Risk: Call transcripts, recordings, phone numbers, and inbound summaries may contain sensitive personal or business information. <br>
Mitigation: Treat polling output and detail links as sensitive, share them only with the intended user, and avoid storing or forwarding call records beyond the user's workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/hi-yox/ai-receptionist-skills) <br>
- [PollyReach Homepage](https://pollyreach.ai) <br>
- [PollyReach Agent Portal](https://agent.pollyreach.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PollyReach API responses, local credential configuration, and call summaries or transcripts when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
