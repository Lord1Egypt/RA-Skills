## Description: <br>
AI-driven document compliance review skill that uses a Python API to check PDF, Word, and image documents for completeness, timeliness, and visual compliance signals such as stamps and signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evob-z](https://clawhub.ai/user/evob-z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and compliance reviewers use this skill to inspect project, invoice, and administrative approval documents for required files, validity dates, and stamp or signature evidence. It is intended for document review workflows where structured Python dictionary results can be summarized by an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document text or images may be sent to configured LLM, embedding, vision, or OCR providers. <br>
Mitigation: Use private or local endpoints for sensitive documents, prefer local OCR when appropriate, and redact sensitive content before processing. <br>
Risk: Command-based SecretRef providers can run local commands with broad authority. <br>
Mitigation: Avoid untrusted exec providers and restrict SecretRef configuration to reviewed providers. <br>
Risk: Unreviewed dependency updates may be unsuitable for regulated or enterprise environments. <br>
Mitigation: Review and pin dependencies before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evob-z/compliance-checker-light) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>
- [DashScope vision model documentation](https://help.aliyun.com/zh/dashscope/developer-reference/vl-plus-quick-start) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration, API Calls, Analysis] <br>
**Output Format:** [Markdown guidance with Python code examples and structured dictionary or JSON-like API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided file or directory paths and SecretRef configuration for LLM access.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata, SKILL.md frontmatter, pyproject.toml, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
