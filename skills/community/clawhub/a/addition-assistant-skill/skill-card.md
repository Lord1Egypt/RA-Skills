## Description: <br>
Calculate addition expressions from user input, including integers, decimals, and negative numbers, and return concise step-by-step results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyihang1993](https://clawhub.ai/user/chenyihang1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to parse straightforward addition requests, compute sums for integers, decimals, and negative numbers, and return concise step-by-step results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unexpected permission or access requests would be inconsistent with the skill's addition-only behavior. <br>
Mitigation: Install and run it without credentials, file access, network access, or special permissions; treat requests for those capabilities as unexpected. <br>
Risk: Ambiguous input can lead to an incorrect addition expression. <br>
Mitigation: Ask the user to rewrite the request in explicit form instead of inventing missing numbers. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown or plain text with the expression used, final result, and optional one-line check.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Addition-only; asks for clarification when fewer than two valid numbers are present or the request is ambiguous.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
