## Description: <br>
查询A股市场温度，当用户询问今日市场温度、今日A股温度、市场热度、大盘温度或类似问题时触发，并支持多个A股指数。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pandasky](https://clawhub.ai/user/pandasky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to generate a concise A-share index temperature report with PE and status values for configured indices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data retrieval can fail or return incomplete results for a configured index. <br>
Mitigation: Surface the script error in the report and review failed rows before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pandasky/a-share-thermometer) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Fixed Chinese plain text report with index, PE, temperature, and status rows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the East 8 date and omits unrelated explanation, summaries, and advice.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata; artifact frontmatter says 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
