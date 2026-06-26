## Description: <br>
Chinese response-compression skill that helps agents answer more concisely in multiple compression modes, including a classical Chinese style, while preserving technical substance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garylooop](https://clawhub.ai/user/garylooop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to compress Chinese technical explanations, troubleshooting guidance, and operational responses to reduce token use while keeping key facts, code, identifiers, and configuration values intact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ultra and classical compression can remove context or nuance that is needed for high-stakes or step-by-step safety work. <br>
Mitigation: Use normal or clear responses for safety-critical, legal, medical, security-sensitive, or procedural instructions; review compressed outputs before acting. <br>
Risk: Document and index integrations may retain original text, compressed text, or mapping logs in local result objects or indexes. <br>
Mitigation: Avoid processing secrets or sensitive documents unless local retention is acceptable, and clear mappings or indexes after use when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/garylooop/ancient) <br>
- [Chinese compression guide](artifact/references/caveman_zh_cn.md) <br>
- [Classical enhancement guide](artifact/references/classical_enhancement.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Compressed Chinese prose, markdown examples, Python snippets, and command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports lite, standard, ultra, and classical compression modes; integrations can return compression metadata and mapping logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
