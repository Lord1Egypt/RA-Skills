## Description: <br>
Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangfeng1995](https://clawhub.ai/user/huangfeng1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to track blog and RSS/Atom feed updates, scan feeds for new articles, list tracked blogs and articles, mark articles read, and remove tracked blogs through the blogwatcher CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-suggested CLI commands can change local blogwatcher state, including removing tracked blogs or marking articles read. <br>
Mitigation: Review the exact blogwatcher command and target before execution, especially remove and read-all operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangfeng1995/blogwatcher-old) <br>
- [blogwatcher project homepage](https://github.com/Hyaxia/blogwatcher) <br>
- [Publisher profile](https://clawhub.ai/user/huangfeng1995) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume the blogwatcher binary is installed and available on PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
