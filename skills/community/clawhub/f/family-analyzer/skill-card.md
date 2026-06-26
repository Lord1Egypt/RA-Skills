## Description: <br>
Analyzes family or group chat exports and generates a collective soul.md plus member persona Markdown files for use as AI agent personality foundations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengury](https://clawhub.ai/user/zengury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process exported chat records, identify relationship and behavior patterns, and produce Markdown persona files that can guide AI agents. It is intended for user-supplied chat exports where participants have consented to analysis and any external model processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive private chats may be processed by external LLM services. <br>
Mitigation: Use only chat exports whose participants have consented, and define clear privacy, retention, and deletion controls before running the skill. <br>
Risk: The release evidence reports bundled private-looking chat data and generated output files. <br>
Mitigation: Remove bundled raw chat data and generated outputs before installation or redistribution. <br>
Risk: The release evidence reports embedded Kimi API credentials. <br>
Mitigation: Delete the embedded credential, rotate the exposed key, and require runtime configuration through user-controlled environment variables. <br>
Risk: The release evidence recommends fixing the runner to process only the user-selected file. <br>
Mitigation: Validate the runner behavior before use so it reads only the path explicitly provided by the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zengury/family-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/zengury) <br>
- [Bundled README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown files and progress-tagged terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces soul.md and persona_*.md files from chat exports; stage markers report pipeline progress and output paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence; bundled SKILL.md frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
