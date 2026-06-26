## Description: <br>
Checks specified directory for console.log statements, excluding common folders, and reports file locations and line previews of occurrences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sy724](https://clawhub.ai/user/sy724) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill before commit or deployment to audit a project for leftover console.log debugging statements. It reports matching file locations, line previews, total occurrences, and cleanup recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans project files and may surface source snippets that contain sensitive information. <br>
Mitigation: Review findings before sharing them outside the project context, and adjust the path or exclude inputs to avoid scanning sensitive directories. <br>
Risk: Search results can include false positives or miss logging patterns that are not literal console.log calls. <br>
Mitigation: Use the results as a focused cleanup aid and review production-critical files manually before release. <br>


## Reference(s): <br>
- [Console Log Checker on ClawHub](https://clawhub.ai/sy724/console-log-checker) <br>
- [Publisher profile: sy724](https://clawhub.ai/user/sy724) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with a findings table and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes file path, line number, content preview, total occurrence count, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
