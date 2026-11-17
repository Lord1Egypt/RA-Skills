## Description:

Guides an agent through booking train tickets in the 12306 Android app using a USB-connected phone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlittlebear](https://clawhub.ai/user/openlittlebear)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and their authorized agents use this skill to search for and reserve train tickets in the 12306 Android app. The traveler logs in and pays manually, and confirms the trip details before the agent submits an order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Device control could submit an unintended ticket order.

Mitigation: Use only for an explicit booking request; show the train, date, route, seat, price, and passenger and obtain confirmation before submitting.

Risk: Screenshots and OCR may expose personal travel details.

Mitigation: Treat captures as sensitive, keep them in private storage, and remove them when no longer needed.

Risk: Credentials or payment details could be exposed through automation or the device clipboard.

Mitigation: Leave login and payment to the user on the phone and do not put secrets on the clipboard.

## Reference(s):

- [12306 Android Adb on ClawHub](https://clawhub.ai/openlittlebear/skills/12306-android-adb)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the appium-android-adb base skill, a USB-connected Android device, and manual login and payment.]

## Skill Version(s):

2.2.5 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
