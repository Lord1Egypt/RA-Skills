## Description:

Compiles locally recorded AI coding-agent usage into an append-only ledger, prices it at list API rates, attributes it by account and billing plan, and renders dashboards, study packages, ledger documents, exports, and query results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[completetech](https://clawhub.ai/user/completetech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering managers, operations teams, and finance reviewers use this skill to inventory local AI coding-agent usage, estimate API-equivalent cost, compare subscriptions, validate coverage, and prepare anonymized usage evidence for internal or external reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive local AI-agent transcripts and tool databases.

Mitigation: Install only when that local read access is acceptable, keep optional high-sensitivity features off unless needed, and review the disclosed scan scope before first use.

Risk: Prompt capture, credential-derived account labeling, raw-log archiving, all-profile scanning, WSL, SSH hosts, and scheduled refresh can expand the data collected or the systems reached.

Mitigation: Leave those features disabled unless specifically required; the artifact evidence describes them as opt-in and operator-controlled.

Risk: Generated packages can expose private account, host, organization, path, or prompt details if shared without review.

Mitigation: Use the anonymized copy for publication and run the provided publish check before sharing generated outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/completetech/skills/ai-usage-ledger-skill)
- [Project Homepage](https://github.com/CompleteTech-LLC/ai-usage-ledger-skill)
- [Harness and Runtime Catalog](references/harness-catalog.md)
- [Log Formats](references/log-formats.md)
- [Discovery and Account Attribution](references/discovery.md)
- [Ledger Document Catalog](references/ledger-document-catalog.md)
- [Pitfalls That Produce Wrong Numbers](references/pitfalls.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, CSV, HTML, PDF, DOCX]

**Output Format:** [Markdown guidance with inline shell commands, plus generated ledger artifacts as SQLite, JSON/JSONL, CSV, HTML, PDF, and DOCX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The ledger is local and append-only; prompt capture, credential-derived account labeling, raw-log archiving, all-profile scanning, WSL, SSH hosts, anonymization, and scheduled refresh are operator-controlled.]

## Skill Version(s):

1.5.11 (source: evidence.release.version, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
