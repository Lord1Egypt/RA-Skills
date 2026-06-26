## Description: <br>
Guides users through Dataify YouTube video post collection modes, validates parameters and token use, submits a Builder task, and returns the task_id and status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and submit Dataify Builder jobs that collect YouTube video posts by URL, search filters, hashtag, podcast URL, keyword, or Explore URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad YouTube-related trigger wording may invoke the skill for requests that do not intend a Dataify collection task. <br>
Mitigation: Confirm the user wants to use Dataify for YouTube collection before requesting parameters or submitting a Builder task. <br>
Risk: The skill uses a Dataify API TOKEN to submit Builder requests. <br>
Mitigation: Use a limited-scope token when available, resolve the token only for the current task, and review parameters before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-youtube-video-post) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON task summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns mode, spider_id, task_id, status, parameters, file_name, dashboard_url, and message after successful submission.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
