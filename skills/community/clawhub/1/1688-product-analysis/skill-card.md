## Description: <br>
Analyzes 1688 product listings by collecting seller product data, diagnosing performance, traffic, search ranking, advertising, and competitive issues, and returning actionable optimization recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and operators use this skill to select abnormal 1688 listings, retrieve real listing data, and produce concise product diagnosis reports with follow-up optimization choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires ALI_1688_AK credentials and can access 1688 seller and product data. <br>
Mitigation: Configure ALI_1688_AK specifically for this skill and install it only when that account-level access is acceptable. <br>
Risk: The skill can reuse 1688 credentials stored for related skills or unintended USER_ID/X_USER_ID values. <br>
Mitigation: Review the OpenClaw credential configuration before use and remove or correct unintended user identifiers. <br>
Risk: Follow-up action choices may hand off to downstream image or title optimizer skills that can affect product changes. <br>
Mitigation: Review downstream optimizer permissions and require explicit approval before allowing changes to listings. <br>
Risk: CLI command execution reports usage automatically. <br>
Mitigation: Review the release's telemetry behavior before deploying in environments where usage reporting is restricted. <br>


## Reference(s): <br>
- [1688 Product Analysis ClawHub page](https://clawhub.ai/1688aiinfra/1688-product-analysis) <br>
- [Analysis Dimensions](references/analysis-dimensions.md) <br>
- [Interaction Specs](references/interaction-specs.md) <br>
- [Simple Report Template](references/report-template-simple.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown diagnosis report with JSON CLI responses and interactive selection data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALI_1688_AK credentials; CLI responses use success, markdown, and data fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
