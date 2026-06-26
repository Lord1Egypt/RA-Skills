## Description: <br>
Analyzes Git repositories to compare developer commit patterns, work habits, development efficiency, code style, code quality, and slacking indicators, then generates data-driven evaluations with scores, grades, strengths, weaknesses, and actionable suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongbai233](https://clawhub.ai/user/kongbai233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze one Git repository or a directory of repositories, compare contributor behavior and code-health metrics, and produce reports for review or self-improvement. It supports author filtering, date ranges, branch selection, and Markdown, JSON, HTML, or PDF outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Developer privacy and consent risk from analyzing personal activity patterns in Git history. <br>
Mitigation: Run the skill only on repositories the user is authorized to analyze and obtain informed consent from affected developers before reviewing individual-level results. <br>
Risk: Scores, grades, leaderboards, or slacking labels could be misused for punitive personnel decisions. <br>
Mitigation: Use results for aggregate insight, self-review, or engineering discussion only; do not use them for HR, compensation, discipline, or public shaming. <br>
Risk: Generated reports may contain personal work-pattern data. <br>
Mitigation: Store reports securely, limit access to appropriate reviewers, and avoid public sharing. <br>
Risk: Broad recursive scans may collect more repository and contributor data than needed. <br>
Mitigation: Set an explicit repository path, author list, and date range, and use recursive scanning only when necessary. <br>


## Reference(s): <br>
- [Metrics Guide](references/metrics-guide.md) <br>
- [PyDriller](https://github.com/ishepard/pydriller) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, PDF, Shell commands, Guidance] <br>
**Output Format:** [Markdown, JSON, HTML, PDF, and concise natural-language guidance with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report files when an output path or multi-format output is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
