## Description: <br>
Provides pronunciation guidance for complex drug generic names using IPA transcriptions, syllable breakdowns, emphasis markers, and SSML-style audio markers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up pronunciation guidance for supported medication names, including IPA notation, syllables, emphasis, common errors, and optional SSML-style markers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pronunciation coverage may be incomplete or overstated for real clinical use. <br>
Mitigation: Treat the data as a small local lookup aid and verify pronunciations against authoritative clinical or pharmaceutical references before using them in clinical workflows. <br>
Risk: The optional --output path can overwrite writable files. <br>
Mitigation: Use --output only with an intended safe path inside the workspace and review the destination before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AIPOCH-AI/drug-pronunciation) <br>
- [AIPOCH-AI Publisher Profile](https://clawhub.ai/user/AIPOCH-AI) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON object or plain text list, optionally written to a JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes IPA transcription, syllable breakdown, emphasis, common pronunciation errors, and optional SSML-style audio marker in detailed output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
