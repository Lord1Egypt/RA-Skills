## Description: <br>
This skill helps agents compress long Chinese text semantically with anchor checks and iterative validation so key information is preserved while token use is reduced. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and knowledge managers use this skill to shorten prompts, documentation, reports, and conversation history while preserving named entities, numbers, dates, and other anchors. It is intended for non-critical text where semantic compression and human or model review are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs semantic compression rather than byte-level lossless compression, so important nuance may be lost or changed. <br>
Mitigation: Use anchor extraction and iterative validation, keep the original text available, and manually review compressed output before relying on it. <br>
Risk: Server security evidence flags broad file access and command-execution authority that the Markdown-driven behavior does not clearly require. <br>
Mitigation: Run the skill only in constrained agent environments and avoid granting command execution or broad write access unless a specific workflow requires it. <br>
Risk: Compression is inappropriate for secrets, regulated records, legal, financial, medical, or security-critical instructions. <br>
Mitigation: Do not process those materials with this skill unless access, storage, and review controls are explicitly in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/file-compressor-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text with compressed content, anchor checks, validation notes, and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The free edition focuses on L1 and L2 semantic compression and excludes L3, L4, batch compression, custom anchor strategies, and advanced quality reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
