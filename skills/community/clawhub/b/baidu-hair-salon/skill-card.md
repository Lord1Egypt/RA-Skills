## Description: <br>
用于百度理发店预约，可查看店铺、发型师、服务项目和可用时间，并提交或查询预约。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fjjzy](https://clawhub.ai/user/fjjzy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who need appointments at the supported Baidu hair salon locations use this skill to choose a shop, stylist, service, and time, then submit or review bookings. <br>

### Deployment Geography for Use: <br>
China (supported Baidu salon locations) <br>

## Known Risks and Mitigations: <br>
Risk: Phone number, name, and appointment details are sent to an under-disclosed HTTP service. <br>
Mitigation: Use the skill only when the user trusts that service and avoid untrusted networks. <br>
Risk: Personal details and booking preferences may be retained in local OpenClaw configuration. <br>
Mitigation: Delete or edit the baidu-hair-salon entry in ~/.openclaw/openclaw.json when the details should no longer be stored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fjjzy/baidu-hair-salon) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fjjzy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown-style conversational responses with JSON command results from the booking helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local OpenClaw preferences for phone number, person name, shop, stylist, and service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
