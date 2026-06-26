## Description: <br>
Query and analyze Tencent Cloud CLS logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbwang0130](https://clawhub.ai/user/dbwang0130) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure clscli, list Tencent Cloud CLS topics, query logs over explicit regions and time ranges, and retrieve nearby log context for incident investigation or operational analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tencent Cloud credentials may grant access to sensitive CLS logs. <br>
Mitigation: Use a dedicated least-privilege Tencent Cloud key and provide credentials only through the documented environment variables. <br>
Risk: The clscli binary is installed from a third-party Homebrew tap/source. <br>
Mitigation: Verify the clscli tap and source before installation. <br>
Risk: Broad regions, topics, or time ranges can expose more log data than intended. <br>
Mitigation: Keep regions, topics, and time ranges explicit before running queries. <br>
Risk: Exported log files may contain secrets or user data. <br>
Mitigation: Write exported logs only to protected local locations. <br>


## Reference(s): <br>
- [Tencent Cloud CLS API Documentation](https://cloud.tencent.com/document/api/614/56474) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide clscli output as JSON, CSV, or protected local files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
