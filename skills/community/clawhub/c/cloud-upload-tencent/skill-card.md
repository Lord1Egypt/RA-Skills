## Description:

Guides agents through uploading local files to Tencent Cloud Object Storage (COS), generating download links, and preparing image or document preview links across macOS, Linux, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realorange1994](https://clawhub.ai/user/realorange1994)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they need an agent to provide Tencent COS upload commands, credential setup guidance, sharing-link options, and result formatting for file backup, public sharing, or static asset storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Upload or sharing guidance can expose local files unintentionally.

Mitigation: Use the skill only for files intended for Tencent COS and prefer private buckets with short-lived presigned URLs.

Risk: Cloud credentials can be exposed if entered directly into commands or reused broadly.

Mitigation: Use narrowly scoped temporary credentials, keep SecretKey values out of command lines, and review environment handling before execution.

Risk: Installing upload dependencies without review can introduce supply-chain risk.

Mitigation: Install dependencies in an isolated environment and prefer reviewed pinned versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realorange1994/skills/cloud-upload-tencent)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown with bash, PowerShell, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment variable guidance, COS bucket and region fields, upload result summaries, and public or presigned link options.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
