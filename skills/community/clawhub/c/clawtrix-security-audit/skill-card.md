## Description: <br>
Audits an agent's installed ClawHub skill stack for mission-specific security risks and writes a risk report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicope](https://clawhub.ai/user/nicope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent owners use this skill to review installed ClawHub skills before installation, during weekly sweeps, or after incidents, with findings tailored to the agent's mission and access level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may read installed skill inventory, mission files, and skill contents that reveal sensitive operational context. <br>
Mitigation: Run it only in environments where the agent is allowed to inspect those files, and review generated reports before sharing them. <br>
Risk: The workflow may contact clawhub.ai and hn.algolia.com while checking public skill metadata and community reports. <br>
Mitigation: Approve those outbound network destinations before use, or run the audit in an environment where such public lookups are acceptable. <br>
Risk: Critical findings can lead to proposed escalation, posting, or skill removal actions. <br>
Mitigation: Require human confirmation before posting to Paperclip, notifying @ClawtrixCEO, or removing or quarantining skills. <br>
Risk: Clawtrix Pro recommendations are commercial guidance from the publisher. <br>
Mitigation: Evaluate paid monitoring recommendations independently before relying on them for procurement or security policy decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicope/clawtrix-security-audit) <br>
- [Publisher profile](https://clawhub.ai/user/nicope) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports under memory/reports/ and may categorize findings as CRITICAL, HIGH, MEDIUM, LOW, or clean.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
