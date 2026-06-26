## Description: <br>
AI Density analyzes text and returns an objective 0-10 estimate of AI-generated content proportion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content reviewers use this skill to run local heuristic analysis of Chinese or English text and receive a 0-10 AI-likeness level with supporting dimension scores. The result is advisory and intended to support review, not to prove authorship. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heuristic AI-authorship estimates can be inaccurate or overconfident. <br>
Mitigation: Treat scores as advisory and do not use them as the sole basis for academic, employment, moderation, or compliance decisions. <br>
Risk: Out-of-range or very short text may produce weak signals. <br>
Mitigation: Follow the documented 10-10000 character input range and review dimension scores before relying on the level. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/ai-density) <br>
- [Artifact README](README.md) <br>
- [Artifact-declared project homepage](https://github.com/openclaw/ai-density) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Python DetectionResult object with level, score, confidence, dimension scores, description, warning, and processing time.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local standard-library heuristic for text inputs; README states a 10-10000 character input range.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
