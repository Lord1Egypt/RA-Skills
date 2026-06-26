## Description: <br>
Local-first deep research like OpenAI Deep Research: generates questions.md + response.md artifacts and enforces a time budget. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VirajSanghvi1](https://clawhub.ai/user/VirajSanghvi1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and analysts use DeepthinkLite to scaffold repeatable local research runs with durable questions, response, and metadata files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to browse the web or read local files during research. <br>
Mitigation: Require user approval before browsing or reading non-obvious local paths, and keep tool use agent-controlled. <br>
Risk: Research sources may contain prompt-injection attempts or misleading content. <br>
Mitigation: Treat retrieved content as untrusted data, prefer summaries with citations, and clearly delimit any raw excerpts. <br>
Risk: Generated research artifacts may contain incomplete or incorrect guidance. <br>
Mitigation: Review questions.md, response.md, and meta.json before relying on them for decisions or downstream instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/VirajSanghvi1/deepthinklite) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and JSON metadata generated in a local run directory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates questions.md, response.md, and meta.json without overwriting existing files.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
