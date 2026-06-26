## Description: <br>
Generates distillation tower CAD drawing workflows by guiding users through JXT mechanical platform product selection, parameter collection, calculation, production sheet creation, and progress monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and engineers use this skill to create distillation tower CAD production requests through the JXT mechanical parts service. The skill collects design parameters, calls the external CAD service, and reports production sheet status and output links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends distillation tower design inputs to an external CAD service. <br>
Mitigation: Use only with design data that can be shared with jixietools.com, and review the returned production sheet before relying on it. <br>
Risk: The artifact contains a documented category mismatch: the base information says distillation tower category ID 33, while the product listing command uses category_id=8. <br>
Mitigation: Confirm the product list and category ID match distillation towers before submitting parameters or creating a production sheet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liv09370/distillation) <br>
- [JXT mechanical API base URL](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Chinese conversational guidance with Markdown tables, JSON examples, and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses external jixietools.com CAD endpoints, preserves calculation filenames for incremental updates, and polls guest production sheet status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
