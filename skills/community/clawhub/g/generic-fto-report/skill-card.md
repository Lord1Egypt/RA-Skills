## Description:

Generates traceable general-industry FTO reports from risk-point Word documents and user-provided PatSnap search queries by retrieving patent results, claim 1 text, and AI-assisted infringement comparisons through PatSnap/Zhihuiya services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent risk analysts use this skill to turn target-product risk documents and manually supplied PatSnap search queries into FTO reports with patent lists, claim 1 retrieval, AI07 comparison records, and traceable supporting files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can send sensitive FTO inputs, search queries, claim text, and AI comparison prompts to PatSnap/Zhihuiya services.

Mitigation: Use only approved inputs for external processing, confirm the organization permits this data flow, and use a dedicated low-privilege API key.

Risk: API credentials may be mishandled because the skill relies on a local Zhihuiya configuration file.

Mitigation: Keep credentials out of committed or shared files, replace the placeholder only in a private runtime config, and verify no real API key is present before redistribution.

Risk: The evidence reports inconsistent MCP/API setup guidance and weak credential-routing controls.

Mitigation: Verify the configured API base URL remains the intended HTTPS vendor host and avoid broad external MCP services unless the publisher clarifies exactly which service is required.

Risk: FTO conclusions can be misleading if search queries, claim 1 retrieval, or AI07 outputs are incomplete or treated as final legal analysis.

Mitigation: Require analyst-provided search queries, preserve trace files, base conclusions on retrieved claim 1 text, treat AI07 as auxiliary, and route final reports through qualified legal review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/generic-fto-report)
- [PatSnap/Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [PatSnap developer documentation](https://open.patsnap.com/devportal)
- [Authentication guide](https://open.zhihuiya.com/devportal/guides/authentication)
- [MCP server marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)
- [API call policy](references/api_call_policy.md)
- [API reference](references/api_reference.md)
- [Report requirements](references/report_requirements.md)
- [Claim chart schema](references/claim_chart_schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands plus generated JSON, HTML, and DOCX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a risk-point DOCX input, at least one user-supplied PatSnap query, and PatSnap/Zhihuiya API credentials before live retrieval and comparison can run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
