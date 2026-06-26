## Description: <br>
Automates Boss Zhipin job browsing, OCR-assisted job analysis, technical matching, and recruiter message sending from a desktop environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinkerjueberg](https://clawhub.ai/user/tinkerjueberg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and automation developers use this skill to automate Boss Zhipin job listing review, capture job descriptions for OCR, match roles against configured technical criteria, and send prepared outreach messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a live desktop and repeatedly interact with a job platform. <br>
Mitigation: Run it first in an isolated browser window or test account, keep pyautogui failsafe enabled, and stop execution if coordinates or page state are wrong. <br>
Risk: The skill can send recruiter messages without manual review, including exaggerated skill claims from the template. <br>
Mitigation: Require manual approval before sending any message and edit the chat template to reflect accurate experience. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tinkerjueberg/bosszhipin-automation) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact README.md](artifact/README.md) <br>
- [Artifact config.json](artifact/config.json) <br>
- [Boss Zhipin jobs page](https://www.zhipin.com/web/geek/jobs) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local screenshots and OCR output; desktop actions depend on configured screen coordinates and live page state.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version, artifact/config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
