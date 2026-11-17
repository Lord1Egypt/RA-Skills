## Description:

基于 pyautogui 实现 Boss 直聘职位浏览、OCR 分析、技术匹配和沟通话术生成及发送的无 GUI 自动化技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinkerjueberg](https://clawhub.ai/user/tinkerjueberg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate Boss Zhipin job browsing workflows: opening job entries, taking screenshots, extracting text with OCR, matching technical keywords, and preparing outreach messages. Because the artifact can send messages through the live desktop, operators should use it only where automated job-platform outreach is permitted and supervised.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send job-platform messages through live desktop automation with weak safeguards.

Mitigation: Run only in an isolated environment, change sending behavior to draft-only by default, and require explicit approval before each send.

Risk: The skill may interact with the wrong page, recipient, or active desktop target.

Mitigation: Verify the active Boss Zhipin page and intended recipient before each automated action, and add per-session action limits.

Risk: Generated outreach guidance includes qualification exaggeration.

Mitigation: Remove exaggeration instructions and require messages to accurately represent the operator's qualifications.

Risk: The workflow stores screenshots and OCR outputs from job pages.

Mitigation: Define screenshot and OCR retention rules and delete captured files that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinkerjueberg/skills/bosszhipin-automation)
- [Publisher profile](https://clawhub.ai/user/tinkerjueberg)
- [Boss Zhipin jobs page](https://www.zhipin.com/web/geek/jobs)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown guidance, Python commands, configuration values, generated outreach text, screenshots, and OCR text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local screenshot and OCR output files and may paste and send configured chat text through desktop automation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
