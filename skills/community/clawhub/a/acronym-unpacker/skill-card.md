## Description: <br>
Disambiguate medical acronyms and abbreviations with context-aware full form lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians, healthcare operations teams, and developers can use this local helper to expand a small set of medical acronyms and compare likely meanings by clinical context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical acronym expansions may be incomplete or contextually wrong if treated as clinical advice. <br>
Mitigation: Use the output as a convenience reference only and verify medical meaning against authoritative clinical sources before acting on it. <br>
Risk: Documentation claims broader features than the artifact demonstrates. <br>
Mitigation: Validate behavior locally against the included script and supported acronym database before relying on advanced features such as batch processing or feedback learning. <br>
Risk: A future or external requirements.txt could introduce unreviewed dependencies. <br>
Mitigation: Review dependency files before installation and prefer running the included no-dependency Python script directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/acronym-unpacker) <br>
- [Publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns ranked acronym expansions with confidence scores for supported acronyms and contexts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
