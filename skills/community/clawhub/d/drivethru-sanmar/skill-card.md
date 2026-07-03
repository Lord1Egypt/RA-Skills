## Description: <br>
Deterministic SanMar API toolkit that wraps SanMar SOAP web services and PromoStandards order-shipment services behind typed CLI tools for product search, inventory, pricing, cart validation, purchase orders, order tracking, PO PDF parsing, and mainframe color-code resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmtucker](https://clawhub.ai/user/zmtucker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and purchasing agents use this skill to query SanMar catalog, inventory, pricing, and shipping data and to prepare or submit SanMar order workflows through deterministic CLI actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real SanMar credentials may be exposed in tool output or retained in raw payloads. <br>
Mitigation: Use platform secret storage, prefer environment variables over inline JSON, redact raw payloads before retention, and avoid logging outputs that may include credentials. <br>
Risk: The skill can perform business-write actions such as purchase-order submission. <br>
Mitigation: Use least-privilege SanMar credentials, run validation and dry-run previews first, and require explicit user confirmation before live submit actions. <br>
Risk: Parsed purchase-order PDFs are heuristic drafts and may contain incorrect fields. <br>
Mitigation: Show parsed PO details to the user and obtain approval before submitting any generated purchase order. <br>
Risk: Browser-driven return processing is partially implemented and final return submission is not supported by the artifact. <br>
Mitigation: Treat return output as a dry-run or not-implemented result unless the implementation is completed and tested against an intentional real return. <br>


## Reference(s): <br>
- [Drivethru Sanmar ClawHub release](https://clawhub.ai/zmtucker/drivethru-sanmar) <br>
- [SanMar homepage](https://www.sanmar.com) <br>
- [SanMar runtime docs index](references/README.md) <br>
- [SanMar skill agent examples](references/examples.md) <br>
- [SanMar API auth, environments, and integration patterns](references/auth_and_patterns.md) <br>
- [SanMar SOAP Web Services API](references/web_services.md) <br>
- [SanMar Purchase Order Integration](references/purchase_orders.md) <br>
- [SanMar FTP Integration and File Feeds](references/ftp_feeds.md) <br>
- [SanMar portal process a return flow notes](references/returns_flow_notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON tool responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI actions read JSON from stdin and print one JSON object on stdout; side-effecting actions require explicit confirmation.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
