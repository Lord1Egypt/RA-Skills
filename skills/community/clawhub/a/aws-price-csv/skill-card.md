## Description: <br>
Generate AWS cost CSVs from a user-provided service list. Use when someone supplies an item list + AWS region and needs per-item pricing plus totals via AWS Price List API or bulk pricing JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crazylion](https://clawhub.ai/user/crazylion) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, cloud engineers, and FinOps users use this skill to turn AWS service item lists into itemized pricing CSVs with per-line costs and totals. It can use live AWS Price List API queries or cached bulk pricing JSON for On-Demand and Reserved terms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API mode can use the active AWS profile and call the AWS Price List API. <br>
Mitigation: Use a least-privilege AWS profile limited to pricing:GetProducts and verify the active profile before running API mode. <br>
Risk: Bulk mode downloads and caches large pricing JSON files locally. <br>
Mitigation: Use a dedicated cache directory and refresh cached data intentionally with the provided cache controls. <br>
Risk: The output CSV path is user-selected and could overwrite an existing file. <br>
Mitigation: Choose an output filename that will not overwrite important files. <br>


## Reference(s): <br>
- [AWS Pricing Cheat Sheet](references/api_reference.md) <br>
- [AWS Price List API endpoint](https://api.pricing.us-east-1.amazonaws.com/) <br>
- [AWS bulk pricing file pattern](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-northeast-1/index.json) <br>
- [ClawHub release page](https://clawhub.ai/crazylion/aws-price-csv) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, CSV files] <br>
**Output Format:** [Markdown guidance with shell commands and generated CSV output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CSV rows include item-level pricing details and a TOTAL row.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
