## Description:

Creates a concise A-share company brief from a company name or code, covering disclosed identity and financial facts, dated events, directly checked risks, and blank fields for human opinions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and business professionals can prepare a quick pre-meeting or client brief on one or more A-share companies. The brief presents sourced facts and leaves its opinion fields blank; it is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags possible transmission of an API key to a destination supplied by an external catalog.

Mitigation: Avoid installation until the credential destination has been independently reviewed and shown to be necessary.

Risk: The security assessment flags MCP discovery behavior that does not match the stated company-briefing purpose.

Mitigation: Review that behavior independently and confirm it is necessary before use.

Risk: The installer is unpinned, creating an additional supply-chain risk.

Mitigation: Pin the installer version and review the installer source before installation.

Risk: Security scan coverage is partial, and unresolved local references limit the assessment.

Mitigation: Resolve the references and complete an independent security review before use; the current results establish neither safety nor malicious intent.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-tear-sheet)
- [Cue MCP configuration](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader configuration](https://cuecue.cn/hub/omni-reader)
- [Cue API key setup](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Structured data, Text]

**Output Format:** [A Markdown company brief with a JSONL source index and a text progress log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fixed five-section brief for up to five companies; factual claims are expected to carry disclosure anchors, and the opinion section remains blank for a human.]

## Skill Version(s):

0.1.22 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
