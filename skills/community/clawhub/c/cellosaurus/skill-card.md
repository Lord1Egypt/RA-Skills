## Description:

This third-party skill lets agents query Cellosaurus cell line data through a Xiaobenyang-hosted MCP API, including cell-line search, accession lookup, release information, disease-based lookup, tissue-based lookup, and available-field listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, bioinformatics users, and agents assisting with cell-line lookup use this skill to search Cellosaurus records, retrieve accession-level details, and inspect release or field metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cellosaurus query parameters are routed through the Xiaobenyang MCP gateway.

Mitigation: Use the skill only when this third-party data flow is acceptable, and avoid sending sensitive project or patient-context details in query terms.

Risk: The XBY_APIKEY may be persisted in plaintext in a local .env file.

Mitigation: Use a dedicated low-privilege key, restrict local file access, and rotate or remove the key after use.

Risk: Security evidence classifies this release as suspicious because the Cellosaurus-facing skill uses an unrelated gateway and has an identity mismatch.

Mitigation: Review the source and service trust relationship before installing or deploying this release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/cellosaurus)
- [Xiaobenyang API key portal](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or text summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY before tool calls can complete.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
