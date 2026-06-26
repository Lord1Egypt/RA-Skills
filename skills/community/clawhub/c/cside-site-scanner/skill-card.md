## Description: <br>
Scan any website for third-party scripts, trackers, and security risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swijckmans](https://clawhub.ai/user/swijckmans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security teams, and site owners use this skill to audit a web page for third-party scripts, security headers, cookies, storage usage, tracker domains, fingerprinting indicators, and PCI DSS 4.0 relevance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Website scans can expose privacy-sensitive page data such as screenshots, cookies, storage metadata, and page context. <br>
Mitigation: Use the skill only on sites you own or have permission to test, prefer a clean or unauthenticated browser profile, and avoid including cookie values, tokens, or full browser storage contents unless you can handle that data safely. <br>
Risk: The report is a point-in-time snapshot from one page load and does not establish compliance. <br>
Mitigation: Present results as triage guidance, include the scan limitations, and use continuous or formal compliance tooling for production assurance. <br>


## Reference(s): <br>
- [Fingerprinting Detection Patterns](references/fingerprinting-patterns.md) <br>
- [Known Third-Party Domain Categories](references/tracker-domains.md) <br>
- [cside](https://cside.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report in a chat message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a security grade, script and domain inventory, risk flags, header review, cookie summary, fingerprinting findings, PCI relevance, and scan limitations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
