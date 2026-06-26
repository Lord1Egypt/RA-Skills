## Description: <br>
Admin skill to sign into Cosmonyx, fetch companies, filter/export (PDF or Excel), optionally email the export, or send reminder emails to filtered companies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waqas-orcalo](https://clawhub.ai/user/waqas-orcalo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Cosmonyx administrators use this skill to sign in, retrieve company records, filter compliance or risk subsets, export selected records, and send export or reminder emails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can email sensitive company exports or local attachments. <br>
Mitigation: Use it only in a controlled admin environment and manually verify recipients, attachment paths, and export contents before sending. <br>
Risk: Attachment paths are not strongly scoped by the skill. <br>
Mitigation: Restrict attachments to a dedicated export directory and avoid arbitrary local file paths. <br>
Risk: The skill handles Cosmonyx admin credentials and access tokens. <br>
Mitigation: Keep credentials and tokens out of replies and logs, and stop the workflow if authentication fails or a token is missing. <br>


## Reference(s): <br>
- [Comonyx Admin ClawHub page](https://clawhub.ai/waqas-orcalo/comonyx-admin) <br>
- [Cosmonyx admin sign-in endpoint](https://gateway-dev.cosmonyx.co/auth/signin) <br>
- [Cosmonyx companies endpoint](https://gateway-dev.cosmonyx.co/companies) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown responses with generated PDF or Excel exports and optional shell commands for email sending] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create files in the user's Downloads folder and send email through SMTP when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
