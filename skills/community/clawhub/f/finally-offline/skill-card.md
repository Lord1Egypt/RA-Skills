## Description:

Browse culture articles and generate personalized HTML newsletters via MCP

This skill is ready for commercial/non-commercial use.

## Publisher:

[wn-fo](https://clawhub.ai/user/wn-fo)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to browse and search curated culture articles, subscribe an agent to the publication, generate branded HTML newsletter digests, and view subscription or reading reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the remote MCP service may send search terms, category interests, agent display name, subscription status, and reading activity to the service.

Mitigation: Avoid sensitive identifiers in the agent name, avoid entering sensitive search terms or interests, and remove the MCP configuration when the integration is no longer needed.

Risk: Digest generation depends on subscription state and remote service availability.

Mitigation: Confirm subscription status before requesting digest generation and keep alternate article browsing or search workflows available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wn-fo/skills/finally-offline)
- [Publisher Profile](https://clawhub.ai/user/wn-fo)
- [Publication](https://finallyoffline.com)
- [MCP Docs](https://finallyoffline.com/llms.txt)
- [Example Digest Output](https://finallyoffline.com/digest-example.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Article results, subscription reports, configuration JSON, and branded HTML newsletter digests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote MCP service; no API key is required for browsing, while digest generation requires subscription.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
