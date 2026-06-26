## Description: <br>
Automates online course video playback in Chrome, detects video completion, advances to the next video, and supports pause, resume, progress checks, and study-time reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quanfuda](https://clawhub.ai/user/quanfuda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to automate playback and progress tracking for web-based course videos in Chrome. It is intended for environments where the course platform, school, and account owner explicitly allow this form of automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can advance course progress in a logged-in education account and may affect attendance, completion credit, assessments, submissions, payments, or official records. <br>
Mitigation: Use only when the course platform, school, and account owner explicitly allow automation, and avoid use where official records or assessed work could be affected. <br>
Risk: The artifact includes anti-detection guidance and broad auto-clicking behavior for course pages and dialogs. <br>
Mitigation: Review and narrow the Tampermonkey match scope before use, remove anti-detection behavior, and keep human review for confirmations, captchas, and unexpected dialogs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/quanfuda/auto-course-player) <br>
- [README](artifact/README.md) <br>
- [Installation Guide](artifact/INSTALL.md) <br>
- [Tampermonkey Userscript](artifact/scripts/course-autoplay.user.js) <br>
- [Tampermonkey](http://tampermonkey.net/) <br>
- [Target Course Platform](https://studentjxjyzx.qdu.edu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript userscript code, browser configuration steps, and Markdown progress reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local course-progress Markdown file and browser-side automation state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
