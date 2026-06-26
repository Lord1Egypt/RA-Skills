## Description: <br>
AhaPoint 生成专家按 AhaPoints Protocol v1.0 标准，挖掘并生成带确权元数据、知识图谱和优先权声明的独立 AhaPoint 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyuxing](https://clawhub.ai/user/lyuxing) <br>

### License/Terms of Use: <br>
CC-BY-4.0 <br>


## Use Case: <br>
External users and developers use this skill to research a domain, identify pain, innovation, or fun points, and turn them into standardized AhaPoint Markdown reports with APS v1.0 metadata. It supports single-point deep generation, batch idea exploration, and formatting an existing idea into the AhaPoint template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include author identifiers or contact details for private ideas. <br>
Mitigation: Use a pseudonym or omit contact details when recording sensitive or early-stage ideas. <br>
Risk: The skill may save persistent Markdown reports and examples reference a hard-coded local path. <br>
Mitigation: Confirm the intended save directory before use and avoid the hard-coded /Users/olivia path unless it is actually intended. <br>
Risk: Browser-based research may surface incomplete or inaccurate claims that affect the generated report. <br>
Mitigation: Review cited sources and validate important claims before relying on the generated AhaPoint report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lyuxing/aha-point-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with YAML metadata blocks, Mermaid diagrams, and registry updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May browse the web for research and save persistent AhaPoint report files under an ahapoints-protocol directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
