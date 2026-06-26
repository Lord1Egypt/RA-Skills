## Description: <br>
Scans public social media profile links before a date and produces a data-driven Date Intel Report with inferred interests, lifestyle signals, values, red and green flags, and conversation suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophie-xin9](https://clawhub.ai/user/sophie-xin9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to review public social profile content before a date and generate a Markdown brief for conversation planning and risk-aware first impressions. The skill is intended for public-content review, not private account access or background investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled platform collectors can access active logged-in social accounts and collect sensitive histories such as likes, favorites, follows, ratings, or comments. <br>
Mitigation: Use a logged-out or separate browser profile for reviewing another person's public profile, and avoid running full account-collector steps for someone else's profile. <br>
Risk: The skill may save raw profile data locally while generating reports. <br>
Mitigation: Delete raw report files when they are no longer needed and avoid sharing generated reports without reviewing the contents. <br>
Risk: The skill can download its ManoBrowser dependency during setup. <br>
Mitigation: Manually review and approve dependency downloads before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sophie-xin9/blind-date-mirror) <br>
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser) <br>
- [Example Date Intel Report](examples/xiaokai_date_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown report with structured sections and optional shell commands for dependency checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local raw data files under date-reports/ during profile collection.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
