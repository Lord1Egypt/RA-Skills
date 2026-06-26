## Description: <br>
Climate is a command-line utility skill for everyday climate-related workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to invoke a simple local CLI for status, activity logging, search, and export workflows presented as a climate utility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may retain command arguments and activity records locally. <br>
Mitigation: Avoid entering secrets, tokens, private prompts, or sensitive file paths, and review or delete ~/.local/share/climate when retained records are no longer wanted. <br>
Risk: The skill is described as a climate toolkit, while the security summary says it mostly behaves like a local history/logging utility. <br>
Mitigation: Review the skill before installation and use it only where local logging behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/climate) <br>
- [Publisher Profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output with optional JSON, CSV, or text exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read local files under ~/.local/share/climate.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
