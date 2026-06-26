## Description: <br>
Coding style memory that adapts to your preferences, conventions, and patterns for consistent coding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbingquanxu-cpu](https://clawhub.ai/user/alexbingquanxu-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to remember explicitly confirmed coding preferences, apply them to future code output, and let users inspect or forget stored preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stale or overly broad coding preferences could steer future code output away from current intent. <br>
Mitigation: Review ~/coding/memory.md periodically and use the documented forget behavior to remove stale preferences. <br>
Risk: Preference memory is intended to stay within the local ~/coding/ storage boundary. <br>
Mitigation: Treat ~/coding/ as the storage boundary and keep entries limited to concise, confirmed coding preferences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexbingquanxu-cpu/coding-custom) <br>
- [Publisher profile](https://clawhub.ai/user/alexbingquanxu-cpu) <br>
- [Skill homepage](https://clawic.com/skills/coding) <br>
- [Preference criteria](artifact/criteria.md) <br>
- [Preference dimensions](artifact/dimensions.md) <br>
- [Memory templates](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and concise text guidance with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores confirmed preferences in ~/coding/memory.md and archives older entries in ~/coding/history.md; memory.md is limited to 100 lines.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
