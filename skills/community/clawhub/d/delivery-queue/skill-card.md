## Description: <br>
Delivery Queue schedules and sends segmented messages at timed intervals to mimic human-like delivery and optimize engagement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents supporting outreach workflows use this skill to queue segmented messages for WhatsApp, Telegram, or email, list pending deliveries, cancel scheduled items, and flush queued messages when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local queue can store phone numbers, handles, email addresses, and message text. <br>
Mitigation: Review queue files before use, avoid sensitive or regulated content unless retention and deletion requirements are defined, and run the clean or cancel workflow for stale entries. <br>
Risk: Flush or scheduled delivery workflows can affect real outbound messaging. <br>
Mitigation: Confirm every recipient, channel, message, and timing before running schedule or flush commands, and restrict use to approved outreach workflows. <br>
Risk: The skill describes pacing behavior that could be misused for spam-like outreach. <br>
Mitigation: Use only with recipient consent and applicable messaging policies, and review campaigns for compliance before queuing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ipythoning/delivery-queue) <br>
- [Publisher profile](https://clawhub.ai/user/ipythoning) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell command usage and local JSON queue entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queue entries may include channel, recipient, message text, delivery timestamp, status, and retry count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
