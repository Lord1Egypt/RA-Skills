## Description: <br>
Detector AI detects AI-generated text with multiple analysis methods, including perplexity analysis, burstiness detection, readability scoring, and AI fingerprint detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze supplied text for signals associated with AI-generated writing and receive a probability score, component analyses, and plain-language interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heuristic AI detection results can be wrong and should not be treated as proof of authorship. <br>
Mitigation: Use the score and component findings as guidance, review the underlying text context, and avoid making consequential decisions from this result alone. <br>
Risk: The script can read a user-supplied local file path for analysis. <br>
Mitigation: Provide only text or files intentionally selected for analysis and review the file path before execution. <br>


## Reference(s): <br>
- [AI Writing Patterns Reference](references/ai_patterns.md) <br>
- [Detector AI on ClawHub](https://clawhub.ai/openlark/detector-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Plain-language report or JSON analysis from the local detection script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports heuristic AI probability, verdict, confidence, text statistics, perplexity, burstiness, readability, and AI fingerprint findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
