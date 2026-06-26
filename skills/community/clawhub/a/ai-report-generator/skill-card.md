## Description: <br>
Generates Xiaohongshu operations reports from Feishu Bitable data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangfeng1995](https://clawhub.ai/user/huangfeng1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and operations teams use this skill to turn Xiaohongshu metrics from Feishu Bitable into a weekly performance report with overview metrics, high-performing post analysis, issue diagnosis, and optimization suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Feishu Bitable data and may expose or analyze the wrong table if permissions or table selection are too broad. <br>
Mitigation: Use a read-only Feishu app or token limited to the specific Xiaohongshu metrics table, and confirm the target table before generating a report. <br>
Risk: Generated operations recommendations may be misleading when the source metrics are incomplete, stale, or incorrectly entered. <br>
Mitigation: Review the Feishu source data and the generated report before using the recommendations for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangfeng1995/ai-report-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Xiaohongshu weekly operations metrics, high-performing post analysis, issue diagnosis, and optimization suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
