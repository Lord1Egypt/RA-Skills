## Description: <br>
Generates clutch CAD drawings through a guided JXT mechanical parts workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and mechanical design practitioners use this skill to choose a clutch product, enter design parameters step by step, review calculated values, and create a guest production sheet for CAD drawing generation through jixietools.com. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact names clutch category ID 31 but the product-list command uses category_id=8, so the product list may not match the intended clutch catalog. <br>
Mitigation: Confirm the correct clutch category with the publisher or jixietools.com documentation before relying on the fetched product list. <br>
Risk: The workflow sends design parameters to jixietools.com and creates a guest production sheet link accessible with its guest code. <br>
Mitigation: Use the skill only when sharing those design parameters and creating a guest-accessible production sheet is acceptable for the user's project. <br>


## Reference(s): <br>
- [JixieTools API base](https://jixietools.com/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/liv09370/clutch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Chinese Markdown conversation with parameter tables, curl commands, JSON examples, and production sheet links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides one parameter at a time, stores the returned filename for incremental recalculation, and polls the guest production sheet status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
