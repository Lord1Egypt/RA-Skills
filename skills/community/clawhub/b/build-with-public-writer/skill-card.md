## Description: <br>
Use the bwp command to create technical content for codewithriver, including articles, courses, theory notes, writing personas, version management, and link sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riverfor](https://clawhub.ai/user/riverfor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, developers, and technical educators use this skill to scaffold and manage Markdown articles, course outlines, theory notes, and writing personas in a local content workspace. It also provides helper commands for listing content, committing changes, checking status, and generating local share links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated sharing server can expose local content or directory listings more broadly than intended. <br>
Mitigation: Bind the server to localhost or a trusted interface, change the default .env password, and avoid public exposure until path handling and directory listing behavior are reviewed. <br>
Risk: The Git helper can commit more local data than the user expects. <br>
Mitigation: Add .env to .gitignore and review git status and git diff before running bwp commit. <br>
Risk: The skill runs a shell script that creates files and configuration in a local publishing workspace. <br>
Mitigation: Review scripts/bwp.sh before installation and set BWP_PROJECT_ROOT to an intended workspace before creating content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/riverfor/build-with-public-writer) <br>
- [Outline template](templates/outline.template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, shell command output, generated Python server code, and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates files under a local content workspace controlled by BWP_PROJECT_ROOT or the default project path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
