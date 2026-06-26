## Description: <br>
自动追踪用户情绪变化，在合适的时机关心用户。检测对话情绪、记忆历史、主动关心、周报生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[786793119](https://clawhub.ai/user/786793119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to detect emotional tone in conversation text, keep local mood history, send care-oriented messages after negative signals, and generate weekly mood summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local mood history and short analyzed message snippets may contain sensitive personal information. <br>
Mitigation: Install only when local retention is acceptable, and periodically inspect or delete ~/.memory/emotions/history.json to remove retained history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/786793119/emotion-memory-assistant) <br>
- [Skill-declared homepage](https://github.com/786793119/miya-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Python dictionaries and text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local mood history to ~/.memory/emotions/history.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
