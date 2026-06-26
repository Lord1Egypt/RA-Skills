## Description: <br>
Looks up domain WHOIS information, checks DMARC/SPF/DKIM email security, inspects TLS certificates, and can capture website screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxlderek](https://clawhub.ai/user/sxlderek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and support teams use this skill to inspect a domain, URL, or email domain and receive a domain-only report covering registration, DNS, email security, TLS, and optional screenshot evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain lookups and optional screenshots can disclose queried domains to external network services or visited sites. <br>
Mitigation: Use the skill only for domains the user is comfortable querying, and keep screenshot capture optional when browser tooling is not already available. <br>
Risk: The security evidence notes a limited robustness issue around custom screenshot output paths. <br>
Mitigation: Use the screenshot helper's default output path or tighten its path check before relying on custom output locations. <br>


## Reference(s): <br>
- [Skill Setup Notes](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Single final Markdown-style text report with an optional screenshot file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Buffers results before sending the final response; screenshot capture is optional and skipped when tooling is unavailable.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
