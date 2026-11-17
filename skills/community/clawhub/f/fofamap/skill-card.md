## Description:

fofamap turns FOFA-based security reconnaissance requests into deterministic asset discovery, host profiling, distribution statistics, icon_hash generation, query refinement, monitoring, and cautious follow-up triage workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asaotomo](https://clawhub.ai/user/asaotomo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and authorized operators use this skill to translate FOFA reconnaissance requests into permission-aware searches, host profiles, distribution summaries, recurring monitoring reports, and exportable handoff files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FOFA credentials could be sent to a configured endpoint if FOFA_BASE_URL is changed.

Mitigation: Leave FOFA_BASE_URL unset unless the endpoint is intentionally selected and trusted.

Risk: Active follow-up can run a locally spoofed nuclei executable.

Mitigation: Run nuclei only from trusted working directories and confirm authorization before active scanning.

Risk: CSV and XLSX exports contain internet-derived data.

Mitigation: Treat exported spreadsheets as untrusted before opening or sharing them.

## Reference(s):

- [fofamap ClawHub listing](https://clawhub.ai/asaotomo/skills/fofamap)
- [Setup](references/setup.md)
- [Query Playbook](references/query-playbook.md)
- [Analysis Playbook](references/analysis-playbook.md)
- [Permission Playbook](references/permission-playbook.md)
- [Monitor Playbook](references/monitor-playbook.md)
- [Red Team Hunt Playbook](references/redteam-hunt-playbook.md)
- [Report Templates](references/report-templates.md)
- [Evolution Playbook](references/evolution-playbook.md)
- [Syntax Arsenal](references/syntax-arsenal.md)
- [Syntax Corpus](references/syntax-corpus.tsv)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON helper results, and optional CSV, XLSX, targets.txt, and Markdown report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FOFA_EMAIL, FOFA_API_KEY, and python3; FOFA_BASE_URL is optional and should remain unset unless a trusted FOFA-compatible endpoint is intended.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
