## Description: <br>
Feishu Power Skill helps agents automate Feishu Bitable operations, cross-table queries, document generation, retail operations audits, and scheduled reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zj00777](https://clawhub.ai/user/zj00777) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and business teams use this skill to automate Feishu Bitable workflows, generate Feishu documents from templates, audit retail operating data, and run recurring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A schedule file can invoke local Python code through custom job settings. <br>
Mitigation: Run only trusted schedule files and review or remove jobs that use type custom, script, or args before execution. <br>
Risk: Configured Feishu credentials may allow broad Bitable or document changes. <br>
Mitigation: Use a dedicated least-privilege Feishu app and test with dry-run or local output before bulk updates or publishing. <br>
Risk: Snapshots and generated reports may contain workspace or business data. <br>
Mitigation: Keep generated files out of shared folders and source control unless they have been reviewed for sensitive content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zj00777/feishu-power-skill) <br>
- [Publisher profile](https://clawhub.ai/user/zj00777) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, command-line output, YAML configuration, and Feishu API side effects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read and write Feishu Bitable records and Feishu documents when credentials and permissions are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
