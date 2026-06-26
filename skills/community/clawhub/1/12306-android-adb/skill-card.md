## Description: <br>
12306-specific knowledge for booking train tickets via the Android app, including UC WebView virtual list behavior, a proven booking flow, and common automation pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlittlebear](https://clawhub.ai/user/openlittlebear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to guide Android-based 12306 train ticket booking through ADB or uiautomator2, including train search, booking-button selection, passenger selection, order submission, and manual handoff for payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a real Android phone and submit ticket orders. <br>
Mitigation: Use a test or dedicated Android device and account where possible, and require the user to confirm every booking step before order submission. <br>
Risk: Screenshot and OCR fallback can capture payment details, messages, one-time codes, or other private data. <br>
Mitigation: Avoid sensitive screens when using screenshot or OCR fallback, and delete local /tmp screenshots and on-device temporary files after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlittlebear/12306-android-adb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Android UI automation steps, ADB commands, uiautomator2 snippets, and manual payment handoff guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
