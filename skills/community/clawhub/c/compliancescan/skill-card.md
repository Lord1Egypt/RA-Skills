## Description: <br>
Scans public websites for GDPR/DSGVO compliance from the terminal and reports a 0-100 score plus key findings such as trackers, cookies, consent banner status, pre-consent tracking, fonts, and third-party transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2g4y1](https://clawhub.ai/user/2g4y1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and compliance reviewers use this skill to run a limited public Quick-Scan or authenticated full scan for GDPR/DSGVO, cookie, tracker, consent-banner, external-font, and related website compliance signals. The result is an automated technical indication and should not be treated as legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan output is an automated technical indication and can be incomplete or stale, especially for cached Quick-Scan results. <br>
Mitigation: State scan scope and cache status when present, report only fields returned by the API, and direct users to a full scan or legal review for decisions. <br>
Risk: The skill sends target URLs to an external scanning service and anonymous scans are rate limited. <br>
Mitigation: Validate the target URL, start only one scan per invocation, respect retry and rate-limit guidance, and avoid scanning private or internal addresses. <br>
Risk: Authenticated full scans use an API key and may consume credits or expose account-scoped capabilities. <br>
Mitigation: Use the key only when configured, never print credentials or authorization headers, and avoid automatic retries for write operations. <br>


## Reference(s): <br>
- [Compliancescan ClawHub skill page](https://clawhub.ai/2g4y1/skills/compliancescan) <br>
- [Compliancescan homepage](https://compliancescan.eu) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Concise Markdown with terminal commands and scan-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Replies in the user's language; Quick-Scan output is limited to fields returned by the public scan API, and authenticated full scans require COMPLIANCESCAN_API_KEY.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
