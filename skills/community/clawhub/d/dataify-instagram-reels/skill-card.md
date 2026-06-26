## Description: <br>
Submit Dataify Instagram Reel Information Builder tasks for three Instagram Reel collection modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Dataify Builder jobs that collect Instagram Reel information by detail URL, list or profile URL, or website/list URL. The skill guides mode selection, validates parameters, resolves the Dataify API TOKEN, and returns the submitted task ID and status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A saved DATAIFY_API_TOKEN can be used to create external Dataify jobs. <br>
Mitigation: Review the selected mode, Instagram URLs, dates, post counts, and file name before submission, and save the API TOKEN only when future reuse is intended. <br>
Risk: Invalid or unintended Instagram URLs and date ranges can submit the wrong collection task. <br>
Mitigation: Use the skill's parameter confirmation and validation steps before allowing a Builder request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-instagram-reels) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Dataify task identifiers, status values, submitted parameters, and dashboard links after successful submission.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
