## Description: <br>
Organizes files in a selected directory by moving them into folders named after their file extensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can use this skill to clean up local folders by grouping files into extension-named subfolders. It is suited for quick directory organization tasks such as sorting downloads or desktop files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill moves files immediately and can disrupt paths or workflows in the selected directory. <br>
Mitigation: Run it first on a copy or non-critical folder and use it only on directories intended for reorganization. <br>
Risk: Files without extensions are also moved into a generated no_ext folder. <br>
Mitigation: Review the target directory before running the organizer so extensionless files are expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/file-organizer-by-ext) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local file-moving guidance and command-line usage for organizing directory contents.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
