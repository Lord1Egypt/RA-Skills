## Description:

Auto Course Player helps an agent automate playback of online course videos in Chrome, including muting videos, detecting completion, switching to the next video, and reporting progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanfuda](https://clawhub.ai/user/quanfuda)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to control Chrome or a Tampermonkey userscript for sequential online course video playback, progress checks, pause/resume control, and learning-time reporting. It is intended only for authorized use that complies with the applicable course platform rules and academic integrity requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates course video playback and completion behavior on a logged-in university course site.

Mitigation: Install and run it only when the user is authorized to automate the platform and the use complies with school rules and academic integrity requirements.

Risk: The browser automation includes broad automatic clicking and generic popup-confirmation behavior.

Mitigation: Review the Tampermonkey match scope and disable or narrow generic popup-confirmation logic before using it on logged-in university pages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/quanfuda/skills/auto-course-player)
- [Publisher Profile](https://clawhub.ai/user/quanfuda)
- [Target Course Platform](https://studentjxjyzx.qdu.edu.cn/)
- [Tampermonkey Namespace](http://tampermonkey.net/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript userscript or bookmarklet snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local markdown progress file for course playback status.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
