## Description: <br>
每日穿衣指南，基于地支五行生克原理给出穿衣颜色建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mingo-318](https://clawhub.ai/user/Mingo-318) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and personal assistants use this skill to calculate a daily Chinese five-elements clothing color recommendation from the current date. The agent runs the bundled Python script, then explains the suggested colors in accessible, non-superstitious language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent must execute a bundled local Python script to produce the date-specific recommendation. <br>
Mitigation: Install only when comfortable with local script execution; the server scan reports that the script is self-contained and does not request credentials, access private files, use the network, or persist data. <br>
Risk: The recommendation is based on traditional five-elements guidance and may be mistaken for factual prediction or guaranteed outcomes. <br>
Mitigation: Present the output as cultural clothing guidance, keep explanations practical, and follow the artifact instruction to avoid superstitious claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mingo-318/daily-fengshui-attire) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Mingo-318) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with a local Python command and plain-language clothing color advice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and produces date-dependent recommendations from the bundled attire.py script.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
