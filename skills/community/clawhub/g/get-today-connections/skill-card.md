## Description: <br>
Fetch today's NYT Connections puzzle answers and hints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1eif](https://clawhub.ai/user/1eif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who want current NYT Connections hints or answers use this skill to fetch a third-party puzzle data source and present the categories, hints, answer words, and source breakdown link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on connections-answers.com as a third-party source for puzzle data. <br>
Mitigation: Use it only when that source is acceptable, and review the returned puzzle details before relying on them. <br>
Risk: The skill may reveal NYT Connections spoilers when a user asks for answers. <br>
Mitigation: When the user asks only for hints, omit answer words and show only the hint-focused output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1eif/get-today-connections) <br>
- [connections-answers.com today API](https://connections-answers.com/api/today) <br>
- [connections-answers.com archive](https://connections-answers.com/blog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown table with optional full Markdown breakdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can hide answer words when the user asks for hints only.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
