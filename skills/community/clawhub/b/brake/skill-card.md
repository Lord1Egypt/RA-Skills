## Description: <br>
Brake guides users through collecting brake design parameters, calculating results, and creating guest production sheets for CAD drawing generation on jixietools.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and mechanical design practitioners use this skill to generate brake CAD drawing workflows by selecting a brake product, entering parameters, reviewing calculated values, and creating a guest production sheet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends brake design parameters to jixietools.com and creates a guest production sheet on that service. <br>
Mitigation: Use the skill only when users accept that remote service interaction, and stop before production-sheet creation if they do not want remote job creation or polling. <br>
Risk: The generated guest URL and guest code provide access to production-sheet progress and results. <br>
Mitigation: Treat the generated URL and guest code as private access links and avoid sharing them outside the intended audience. <br>
Risk: The skill evidence notes a category ID inconsistency in product selection. <br>
Mitigation: Review the selected product carefully before calculation or production-sheet creation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liv09370/brake) <br>
- [Jixietools API Base URL](https://jixietools.com/api/v1) <br>
- [Publisher Profile](https://clawhub.ai/user/liv09370) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese-language Markdown with tables, prompts, URLs, and inline bash/curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces remote job progress links and generated drawing file listings when the external service completes the workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
