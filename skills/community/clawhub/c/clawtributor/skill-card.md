## Description: <br>
Community incident reporting for AI agents. Contribute to collective security by reporting threats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Developers, security teams, and agent operators use this skill to draft standardized reports for malicious prompts, vulnerable skills, and tampering attempts, then submit them manually after explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incident reports can contain sensitive security details or private evidence. <br>
Mitigation: Review and sanitize every generated report before sharing it outside the host. <br>
Risk: Submitting a report externally can disclose report contents to maintainers. <br>
Mitigation: Keep submission approval-gated and submit only after the user explicitly approves the exact report content. <br>
Risk: Standalone installation artifacts could be tampered with if release assets are fetched directly. <br>
Mitigation: Verify the signed release manifest, archive hash, SKILL.md, and skill.json checksums before trusting standalone artifacts. <br>


## Reference(s): <br>
- [Clawtributor ClawHub listing](https://clawhub.ai/davida-ps/clawtributor) <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>
- [Security Incident Report Form](https://github.com/prompt-security/clawsec/issues/new?template=security_incident_report.md) <br>
- [reporting.md](artifact/reporting.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with report JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local incident report drafts and approval-gated submission guidance; no automatic external submission is described by the security evidence.] <br>

## Skill Version(s): <br>
0.0.6 (source: frontmatter, skill.json, CHANGELOG, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
