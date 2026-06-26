## Description: <br>
Analyze ad creatives from a local directory of images, videos, or transcripts to score creative quality, messaging effectiveness, CTA strength, and engagement potential, then summarize cross-creative patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baitoxkevin](https://clawhub.ai/user/baitoxkevin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing teams, creative strategists, and growth operators use this skill to review competitor or reference ad creatives, identify strong hooks and CTA patterns, and prioritize assets for testing or iteration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects a user-provided local folder, which could expose unintended files if pointed at a broad Downloads, Desktop, client, or project directory. <br>
Mitigation: Use a dedicated folder containing only the ad images, videos, transcripts, and metadata intended for analysis. <br>
Risk: Creative scores, target-audience labels, emotion appeals, and performance recommendations are subjective model judgments. <br>
Mitigation: Review the generated analysis before using it for spend allocation, campaign changes, or client-facing recommendations. <br>


## Reference(s): <br>
- [Ad Creative Analysis Framework](references/analysis-framework.md) <br>
- [ClawHub skill page](https://clawhub.ai/baitoxkevin/ad-creative-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, analysis, guidance] <br>
**Output Format:** [JSON array with per-creative analysis objects and a final cross-creative summary object, often accompanied by concise explanatory text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Per-creative outputs include filenames, formats, dimensions, inferred objectives, platform fit, scores, extracted hooks, CTA details, emotion appeals, and unreadable-file status when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
