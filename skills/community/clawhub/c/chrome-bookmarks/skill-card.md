## Description: <br>
Searches, browses, and opens local Chrome bookmarks from the Chrome Bookmarks JSON file through a Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[truesnow](https://clawhub.ai/user/truesnow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents use this skill when a user asks to find, browse, or open Chrome bookmarks. It helps present bookmark names, URLs, folder paths, and tree summaries before opening a selected bookmark. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Chrome bookmark names, folder paths, and URLs. <br>
Mitigation: Install it only when that local browser data access is acceptable, and avoid sharing command output that contains sensitive bookmark information. <br>
Risk: The open command can launch the first matching bookmark, including URLs with file, javascript, data, or custom app schemes. <br>
Mitigation: Use search or list first, confirm the exact URL with the user, and be cautious before opening unusual URL schemes. <br>


## Reference(s): <br>
- [Chrome Bookmarks on ClawHub](https://clawhub.ai/truesnow/chrome-bookmarks) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and list commands return JSON arrays; open returns JSON status.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
