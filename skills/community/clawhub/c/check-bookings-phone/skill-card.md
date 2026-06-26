## Description: <br>
Automates an ADB-connected Android device to check Ctrip Travel prepaid hotel orders for reservation availability and price-difference status across a requested date range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcqqq](https://clawhub.ai/user/zcqqq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users who manage Ctrip Travel prepaid bookings use this skill to automate phone navigation and summarize which target dates are available, sold out, or require a price difference. It is intended for a logged-in Android device with ADB debugging enabled and configured vision-model credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically approve phone permissions or user agreements while operating the logged-in Ctrip app. <br>
Mitigation: Keep the phone visible while it runs and remove or change auto-approval behavior before relying on unattended use. <br>
Risk: Phone screenshots can include order details such as hotel names, prices, and dates and are sent to the configured external vision-model API. <br>
Mitigation: Use only a vision-model provider whose data handling you trust, and configure the model endpoint deliberately before running the skill. <br>


## Reference(s): <br>
- [Check Bookings Phone on ClawHub](https://clawhub.ai/zcqqq/check-bookings-phone) <br>
- [Midscene.js model configuration](https://midscenejs.com/choose-a-model.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands; runtime output is console text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime output includes per-order date statuses and timing summaries for the requested date range.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
