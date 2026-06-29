## Description: <br>
Scan any public web page for WCAG 2.2 accessibility issues, with clear limits on what automated static checks can and cannot detect. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foomworks](https://clawhub.ai/user/foomworks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and accessibility reviewers use this skill to scan a public URL for static HTML accessibility findings mapped to WCAG success criteria, then review concrete remediation guidance and scan limitations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted service receives the public URL being scanned. <br>
Mitigation: Use the skill only for public pages and avoid submitting private, internal, or sensitive URLs. <br>
Risk: Automated static scans can miss issues such as color contrast, keyboard behavior, focus handling, JavaScript-rendered content, and legal compliance concerns. <br>
Mitigation: Treat results as a starting point and follow up with browser-based testing, assistive technology checks, and human accessibility review. <br>


## Reference(s): <br>
- [A11y Scan ClawHub listing](https://clawhub.ai/foomworks/skills/a11y-scan) <br>
- [A11y Scan service homepage](https://a11y-scan.foomworks.workers.dev) <br>
- [A11y Scan MCP endpoint](https://a11y-scan.foomworks.workers.dev/mcp) <br>
- [A11y Scan OpenAPI descriptor](https://a11y-scan.foomworks.workers.dev/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with curl examples and JSON responses from REST or MCP calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns automated accessibility findings, WCAG mappings, impact counts, remediation notes, summaries, and coverage limitations for a single public URL.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
