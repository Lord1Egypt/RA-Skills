## Description: <br>
Skill-first Bilibili to Notion pipeline. Download a Bilibili/b23 video, transcribe audio, upload the mp4, create or update a Notion transcript page, write transcript blocks, then optionally append a Markdown summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiing](https://clawhub.ai/user/hiing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert Bilibili videos into Notion transcript pages with uploaded video links, transcript blocks, and optional Markdown summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or archive Notion page content. <br>
Mitigation: Confirm the target Notion page before running and avoid replace-children behavior unless replacing the page body is intended. <br>
Risk: Uploaded videos may become available through a public download URL. <br>
Mitigation: Use a trusted upload endpoint and verify the visibility and retention policy before uploading sensitive videos. <br>
Risk: The pipeline can delete local intermediate files during cleanup. <br>
Mitigation: Keep metadata and transcript files until the Notion page and uploaded video link have been verified. <br>
Risk: The workflow uses credentials such as a limited Notion integration token, optional upload token, and optional Bilibili cookie file. <br>
Mitigation: Use least-privilege credentials, keep tokens and cookies out of source control, and rotate them if logs or local files are exposed. <br>


## Reference(s): <br>
- [Workflow Notes](references/workflow.md) <br>
- [Summary Template](references/summary-template.md) <br>
- [CloudFlare-ImgBed](https://github.com/MarSeventh/CloudFlare-ImgBed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status from pipeline steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update Notion content, upload videos, and clean local intermediate files based on user-selected options.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
