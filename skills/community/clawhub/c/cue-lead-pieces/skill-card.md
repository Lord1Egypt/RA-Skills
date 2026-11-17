## Description:

Reads public company filings into page-linked text, identifies potential credit signals, and checks cited quotes against the source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and research teams can use the skill to organize potential credit signals from public company filings and check each cited passage against its source page. It provides evidence for review, not investment or credit recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential safeguards can be bypassed when requesting external sources.

Mitigation: Review credentialed requests and require validated HTTPS destinations with redirect protection.

Risk: File writes can escape the intended data folder.

Mitigation: Enforce strict path containment for imported source IDs.

Risk: Altered financial quotations can pass verification, including meaningful numeric changes.

Mitigation: Independently check important figures against original filings and review corrected quotations.

Risk: Optional model settings send disclosure excerpts to the configured provider, and external companion services and Bridge code were not audited.

Mitigation: Use a configured provider and companion services only when appropriate for the disclosure material, and review them before credentialed use.

## Reference(s):

- [Cue Omni Reader setup](https://cuecue.cn/hub/omni-reader)
- [Cue data-MCP setup](https://cuecue.cn/hub/mcp)
- [Cue API key setup](https://cuecue.cn/hub/api-key)
- [Verification record and measured limits](artifact/references/verification.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Page-linked filing text, Markdown lead pieces and material catalogs, and JSON evidence or verification results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quotes are checked against the cited page and adjacent pages; if grounded page anchors are unavailable, references may be text-block numbers.]

## Skill Version(s):

0.4.35 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
