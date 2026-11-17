## Description:

Turn a scanned book (PDF or DjVu, up to 1,000 pages) into a clean, searchable PDF for Kindle and e-readers with FixMyScan. Use when the user wants to fix, clean up, OCR, crop, straighten, split two-page spreads in, or convert a scanned book for an e-reader.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fixmyscan](https://clawhub.ai/user/fixmyscan)

### License/Terms of Use:

MIT-0

## Use Case:

External users can submit scanned PDF or DjVu books for cleanup and OCR, then review scan progress or previews and retrieve the searchable PDF. Developers can also integrate the processing workflow through the FixMyScan MCP server or REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends the complete book to an external processor, and the security review says this disclosure may not be clear enough.

Mitigation: Before submitting a book, tell the user that the complete document will be sent to FixMyScan and get their agreement.

## Reference(s):

- [FixMyScan ClawHub skill page](https://clawhub.ai/fixmyscan/skills/fixmyscan)
- [FixMyScan MCP server](https://mcp.fixmyscan.com/mcp)
- [FixMyScan REST API reference (OpenAPI)](https://api.fixmyscan.com/openapi.json)
- [FixMyScan full documentation](https://fixmyscan.com/llms-full.txt)

## Skill Output:

**Output Type(s):** [API Calls, Files, Guidance]

**Output Format:** [Searchable PDF, scan status, and optional page previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts PDF or DjVu books up to 1,000 pages; supports margin trimming, spread splitting, black-and-white or greyscale output, and automatic or specified language.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
