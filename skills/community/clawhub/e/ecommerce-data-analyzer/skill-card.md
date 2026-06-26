## Description: <br>
E-commerce Data Analyzer analyzes uploaded CSV sales data to generate sales trend charts, product rankings, channel revenue breakdowns, margin analysis, inventory alerts, and PDF reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baolige2023](https://clawhub.ai/user/baolige2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers use this skill to upload CSV sales data, review sales, channel, product, margin, and inventory performance, and generate Chinese-language business reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships exposed SkillPay credentials. <br>
Mitigation: Treat the key as compromised, rotate it before use, and provide payment credentials through a private runtime secret instead of bundled files. <br>
Risk: The skill includes a payment-enabled Flask web app that may charge users during upload. <br>
Mitigation: Confirm all SkillPay charges before uploading business data and test payment behavior in a controlled environment. <br>
Risk: Uploaded CSVs and generated reports may contain business-sensitive sales data. <br>
Mitigation: Avoid exposing the Flask server to a network and delete uploaded CSVs and generated reports after use. <br>
Risk: The bundled Flask secret is not suitable for deployment. <br>
Mitigation: Replace the Flask secret before running outside a local review environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baolige2023/ecommerce-data-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/baolige2023) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, Charts, PDF reports] <br>
**Output Format:** [HTML analysis views, chart image files, and downloadable PDF reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CSV input with order date, product name, sales quantity, sales amount, sales channel, and inventory quantity fields.] <br>

## Skill Version(s): <br>
2.7.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
