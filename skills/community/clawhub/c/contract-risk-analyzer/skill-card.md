## Description:

Contract Risk Analyzer reviews contract PDFs by extracting text, detecting contract type and language, and producing structured AI-assisted risk reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiji0802](https://clawhub.ai/user/qiji0802)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement teams, HR teams, freelancers, small businesses, and agents use this skill to review Chinese or English contract PDFs, summarize key terms, and identify high, medium, and low risk clauses. Its output is informational and does not replace qualified legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contracts may contain personal data, signatures, bank details, trade secrets, or confidential terms.

Mitigation: Review provider retention and compliance terms before use, and avoid highly sensitive contracts unless those terms are acceptable.

Risk: The skill sends extracted contract text to a configurable external AI endpoint.

Mitigation: Use only a trusted HTTPS endpoint and a dedicated low-privilege API key.

Risk: Subscription tokens and API credentials can be exposed if passed directly on the command line.

Mitigation: Prefer environment or session configuration for secrets and avoid command-line token arguments.

Risk: Generated contract artifacts can remain in /tmp/contracts after analysis.

Mitigation: Delete /tmp/contracts artifacts after reports are delivered.

## Reference(s):

- [Artifact README](artifact/README.md)
- [ClawHub Listing Evidence](artifact/CLAWHUB.md)
- [SkillHub Listing Evidence](artifact/SKILLHUB.md)
- [ClawHub Skill Page](https://clawhub.ai/qiji0802/skills/contract-risk-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, guidance]

**Output Format:** [Markdown risk report, JSON execution summary, and optional CSV export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include a contract summary, key terms when enabled by tier, risk findings grouped by severity, and a legal-advice disclaimer.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
