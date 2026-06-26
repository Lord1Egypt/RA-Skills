## Description: <br>
Detect whether text is human-written, AI-generated, AI-humanized, or lightly edited. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattc95](https://clawhub.ai/user/mattc95) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, editors, and reviewers use this skill to estimate whether submitted text appears human-written, AI-generated, AI-humanized, or lightly edited for review, moderation, writing checks, and compliance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text is sent to an external GPTHumanizer detection service and may contain sensitive, private, personal, or regulated information. <br>
Mitigation: Do not submit secrets, private documents, personal data, or regulated content unless the service terms have been reviewed and sharing is approved. <br>
Risk: AI-detection results are probabilistic and may be less reliable for short, mixed, heavily edited, or humanized text. <br>
Mitigation: Use the classification as a signal rather than proof, report probabilities when available, and avoid definitive claims from a single result. <br>


## Reference(s): <br>
- [GPTHumanizer](https://www.gpthumanizer.ai/) <br>
- [GPTHumanizer Detection API](https://detect.gpthumanizer.ai/api/detect_ai) <br>
- [API Reference](api.md) <br>
- [Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Analysis, API Calls, Guidance] <br>
**Output Format:** [Markdown or JSON-style text with classification labels and probabilities] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include predicted class, aggregated AI likelihood, per-class probabilities, original text, or API failure details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
