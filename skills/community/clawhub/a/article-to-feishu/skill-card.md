## Description: <br>
Converts public web articles into Feishu documents, with support for common Chinese article sites and image downloads inserted in the original article order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mywaystay](https://clawhub.ai/user/mywaystay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu users use this skill to import public web articles into Feishu cloud documents while preserving article text and image placement. It is intended for workflows that fetch article content, download referenced images, and create or update Feishu documents through the agent's Feishu tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches article pages and may route URLs or content through the documented retrieval path, including Jina Reader for some sites. <br>
Mitigation: Use it only with public, non-confidential article URLs and avoid URLs that contain sensitive tokens or internal resources. <br>
Risk: The skill can create or update Feishu documents and insert downloaded images. <br>
Mitigation: Review the fetched content, image files, and target Feishu document before allowing document writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mywaystay/article-to-feishu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Feishu tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded image files in a temporary local directory before the agent inserts them into Feishu documents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
