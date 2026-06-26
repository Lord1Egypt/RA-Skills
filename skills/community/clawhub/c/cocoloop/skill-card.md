## Description: <br>
A faster, safety-oriented skill manager that helps agents search, download, install, update, uninstall, and check agent skills while keeping search decisions and complex orchestration with the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catrefuse](https://clawhub.ai/user/catrefuse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use CocoLoop to locate installable skills, inspect candidates, install or update them into supported agent skill directories, uninstall existing skills, and run safety-oriented checks before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install, replace, update, and remove files in agent skill directories. <br>
Mitigation: Use it only with trusted sources, check resolved target paths before applying changes, and avoid --force or broad uninstall scopes unless the affected paths are confirmed. <br>
Risk: Safety scan and candidate file workflows can upload local files or directories to the CocoLoop service. <br>
Mitigation: Do not scan or submit secrets, private repositories, credentials, SSH keys, or personal files. <br>
Risk: The OpenAI agent configuration allows implicit invocation. <br>
Mitigation: Disable or narrowly constrain implicit invocation when operating in sensitive repositories or environments. <br>


## Reference(s): <br>
- [CocoLoop ClawHub Release Page](https://clawhub.ai/catrefuse/cocoloop) <br>
- [Skill Installation Guide](references/install-guide.md) <br>
- [Skill Search Guide](references/search-guide.md) <br>
- [Skill Uninstall Guide](references/uninstall-guide.md) <br>
- [CocoLoop Operations Manual](references/operations-manual.md) <br>
- [Safety Check Workflow Guide](references/safety-check-guide.md) <br>
- [CocoLoop Safe Check Standard](references/cocoloop-safe-check.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with command examples, status lines, JSON summaries, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local shell scripts and remote APIs to search, inspect, install, uninstall, update, and scan skills.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
