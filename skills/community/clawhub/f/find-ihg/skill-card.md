## Description: <br>
Finds IHG points-night options in Shanghai, Jiangsu, and Zhejiang, with filters for brand, distance, points range, and executive lounge availability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddylhb](https://clawhub.ai/user/eddylhb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and agent users use this skill to compare IHG reward stays and promotions in the Jiangsu-Zhejiang-Shanghai region. It returns ranked hotel suggestions with points, cash value, distance, brand, and lounge signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports that the main query script and hotel database are missing or referenced from outside the package. <br>
Mitigation: Install only after the publisher includes those files or clearly documents the trusted external path they come from. <br>
Risk: Backup and rollback scripts can change local OpenClaw skill and script files. <br>
Mitigation: Inspect backups before restoring and review maintenance scripts before running them. <br>
Risk: Artifact documentation states that current hotel availability and price values may use simulated data. <br>
Mitigation: Treat recommendations as planning guidance unless the publisher documents a live trusted data source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eddylhb/find-ihg) <br>
- [Artifact changelog](references/CHANGELOG.md) <br>
- [Artifact audit report](references/audit_report.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style text with ranked hotel recommendations, filter summaries, points and cash-value analysis, and booking guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on packaged or external hotel data and query execution files; current release evidence says the main query script and hotel database are missing or referenced outside the package.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
