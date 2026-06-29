## Description: <br>
Harness-neutral community incident reporting for AI agents. Contribute to collective security by reporting threats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use Clawtributor to draft structured reports for malicious prompts, vulnerable skills or plugins, and tampering attempts. Reports stay local until the user reviews the exact contents and approves manual browser submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security reports may contain sensitive evidence such as prompts, indicators, or affected package details. <br>
Mitigation: Review and sanitize every report before submission, and only approve browser submission when the exact contents are safe to share with maintainers. <br>
Risk: The skill can activate during general security-reporting requests and may prepare reports that leave the host after user action. <br>
Mitigation: Keep drafts local by default, require explicit approval for each submission, and use the manual browser form only after review. <br>


## Reference(s): <br>
- [ClawSec Homepage](https://clawsec.prompt.security) <br>
- [Prompt Security](https://prompt.security) <br>
- [Security Incident Report Form](https://github.com/prompt-security/clawsec/issues/new?template=security_incident_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON report templates and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local report drafts and state-tracking guidance; submission remains manual and approval-gated.] <br>

## Skill Version(s): <br>
0.0.9 (source: frontmatter, skill.json, changelog released 2026-06-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
