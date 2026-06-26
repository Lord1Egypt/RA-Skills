## Description: <br>
Generates API documentation from Python source code through a multi-step pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dapan0902](https://clawhub.ai/user/dapan0902) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to document Python modules by inventorying public APIs, proposing Google-style docstrings, assembling a Markdown API reference, and checking coverage and examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for broad documentation requests and process more code than intended. <br>
Mitigation: Provide only the Python files that should be documented. <br>
Risk: Generated docstrings or API references may be inaccurate or omit relevant behavior. <br>
Mitigation: Review generated docstrings, examples, and final documentation before accepting changes. <br>
Risk: Input code may contain secrets or unrelated proprietary content. <br>
Mitigation: Remove secrets and unrelated code before asking the skill to generate documentation. <br>


## Reference(s): <br>
- [Docstring 格式规范（Google 风格）](artifact/references/docstring-style.md) <br>
- [API 文档质量检查清单](artifact/references/quality-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dapan0902/doc-pipeline) <br>
- [Publisher Profile](https://clawhub.ai/user/dapan0902) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown API reference with Google-style Python docstring suggestions and quality-check results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill asks for user confirmation before moving from API inventory to docstring generation, and generated documentation should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
