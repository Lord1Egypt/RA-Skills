## Description: <br>
Lists and inspects local Codex session history from ~/.codex session files, including session ids, titles, projects, workspaces, timestamps, active or archived source, and optional detail or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sube-py](https://clawhub.ai/user/sube-py) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Codex users use this skill to find local Codex sessions, identify the project or workspace each session belongs to, and inspect recent or archived session details when reconstructing work history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Output can reveal private workspace paths, project names, session titles, and prompt snippets from local Codex history. <br>
Mitigation: Review results before sharing them, especially when using --details, --json, or --contains, and avoid running the skill unless local Codex history access is acceptable. <br>
Risk: The skill reads local files under ~/.codex to enumerate sessions. <br>
Mitigation: Use it only in trusted local environments and treat generated session listings as potentially sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sube-py/codex-session-history) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; script output as a table, detail blocks, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local Codex session history and defaults to concise unarchived-session output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
