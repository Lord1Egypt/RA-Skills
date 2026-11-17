## Description:

Uploads local contract files to AnyShare, applies a contract-rule review template through the AnyShare review skill, saves the review report, and generates a share link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyshare-aishu](https://clawhub.ai/user/anyshare-aishu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and contract operations teams use this skill to upload contracts to AnyShare, run structured rule-based review, store the original document and review report in a dated folder hierarchy, and share the resulting report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles confidential contracts, AnyShare credentials, generated review reports, and share links.

Mitigation: Install only for workflows where uploading contracts to AnyShare is intended, use narrowly scoped short-lived credentials where possible, and require manual confirmation before uploading documents or generating links.

Risk: Unsafe handling of untrusted or quote-containing filenames may affect command interpolation.

Mitigation: Avoid untrusted or quote-containing filenames until the interpolation issue identified by security evidence is fixed.

Risk: AI-generated contract review can be incomplete or incorrect.

Mitigation: Treat the report as review assistance and require qualified human review before business or legal action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyshare-aishu/skills/as-contract-rule-review)
- [AnyShare MCP endpoint](https://anyshare.aishu.cn/asmcp/)
- [AnyShare default template API](https://anyshare.aishu.cn/api/intelli-search/v1/skills/templates/default?skill_name=__规则审阅__1)
- [AnyShare temporary-area API](https://anyshare.aishu.cn/api/intelli-search/v1/temporary-area)
- [AnyShare index-check API](https://anyshare.aishu.cn/api/intelli-search/v1/index-check?target_index=pageindex)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown review report with shell command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an AnyShare folder structure, uploads the source contract and review report, and returns a share link when the AnyShare workflow succeeds.]

## Skill Version(s):

2.0.0 (source: frontmatter); release version 1.0.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
