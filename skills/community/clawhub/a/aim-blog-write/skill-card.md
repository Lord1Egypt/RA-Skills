## Description: <br>
Generates SEO blog content from a required theme, industry, and language, then packages the result as a Word document with downloaded images and raw JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[focus-aim](https://clawhub.ai/user/focus-aim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to request SEO-focused blog drafts by specifying a topic, industry, and target language. The skill calls a configured SEO service, downloads returned images, and creates a Word document plus raw JSON for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles an aim-secret-key and sends blog topics, industry, and language fields to a configured AEP service. <br>
Mitigation: Install only if the publisher and service are trusted, use a dedicated low-privilege key, avoid sharing production credentials in chat, and independently verify service URLs before use. <br>
Risk: The skill performs remote network calls and writes raw JSON, downloaded images, and generated Word documents to local output folders. <br>
Mitigation: Review generated content and downloaded media before publication, and delete .env, raw.json, and downloaded images when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/focus-aim/aim-blog-write) <br>
- [AIM skills key registration](https://tools.mentarc.cn/aim-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated runs produce JSON, downloaded images, and .docx files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires theme, industry, and language. Runtime output is written under output/<task>_<timestamp>/ and may include raw.json and images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
