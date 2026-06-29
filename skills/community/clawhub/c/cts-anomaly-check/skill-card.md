## Description: <br>
Checks Huawei Cloud CTS anomaly records, including account debt status, failed operation analysis, and sensitive operation audits, and turns technical details into user-readable explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyujie](https://clawhub.ai/user/chenyujie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud security, operations, and compliance teams use this skill to inspect Huawei Cloud CTS logs for failed, warning, incident, sensitive, and deletion operations, and to produce readable remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read Huawei Cloud audit logs, account debt status, and user or resource operation details. <br>
Mitigation: Install only where that data access is acceptable, and run with explicit region, project, account, time range, and output-log controls. <br>
Risk: The skill creates temporary Huawei Cloud access keys and queries billing balance in addition to CTS traces. <br>
Mitigation: Grant only the IAM temporary credential, BSS billing balance, and CTS trace permissions required for the intended audit, and review the skill before installation. <br>


## Reference(s): <br>
- [CTS Anomaly Types](references/anomaly-types.md) <br>
- [CTS Anomaly Check Examples](references/examples.md) <br>
- [Huawei Cloud CTS API Reference](https://support.huaweicloud.com/api-cts/cts_04_0001.html) <br>
- [Huawei Cloud CTS User Guide](https://support.huaweicloud.com/usermanual-icts/cts_01_0001.html) <br>
- [Huawei Cloud IAM Best Practices](https://support.huaweicloud.com/bestpractice-iam/iam_01_0001.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text reports or JSON output, with Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit Huawei Cloud region, project ID, time range, record limit, and output format controls.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata; artifact frontmatter states 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
