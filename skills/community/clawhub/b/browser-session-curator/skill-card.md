## Description: <br>
Turn an overwhelming set of tabs, bookmarks, and snippets into a structured session digest with tasks, reading queue, and archive plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn browser tabs, bookmarks, and notes into an actionable session digest, reading queue, archive list, and next-hour plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive tab titles, URLs, or notes supplied by the user. <br>
Mitigation: Provide only the browser session data needed for the task and review the generated digest before using it for archiving or follow-up actions. <br>
Risk: The helper script writes a digest file and could overwrite an existing output path. <br>
Mitigation: Use a fresh --out filename when running the helper script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/browser-session-curator) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Example prompt](examples/example-prompt.md) <br>
- [Session tag schema](resources/session_tags.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON files from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a local session digest, reading queue, archive list, and next-hour action plan from user-provided tab data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
