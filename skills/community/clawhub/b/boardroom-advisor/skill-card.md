## Description: <br>
Consult a virtual board of 4 strategic advisors (Donald Miller, Seth Godin, Alex Hormozi, Daniel Priestley) on any major business decision. Two rounds of argument + rebuttal, then a decision brief, interactive dashboard, and clear recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Batsirai](https://clawhub.ai/user/Batsirai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Business operators, founders, and strategy teams use this skill to deliberate major business decisions through four advisor perspectives, then receive a decision brief, optional interactive dashboard, print-ready summary, and clear recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business details may be shared with OpenRouter when OPENROUTER_API_KEY is configured. <br>
Mitigation: Use OpenRouter only when acceptable for the business context, and avoid sharing confidential details unless the user has approved that data path. <br>
Risk: The skill writes decision briefs, dashboards, and print-ready HTML files to the working directory. <br>
Mitigation: Run it in a dedicated folder so generated decision artifacts are easy to review, retain, or delete. <br>
Risk: Strategic recommendations can be incomplete or misleading if the input business context is thin. <br>
Mitigation: Collect sufficient context before running the board and treat the output as decision support that remains subject to human review. <br>


## Reference(s): <br>
- [Boardroom model: OpenRouter + Claude Opus 4.6](references/openrouter-board-model.md) <br>
- [OpenRouter Claude Opus 4.6](https://openrouter.ai/anthropic/claude-opus-4.6) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown decision brief, self-contained HTML dashboard, optional print-ready HTML, and final synthesis in chat] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a decision-specific folder in the working directory; optional OpenRouter use requires OPENROUTER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
