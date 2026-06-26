## Description: <br>
Run a self-contained Chinese and international AI news workflow inside the current workspace. Use when the user wants either high-frequency RSS capture only or scheduled report delivery only, with cumulative Excel outputs and a merged Word brief, without relying on an external local repository path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nighmat1220](https://clawhub.ai/user/Nighmat1220) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators, analysts, and developers use this skill to collect AI news from configured domestic and international RSS feeds and produce cumulative Excel reports plus a merged Word brief for a selected reporting window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collected article text can be sent to a configured Volcengine ARK model API during report generation. <br>
Mitigation: Use trusted RSS sources and scoped ARK credentials, and run with --disable-ai when article text should not be sent to the model. <br>
Risk: The workflow persists cumulative data, reports, snapshots, and deduplication state in the selected workspace. <br>
Mitigation: Run it in an isolated workspace and review generated Excel and Word briefs before sharing or relying on them. <br>
Risk: RSS authentication data and ARK_API_KEY are runtime credentials for external services. <br>
Mitigation: Provide only scoped credentials through the intended environment or source configuration, and avoid using untrusted feed configurations. <br>


## Reference(s): <br>
- [Commands](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSONL data files, Excel workbooks, and Word document briefs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cumulative Excel reports are updated across runs; the Word brief is rebuilt per run; AI generation can be disabled.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
