## Description: <br>
Turns books into daily learning tasks by extracting knowledge points, generating study cards, and pushing them through configured IMA or Feishu workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sedey999](https://clawhub.ai/user/sedey999) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to break PDF, DOCX, HTML, EPUB, TXT, or RTF books into reusable knowledge-point data and deliver one study card per day. It supports bilingual learning workflows, configurable card templates, progress tracking, and failure notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated learning materials can be uploaded to configured IMA or Feishu destinations. <br>
Mitigation: Install and run the skill only after confirming the selected destination is appropriate for the book content and generated cards. <br>
Risk: The workflow uses user-provided credentials and webhooks for IMA, Feishu, and failure notifications. <br>
Mitigation: Store credentials in local configuration as documented, verify webhook destinations before use, and rotate keys if a destination or local environment is no longer trusted. <br>
Risk: The Feishu image path may share generated or source-derived images through an external image host. <br>
Mitigation: Avoid using private, sensitive, or copyrighted images with that path unless sharing them through the configured service is acceptable. <br>


## Reference(s): <br>
- [IMA Agent Interface](https://ima.qq.com/agent-interface) <br>
- [Open Music Theory example source](https://viva.pressbooks.pub/openmusictheory) <br>
- [GTK for Windows](https://gtk.org/download/windows.php) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON, HTML, PDF, image, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include generated learning-card files, progress state, upload actions to configured external services, and user-facing status summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
