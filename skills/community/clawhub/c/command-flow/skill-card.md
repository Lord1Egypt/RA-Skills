## Description: <br>
Command Flow provides a Chinese-language command dashboard for listing, searching, paginating, exporting, and presenting OpenClaw slash commands with source and safety labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[largetool](https://clawhub.ai/user/largetool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to browse slash commands in Chinese, search command metadata, inspect source and safety labels, and generate text, Markdown, or Telegram-style command views before deciding what to run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill marks powerful admin commands as safe. <br>
Mitigation: Review command entries before installation and require deliberate confirmation for admin, token, scheduler, gateway, plugin, reset, memory, session, update, uninstall, or other state-changing commands. <br>
Risk: Broad natural-language triggers and command buttons may surface command actions too casually. <br>
Mitigation: Use the skill as a command reference and keep execution behind explicit user intent, especially for commands that change local or account state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/largetool/command-flow) <br>
- [Publisher profile](https://clawhub.ai/user/largetool) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Chinese text and Markdown command dashboards, optional Telegram inline-keyboard JSON, and command reference output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command safety labels, pagination controls, search results, exportable Markdown, and confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
