## Description: <br>
将飞书文档、Word、PDF、Excel、文本或 CSV 内容转换为深色可视化 HTML 看板，并可导出 PDF 和长图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzm2023](https://clawhub.ai/user/lzm2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to turn business documents, spreadsheets, PDFs, Feishu documents, and raw text into shareable visual dashboards and export artifacts for review or presentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive documents and persist converted HTML, PDF, and image outputs. <br>
Mitigation: Use it only with documents suitable for local export, review output retention expectations, and remove generated export directories when no longer needed. <br>
Risk: Document content may be rendered into browser-viewed HTML without reliable escaping. <br>
Mitigation: Avoid untrusted documents until HTML escaping and request blocking during export are added or independently reviewed. <br>
Risk: Runtime dependencies and browser export behavior may vary because dependency versions are not pinned. <br>
Mitigation: Pin and review dependencies before deployment, especially Playwright and document parsing libraries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lzm2023/doc-visualizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [HTML, PDF, PNG, file paths, and concise setup or usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written to a timestamped visual_exports directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
