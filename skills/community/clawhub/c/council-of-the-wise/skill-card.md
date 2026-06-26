## Description: <br>
Council sends an idea to a multi-perspective panel of AI personas for synthesized feedback, recommendations, action items, and a confidence signal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffaf](https://clawhub.ai/user/jeffaf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use Council to stress-test ideas, plans, content strategies, and major decisions through multiple expert-style perspectives before acting on them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-submitted ideas or documents are passed through the model session during council analysis. <br>
Mitigation: Use the skill only with information you are comfortable sending through the active model session. <br>
Risk: Custom Markdown files added to the agents folder become persona instructions for future council runs. <br>
Mitigation: Review any custom agent Markdown files before deployment or before relying on future council output. <br>
Risk: Casual phrasing may invoke the council when a direct answer would be preferable. <br>
Mitigation: Invoke the skill explicitly when multi-perspective review is desired. <br>


## Reference(s): <br>
- [Council README](README.md) <br>
- [Council Self-Review](docs/council-self-review.md) <br>
- [Daniel Miessler](https://danielmiessler.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/jeffaf/council-of-the-wise) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown council report with synthesis, perspective sections, action items, and confidence signal.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single consolidated report; custom agent persona files can change the included perspectives.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter, changelog, server release metadata; released 2026-02-23 in changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
