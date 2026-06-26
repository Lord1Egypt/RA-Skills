## Description: <br>
Generates company aliases and matching keywords from enterprise names using brand mappings, core-term extraction, filtering rules, and optional public web lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyqdq888](https://clawhub.ai/user/hyqdq888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data operators use this skill to normalize enterprise names into concise aliases or keywords for matching, import, and deduplication workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional web lookup helpers may send company names to third-party public services, which can expose sensitive or pre-public names in service logs. <br>
Mitigation: Keep offline mode enabled for confidential company names, and only enable web lookups when those names are acceptable to disclose to external services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hyqdq888/generate-alias) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Release changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Plain text aliases separated by vertical bars, with Python API and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default operation is offline; optional web lookup helpers may query public services when enabled.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
