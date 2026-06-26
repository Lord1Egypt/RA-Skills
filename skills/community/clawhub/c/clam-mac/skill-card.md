## Description: <br>
Give AI hands to control any Mac app. Auto-discover installed apps, generate CLI wrappers, return structured JSON. Works with Music, Finder, Chrome, Word, Figma, and 20+ more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mileszhang001-boom](https://clawhub.ai/user/mileszhang001-boom) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill on macOS to discover controllable local apps, install generated CLAM wrappers, execute app commands, and use structured JSON results for follow-up reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over local Mac apps and logged-in app sessions. <br>
Mitigation: Install only for trusted agents, use a virtual environment, review the external package source, and remove MCP registration or generated wrappers when no longer needed. <br>
Risk: Mac Automation and Accessibility permissions can expose sensitive app data or allow app actions. <br>
Mitigation: Grant macOS permissions narrowly and require confirmation before reading Mail, Calendar, or Reminders. <br>
Risk: Generated app commands may send, move, archive, or delete user data. <br>
Mitigation: Require explicit user confirmation before any send, move, archive, or delete action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mileszhang001-boom/clam-mac) <br>
- [Publisher Profile](https://clawhub.ai/user/mileszhang001-boom) <br>
- [Homepage](https://github.com/mileszhang001-boom/cli-on-mac) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets macOS app automation through generated CLAM command-line wrappers.] <br>

## Skill Version(s): <br>
0.2.0 (source: release, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
