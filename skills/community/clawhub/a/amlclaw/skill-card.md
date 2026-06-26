## Description: <br>
AMLClaw helps agents screen blockchain addresses for crypto AML risk, generate machine-readable detection rules, and draft jurisdiction-specific compliance policy documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npc7](https://clawhub.ai/user/npc7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Compliance, risk, and engineering teams use this skill to investigate crypto wallet exposure, prepare AML screening reports, maintain detection rules, and draft policy templates for virtual-asset workflows. <br>

### Deployment Geography for Use: <br>
Global, with bundled defaults for Singapore MAS, Hong Kong SFC, and Dubai VARA workflows. <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends blockchain address screening requests to a third-party TrustIn data service and can use an API key for unmasked production data. <br>
Mitigation: Review the TrustIn data-sharing path before installation, store API keys outside shared files, and confirm which addresses and jurisdictions are appropriate for external screening. <br>
Risk: Generated graph data, rules, and reports can contain sensitive compliance findings or customer-related investigation details. <br>
Mitigation: Keep generated graph and report files out of public repositories, apply internal data-retention controls, and require explicit user confirmation before saving or copying defaults into a working directory. <br>
Risk: Bundled jurisdictional defaults and policy drafts may not match an organization's current legal obligations. <br>
Mitigation: Have qualified compliance or legal reviewers approve jurisdiction-specific rules, thresholds, and policy language before operational use. <br>
Risk: The evidence security summary flags law-enforcement seizure and spyware reference material as content that is not suitable for ordinary compliance workflows. <br>
Mitigation: Limit those materials to approved investigative contexts and avoid using them as normal AML policy or screening guidance. <br>


## Reference(s): <br>
- [TrustIn Label Taxonomy](references/trustin-labels.md) <br>
- [FATF 40 Recommendations 2025](references/fatf/FATF-001-40-Recommendations-2025.md) <br>
- [FATF VA/VASP Guidance 2021](references/fatf/FATF-002-VA-VASP-Guidance-2021.md) <br>
- [FATF Targeted Update VA/VASP 2025](references/fatf/FATF-003-Targeted-Update-VA-VASP-2025.md) <br>
- [FATF Travel Rule Best Practices 2025](references/fatf/FATF-005-Travel-Rule-Best-Practices-2025.md) <br>
- [OFAC Virtual Currency Guidance](references/sanctions/SANC-002-OFAC-Virtual-Currency-Guidance.md) <br>
- [UN Consolidated Sanctions](references/sanctions/SANC-003-UN-Consolidated-Sanctions.md) <br>
- [Singapore DPT Compliance Guide](references/singapore/新加坡DPT持牌机构链上风控合规配置指南.md) <br>
- [Hong Kong SFC Compliance Guide](references/hongkong/香港机构链上风控合规配置指南.md) <br>
- [Dubai VARA Compliance Guide](references/dubai/迪拜机构链上风控合规配置指南.md) <br>
- [TrustIn KYA API](https://trustin.info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and policy drafts, JSON rules and screening data, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save local rules, graph data, and screening reports when the agent follows the skill workflow.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
