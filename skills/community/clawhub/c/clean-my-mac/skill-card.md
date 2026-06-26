## Description: <br>
cleanMyMacSkill helps agents scan disk usage on macOS, Windows, and Linux, classify cleanup candidates, and produce an interactive HTML report with optional local cleanup actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peizhou](https://clawhub.ai/user/peizhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to understand what is consuming local disk space, prioritize cleanup candidates, and generate a reviewable report before taking cleanup actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The interactive cleanup mode can remove local files, and permanent delete is intentionally destructive. <br>
Mitigation: Use the static report or trash mode for safer review, and use permanent delete only after checking every listed path. <br>
Risk: Disk cleanup recommendations can include user data or application state that needs manual review. <br>
Mitigation: Review the report classifications and inspect paths before approving cleanup actions, especially items marked for review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/peizhou/clean-my-mac) <br>
- [README (English)](README.en.md) <br>
- [macOS Storage Layout & Classification Reference Guide](references/macos.md) <br>
- [Windows Storage Layout & Classification Reference Guide](references/windows.md) <br>
- [Linux Storage Layout & Classification Reference Guide](references/linux.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown summary, shell commands, JSON scan data, and generated HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static report mode is safer for review; local server mode can move files to trash or permanently delete allowlisted paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
