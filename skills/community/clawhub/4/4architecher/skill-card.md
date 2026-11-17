## Description:

基于产品需求生成中文 4A 分层架构蓝图，通过苏格拉底式澄清逐步产出 4A 总览主图、业务架构图、应用架构图、数据架构图、技术架构图及配套文档，图形默认以可导入 draw.io 的 XML 代码块呈现。

This skill is ready for commercial/non-commercial use.

## Publisher:

[doertiger](https://clawhub.ai/user/doertiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, solution architects, and enterprise architects use this skill to turn product requirements into structured 4A architecture deliverables for planning, design alignment, technical review, procurement, or roadmap discussion. It is especially oriented toward Chinese-language enterprise architecture work where draw.io XML diagrams and supporting documentation are expected outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Architecture recommendations may be incomplete or misleading when the product boundary, target users, or business goals are unclear.

Mitigation: Confirm the product scope and key assumptions early, then review each generated diagram and document before using them for design or compliance decisions.

Risk: Externally sourced claims about regulations, standards, products, or market facts may be stale, misapplied, or insufficient for the user's jurisdiction or industry.

Mitigation: Use current authoritative sources, record provenance for key claims, and separate user-provided facts, external evidence, and model inferences in the final deliverable.

Risk: Generated draw.io XML can encode an incorrect architecture even when the file format is importable.

Mitigation: Validate the imported diagrams against the 4A mapping checks and have domain owners review business, application, data, and technology relationships.

## Reference(s):

- [4A Framework Reference](references/4a-framework.md)
- [Authority Validation Reference](references/authority-validation.md)
- [Deliverable Template](references/deliverable-template.md)
- [Layered Architecture Spec](references/layered-architecture-spec.md)
- [Draw.io XML Template](references/drawio-xml-template.md)
- [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html)
- [The Open Group TOGAF Standards](https://publications.opengroup.org/standards/togaf)
- [Business Architecture Guild](https://www.businessarchitectureguild.org/)
- [DAMA-DMBOK](https://dama.org/learning-resources/dama-data-management-body-of-knowledge-dmbok/)
- [NIST AI Risk Management Framework](https://www.nist.gov/publications/artificial-intelligence-riREDACTED-SECRET)
- [NIST Zero Trust Architecture](https://www.nist.gov/publications/zero-trust-architecture)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown containing prose, tables, and fenced draw.io XML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to distinguish confirmed information, assumptions, external evidence, model inferences, unresolved gaps, and next-step recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
