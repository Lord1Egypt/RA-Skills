## Description: <br>
Automates learning workflows for mooc.ctt.cn, including study hours, topics, courses, and tasks with QR-code login and progress monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gandli](https://clawhub.ai/user/gandli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to set up and run a browser automation workflow for mooc.ctt.cn study-hour, topic, course, and task completion while reporting progress from local status files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill clones and runs unpinned external code from GitHub. <br>
Mitigation: Review the upstream repository first and run only a commit or release you have explicitly approved. <br>
Risk: The workflow stores reusable mooc.ctt.cn login state locally. <br>
Mitigation: Protect access to the working directory and delete output/auth-state.json when saved login state is no longer needed. <br>
Risk: The automation can interrupt local Chrome sessions and performs broad browser cleanup actions. <br>
Mitigation: Run it in an isolated environment or close unrelated Chrome work before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gandli/cttc-auto-learn) <br>
- [Project repository](https://github.com/gandli/cttc-auto-learn) <br>
- [Publisher profile](https://clawhub.ai/user/gandli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, Text] <br>
**Output Format:** [Markdown guidance with shell commands and status-report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local status, log, QR-code, and saved-login files while operating the upstream automation project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
