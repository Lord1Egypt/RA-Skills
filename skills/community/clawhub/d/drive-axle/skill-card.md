## Description: <br>
Drive Axle guides Chinese-language users through a drive-axle CAD workflow that collects design parameters, calls jixietools.com APIs, creates a guest production sheet, and monitors drawing generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mechanical design users and agents use this skill to collect drive-axle configuration parameters, request remote CAD calculations, review returned values, and create a guest-access production sheet for generated drawings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drive-axle design parameters are sent to jixietools.com and results are exposed through a shareable guest progress/result link. <br>
Mitigation: Before creating a production sheet, confirm the user is comfortable with the remote record and unauthenticated guest URL. <br>


## Reference(s): <br>
- [ClawHub Drive Axle Skill Page](https://clawhub.ai/liv09370/drive-axle) <br>
- [JixieTools API Base](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls] <br>
**Output Format:** [Markdown with Chinese-language prompts, tables, inline shell commands, and API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a guest production-sheet URL and status updates when the remote service returns them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
