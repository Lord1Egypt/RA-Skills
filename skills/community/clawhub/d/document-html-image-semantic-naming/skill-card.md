## Description: <br>
文档转 HTML 时的图片语义命名技能。用于把 doc/docx/pdf 等文档导出的 `image1`、`image2` 这类无语义图片，结合文档上下文与图片内容重新命名，并同步更新 HTML 引用与映射清单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinglan803-coder](https://clawhub.ai/user/tinglan803-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content operators use this skill to rename generic images exported from doc, docx, pdf, or HTML conversion workflows based on nearby document context and visible image content. It also guides updating HTML image references and preserving an original-to-final filename mapping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Renaming exported image files can break HTML image links if references are not updated consistently. <br>
Mitigation: Run the skill on a copy or keep backups, then verify every img src resolves after renaming. <br>
Risk: Semantic image names may be inaccurate when document context and visible image content conflict. <br>
Mitigation: Review the generated filename mapping and correct names where image content contradicts surrounding text. <br>
Risk: The original relationship between exported filenames and final asset names can be lost. <br>
Mitigation: Preserve an original-to-final filename mapping and avoid deleting the original export before validation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with suggested file outputs and optional shell-command workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable renaming rules, updated HTML reference guidance, and an original-to-final image mapping; no network use or credentials are indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
