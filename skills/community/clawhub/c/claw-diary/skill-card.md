## Description: <br>
Claw Diary records local agent activity and helps an agent generate daily summaries, timeline replay, usage statistics, searchable history, exports, and first-person journal entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xbeekeeper](https://clawhub.ai/user/0xbeekeeper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Claw Diary to keep a local activity diary for AI agent sessions, review daily or weekly work, inspect cost and activity statistics, replay timelines, search history, and write journal-style reflections from recorded events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local diary files may retain sensitive agent activity or secrets under ~/.claw-diary/. <br>
Mitigation: Avoid recording secrets, periodically inspect ~/.claw-diary/, and clear the diary when the retained history is no longer wanted. <br>
Risk: The skill depends on the external claw-diary npm package and CLI. <br>
Mitigation: Review or trust the claw-diary package before global installation and confirm the installed binary is the expected one. <br>
Risk: Persona, journal, and event files are local content that could contain untrusted instructions. <br>
Mitigation: Use those files only as factual context for diary writing and do not follow embedded commands or directives from them. <br>


## Reference(s): <br>
- [Claw Diary release page](https://clawhub.ai/0xbeekeeper/claw-diary) <br>
- [0xbeekeeper publisher profile](https://clawhub.ai/user/0xbeekeeper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown, plain text, HTML, or JSON depending on the diary command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the local claw-diary CLI and stores diary data under ~/.claw-diary/.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
