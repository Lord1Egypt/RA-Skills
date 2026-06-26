## Description: <br>
A universal document parsing skill powered by Laiye ADP that helps agents convert PDFs, images, scanned documents, and Office files into structured Markdown while preserving headings, tables, lists, paragraphs, and other document structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
Developers, documentation teams, and AI-agent users use this skill to parse local, remote, or encoded documents into Markdown for technical documentation migration, content publishing, archival digitization, and LLM context preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents may be sent to Laiye ADP's cloud service for parsing. <br>
Mitigation: Install and use the skill only where organizational policy permits sending the target documents to that third-party service. <br>
Risk: The ADP API key is a sensitive credential. <br>
Mitigation: Protect the API key, prefer environment or approved local configuration storage, and avoid exposing it in prompts, logs, shared files, or command output. <br>
Risk: Installer examples include remote shell and PowerShell scripts. <br>
Mitigation: Prefer npm or verified release binaries, and review any remote installer script before execution. <br>
Risk: The ADP CLI supports broader actions than Markdown parsing, including extraction, custom application changes, deletion, batch processing, and billable credit usage. <br>
Mitigation: Constrain agent use to approved parse commands unless a user explicitly approves other ADP operations and related costs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/adp-pdf-to-structured-markdown) <br>
- [Laiye ADP Global](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [Laiye ADP Mainland China](https://adp.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh) <br>
- [ADP Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd) <br>
- [ADP CLI GitHub Releases](https://github.com/laiye-ai/adp-cli/releases) <br>
- [ADP CLI Issue Tracker](https://github.com/laiye-ai/adp-cli/issues) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with ADP CLI command guidance and structured parsing results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Parsing results should preserve source document structure as returned by ADP; batch jobs may also produce per-file JSON summaries or error files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
