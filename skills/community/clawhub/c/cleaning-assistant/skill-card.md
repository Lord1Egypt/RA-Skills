## Description: <br>
A Chinese-language cleaning management agent that helps users plan cleaning work, manage room checklists and supplies, track cleaning records in local SQLite storage, query cleaning guidance, and generate monthly HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, household managers, and office administrators use this skill to organize recurring cleaning tasks, record completed cleaning work, monitor supplies, look up practical cleaning methods, and review monthly activity reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save cleaning activity from broad natural-language triggers into a local SQLite database. <br>
Mitigation: Be explicit when asking it to save records, review saved entries, and delete mistaken records when needed. <br>
Risk: Generated HTML reports load Chart.js from a CDN. <br>
Mitigation: Open reports only in contexts where the CDN dependency is acceptable, especially when report contents may be sensitive. <br>
Risk: Cleaning technique guidance may not fit every product, surface, or chemical combination. <br>
Mitigation: Follow product instructions, use ventilation and protective equipment where appropriate, and verify safety before applying cleaning chemicals. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/bettermen/cleaning-assistant) <br>
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, HTML files, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, local SQLite-backed records, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and may create local files under the skill directory, including data/cleaning.db and monthly cleaning_report_<year>_<month>.html reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
