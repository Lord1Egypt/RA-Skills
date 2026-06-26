## Description: <br>
Generates daily work reports by discovering Git repositories with commits on a selected date, collecting commit history across branches, and summarizing CodeBuddy Agent session overviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[disyli](https://clawhub.ai/user/disyli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CodeBuddy users use this skill to collect Git activity and CodeBuddy session summaries for today, yesterday, or a specified date, then produce a structured daily work report in the user's preferred language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans broad local work directories to find Git repositories, which can surface private project paths and commit metadata. <br>
Mitigation: Review and configure excluded directories before use, especially for private or sensitive folders. <br>
Risk: Generated reports may include sensitive work details from CodeBuddy Agent session overviews. <br>
Mitigation: Review the generated report before saving or sharing it, and avoid running the skill casually in sensitive workspaces. <br>


## Reference(s): <br>
- [Skill instructions](SKILL.md) <br>
- [README](README.md) <br>
- [Report template](assets/template.md) <br>
- [Configuration reference](references/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown report with structured JSON collection data from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save the generated report as daily-report-{YYYY-MM-DD}.md and may include local commit metadata plus CodeBuddy session overview excerpts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
