## Description: <br>
Use whenever the user wants to interact with Figshare - searching public datasets/articles, downloading Figshare files, listing their own articles/collections/projects, creating or updating articles, or uploading files (including large multi-part uploads) via the Figshare v2 REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and external users use this skill to search Figshare, download public article files, and automate authenticated article, collection, project, upload, and publishing workflows through the Figshare v2 REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload, update, or publish Figshare account content, and published versions can be hard to reverse. <br>
Mitigation: Use a Figshare token only when needed, confirm article IDs and filenames with the user, and require explicit confirmation before publishing or modifying account content. <br>
Risk: The downloader writes remote-provided filenames locally without filename sanitization. <br>
Mitigation: Download only from trusted Figshare articles or sanitize filenames and use a controlled output directory before running the batch download helper. <br>


## Reference(s): <br>
- [Figshare API reference](https://docs.figshare.com/) <br>
- [Figshare token management](https://figshare.com/account/applications) <br>
- [ClawHub listing](https://clawhub.ai/agents365-ai/figshare-skill) <br>
- [Declared homepage](https://github.com/Agents365-ai/figshare-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and script invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; authenticated account operations require FIGSHARE_TOKEN.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
