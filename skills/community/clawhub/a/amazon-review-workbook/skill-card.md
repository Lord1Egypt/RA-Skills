## Description: <br>
Collects Amazon reviews through a logged-in Chrome debugging session, exports a fixed 14-column factual workbook, optionally fills Chinese translations through DeepLX, and supports model-assisted tagging into a delivery-ready spreadsheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aduo6668](https://clawhub.ai/user/aduo6668) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to collect Amazon product reviews, preserve factual review fields, translate review text when configured, and prepare a final labeled review workbook for competitor or customer feedback analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A logged-in Amazon browser session exposed through Chrome remote debugging can give the skill temporary access to authenticated pages. <br>
Mitigation: Use a dedicated temporary Chrome profile, bind the debug port to local access only, and close the debug session immediately after scraping. <br>
Risk: Optional DeepLX translation can send review text to a configured external translation endpoint. <br>
Mitigation: Use only trusted DeepLX endpoints and omit the translation step when review text should not leave the local environment. <br>
Risk: Review exports, local caches, and label files can contain customer review content and workflow data. <br>
Mitigation: Keep generated outputs out of source control and delete local caches and exports when they are no longer needed. <br>


## Reference(s): <br>
- [Amazon Review Workbook on ClawHub](https://clawhub.ai/aduo6668/amazon-review-workbook) <br>
- [Setup](references/setup.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Tagging Guidelines](references/tagging-guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated JSON, CSV, and XLSX review workbook files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a fixed 14-column delivery workbook and separate labels JSON for model-completed semantic fields.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
