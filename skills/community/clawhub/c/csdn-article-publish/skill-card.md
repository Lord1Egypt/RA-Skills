## Description: <br>
Automates CSDN blog article workflows by creating Markdown posts, saving drafts, updating existing articles, and publishing through CSDN's article API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to draft, update, and publish CSDN blog articles from local Markdown while preserving article IDs and CSDN URLs for later edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to store live CSDN authentication headers in a plaintext local configuration file. <br>
Mitigation: Keep csdn_config.json private, out of shared folders and version control, and rotate or refresh CSDN credentials if the file is exposed. <br>
Risk: The skill has CSDN account-write capability and can update or publish articles. <br>
Mitigation: Review every generated command and confirm update or publish intent before running it. <br>
Risk: Automatic article ID reuse can target the wrong CSDN article if csdn_article_map.json is stale or incorrect. <br>
Mitigation: Review csdn_article_map.json before relying on automatic article ID reuse, or pass the intended article ID explicitly. <br>


## Reference(s): <br>
- [CSDN Blog API Reference](references/api_reference.md) <br>
- [CSDN Article Publish Troubleshooting](references/troubleshooting.md) <br>
- [CSDN Markdown Editor](https://editor.csdn.net/md/) <br>
- [CSDN saveArticle API endpoint](https://bizapi.csdn.net/blog-console-api/v3/mdeditor/saveArticle) <br>
- [ClawHub release page](https://clawhub.ai/wuchubuzai2018/csdn-article-publish) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Node.js API calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create or update local Markdown files and csdn_article_map.json when run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
