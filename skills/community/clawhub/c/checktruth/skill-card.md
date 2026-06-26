## Description: <br>
Checktruth is a zero-configuration fact-checking skill that verifies answers, articles, and claims by decomposing statements, searching for evidence, and producing confidence-scored reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuehengzhang10-hub](https://clawhub.ai/user/xuehengzhang10-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check whether AI answers, articles, posts, or claims are supported by evidence. It is especially useful when a user wants a structured fact breakdown, confidence score, and source-backed explanation before relying on a statement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fact-checking may use web searches, so search queries or retrieved source context can expose parts of the topic being checked. <br>
Mitigation: Avoid submitting sensitive or confidential text for web-backed checks unless that disclosure is acceptable. <br>
Risk: Optional reference scripts can send user text to configured external AI providers and depend on Python packages selected by the user. <br>
Mitigation: Use the core zero-configuration workflow for normal use; only run the optional scripts after reviewing provider data policies and pinning or reviewing dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuehengzhang10-hub/checktruth) <br>
- [Skill instructions](SKILL.md) <br>
- [Requirements](docs/requirements.md) <br>
- [Skill design](docs/skill_design.md) <br>
- [Open-source research notes](docs/opensource_research.md) <br>
- [Optional reference code README](reference/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style fact-checking report with verdicts, confidence scores, source summaries, and consistency checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core use is zero configuration; optional reference scripts can write JSON results when manually run with user-provided API keys.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
