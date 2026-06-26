## Description: <br>
Drop Pick provides cross-platform product selection and sourcing analysis for distributors and dropshippers across Alibaba, AliExpress, and Amazon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lcturing0](https://clawhub.ai/user/lcturing0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, distributors, and commerce agents use this skill to research products, compare sourcing channels, evaluate retail competition, estimate margins, and generate product selection reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Store-import and listing-event commands can change connected commerce accounts. <br>
Mitigation: Require explicit user approval before running live commerce actions, review the exact command and product IDs, and use scoped credentials where possible. <br>
Risk: Alibaba API access depends on OAuth credentials and access tokens. <br>
Mitigation: Use only the required Alibaba credentials, keep tokens scoped and protected, and refresh or revoke them according to the user's account policy. <br>
Risk: The skill can write product research reports into the working directory. <br>
Mitigation: Confirm the output path before writing files and have the user review generated reports before relying on sourcing or listing recommendations. <br>


## Reference(s): <br>
- [Drop Pick on ClawHub](https://clawhub.ai/lcturing0/distributor-product-selection) <br>
- [Project homepage](https://github.com/lcturing0/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with opencli shell commands and a product-selection report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write product-research/product-selection-report.md when report generation is requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
