## Description:

AMLClaw helps agents screen crypto wallet addresses, generate machine-readable AML rules, and draft compliance policy documents using bundled regulatory references and TrustIn-backed graph data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npc7](https://clawhub.ai/user/npc7)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance developers, analysts, and agent operators use AMLClaw to run point-in-time wallet screening, maintain jurisdiction-specific AML rules, and produce Markdown screening reports or policy drafts for review.

### Deployment Geography for Use:

Global; the bundled default rulesets and policy templates focus on Singapore MAS, Hong Kong SFC, Dubai VARA, FATF, OFAC, and UN sanctions references.

## Known Risks and Mitigations:

Risk: Production API keys can be mishandled, especially when passed through command-line flags or stored in shared workspaces.

Mitigation: Use a private workspace, prefer environment-based secrets, avoid passing production API keys on the command line, and restrict access to generated files.

Risk: Screened addresses and graph data may be sent to TrustIn and saved locally in graph_data or reports outputs.

Mitigation: Apply data retention, access control, and workspace cleanup procedures before regulated or sensitive use.

Risk: API errors or missing graph data can make a screening result inconclusive even when the workflow continues.

Mitigation: Treat API failures, masked data, or missing graph details as inconclusive and require manual compliance review before clearing an address.

Risk: The release depends on unpinned Python package ranges.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [AMLClaw README](artifact/README.md)
- [TrustIn Label Taxonomy](artifact/references/trustin-labels.md)
- [FATF 40 Recommendations 2025](artifact/references/fatf/FATF-001-40-Recommendations-2025.md)
- [FATF VA/VASP Guidance 2021](artifact/references/fatf/FATF-002-VA-VASP-Guidance-2021.md)
- [FATF Targeted Update on Virtual Assets and VASPs 2025](artifact/references/fatf/FATF-003-Targeted-Update-VA-VASP-2025.md)
- [FATF Travel Rule Supervision Best Practices 2025](artifact/references/fatf/FATF-005-Travel-Rule-Best-Practices-2025.md)
- [OFAC Virtual Currency Sanctions Compliance Guidance](artifact/references/sanctions/SANC-002-OFAC-Virtual-Currency-Guidance.md)
- [UN Consolidated Sanctions List](artifact/references/sanctions/SANC-003-UN-Consolidated-Sanctions.md)
- [Singapore DPT AML Configuration Guide](artifact/references/singapore/新加坡DPT持牌机构链上风控合规配置指南.md)
- [Hong Kong Virtual Asset AML Configuration Guide](artifact/references/hongkong/香港机构链上风控合规配置指南.md)
- [Dubai Crypto AML Configuration Guide](artifact/references/dubai/迪拜机构链上风控合规配置指南.md)
- [TrustIn](https://trustin.info)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and policy drafts, JSON rules and screening data, plus shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local graph_data and reports files; screening quality depends on available TrustIn data, selected rules, and manual review.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
