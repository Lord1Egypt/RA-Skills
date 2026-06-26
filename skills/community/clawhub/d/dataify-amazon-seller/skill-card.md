## Description: <br>
Use for Dataify Amazon seller information collection Builder tasks by URL, including parameter confirmation, API TOKEN handling, Builder submission, task_id return, and request troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Amazon seller information collection jobs through Dataify Builder and receive the created task_id. It helps configure or reuse a Dataify API TOKEN, confirm request parameters, and direct users to Dataify for results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Dataify API TOKEN and may expose credentials if commands, environment variables, or logs are shared. <br>
Mitigation: Use a limited-scope token when available, keep DATAIFY_API_TOKEN out of shared logs and transcripts, and avoid pasting generated commands that contain credentials. <br>
Risk: The skill submits network requests to Dataify Builder using user-confirmed Amazon seller URLs and file names. <br>
Mitigation: Review the parameter table before submission and only send requests that match the intended seller URL and output file name. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-amazon-seller) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown instructions and parameter tables, optional shell commands, and JSON summaries from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a Dataify task_id and dashboard URL after successful submission; does not collect or invent downstream result fields.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
