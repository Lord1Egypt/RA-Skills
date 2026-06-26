## Description: <br>
Chief is an HR deep organizational diagnosis agent that turns complex people, culture, compensation, readiness, and talent review questions into structured diagnostic reports using a seven-step analysis flow, Socratic audit, and an iceberg model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR leaders, HRBPs, and organization consultants use this skill for deep diagnosis of ambiguous or multi-factor HR issues such as attrition, culture gaps, leadership assessment, compensation benchmarking, change readiness, and talent review. It is not intended for routine HR Q&A, policy lookup, template generation, or email drafting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive HR case details and internal analysis through case memory or failure-taxonomy records. <br>
Mitigation: Use only with clear local file boundaries, opt-in storage, raw reasoning retention disabled, and documented retention and deletion controls. <br>
Risk: HR diagnostics may involve identifiable employee, compensation, misconduct, legal, or leadership-risk information. <br>
Mitigation: Minimize and de-identify inputs, avoid sensitive details unless access controls are acceptable, and require human review for legal, layoff, arbitration, major compensation, leadership-risk, or organization-change outputs. <br>
Risk: External search, meeting analytics, or HR integrations could expose organizational data outside the local environment. <br>
Mitigation: Require explicit approval before any external tool or integration receives organizational data, and skip unavailable external skills rather than silently broadening data sharing. <br>


## Reference(s): <br>
- [Chief ClawHub release page](https://clawhub.ai/tuobadaidai/chief) <br>
- [DiTing skill definition](artifact/SKILL.md) <br>
- [Enhanced HR analysis frameworks](artifact/references/enhanced-frameworks.md) <br>
- [Evaluator quality specification](artifact/references/evaluator-spec.md) <br>
- [Few-shot output examples](artifact/references/few-shot-examples.md) <br>
- [Multi-agent aggregation strategy](artifact/references/multi-agent-aggregation.md) <br>
- [State pruning specification](artifact/references/state-pruning-spec.md) <br>
- [XML scaffold specification](artifact/references/xml-scaffold-spec.md) <br>
- [Architecture validation record](artifact/references/v6-architecture-validation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and concise guidance, with optional JSON case-memory records and shell commands for setup or citation checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include confidence labels, citations, risk flags requiring human review, and prioritized P0/P1/P2 recommendations.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
