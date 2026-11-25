## Description:

Offline AI-search readiness (GEO) audit of saved page HTML, robots.txt and llms.txt — checks whether ChatGPT, Perplexity, Claude and Google AI crawlers can reach, parse and cite the page. Zero network access. Use when the user asks whether their site is visible to AI answer engines or provides saved HTML/robots files to audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site owners use the skill to review saved page HTML, robots.txt, and llms.txt for AI-search readiness. The JSON findings help them identify crawler access, metadata, structured-data, and content issues in the supplied files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is benign with medium confidence because component coverage is 50% and JavaScript analysis is partial.

Mitigation: Treat the scan as limited assurance and consider the coverage gap when deciding whether to install.

Risk: The audit examines supplied snapshots and simplifies robots.txt matching, so its results do not establish live crawler access or actual AI citations.

Mitigation: Use the report as a local-file screening result and verify live behavior separately when that assurance is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nenadzivotic/skills/geo-audit-lite)
- [Publisher profile](https://clawhub.ai/user/nenadzivotic)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured JSON report with pass, warn, fail, and informational checks plus remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-supplied local files only; does not modify files or access the network.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
