## Description:

从中国知网（CNKI）检索、筛选、排序并批量下载学术文献 PDF，使用 Playwright 和 Microsoft Edge 完成需要可视化登录的流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lfp1979](https://clawhub.ai/user/lfp1979)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and agents assisting literature collection use this skill to search CNKI, apply year/source filters and sorting, open result details, and download a requested number of PDFs through a configured CNKI or institutional entry URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks agents to run browser automation outside the sandbox.

Mitigation: Review commands before execution and avoid granting broad host privileges beyond what is needed to open Edge and run the CNKI pipeline.

Risk: Login sessions are retained in a browser_data profile.

Mitigation: Use only trusted CNKI or institution URLs and clear the saved browser profile when the session is no longer needed.

Risk: Dependency installation and browser downloads can affect the local environment.

Mitigation: Use deterministic dependency installation from the bundled package metadata and review installed packages before production use.

Risk: Downloaded files and web paths are handled broadly.

Mitigation: Validate CNKI or proxy hosts, constrain download destinations, and sanitize output filenames before wider deployment.

## Reference(s):

- [CNKI Download Skill Page](https://clawhub.ai/lfp1979/skills/cnki-download)
- [Config JSON Schema](references/config-schema.md)
- [Microsoft Edge](https://www.microsoft.com/edge)
- [CNKI](https://www.cnki.net/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON configuration and download PDF files under the skill's download directory.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
