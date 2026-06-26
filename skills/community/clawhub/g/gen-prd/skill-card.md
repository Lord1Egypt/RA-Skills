## Description: <br>
通过交互式需求分析生成完整的 PRD 文档。基于领域知识库进行结构化提问和数据流推导，确保需求理解和数据流的完整性。仅当用户要「生成 PRD/需求文档」时使用；分析现有代码库请用 analyze。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lf951515851](https://clawhub.ai/user/lf951515851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, founders, and development teams use this skill to turn an initial product idea into a structured PRD through interactive requirement clarification, domain-aware questions, data-flow derivation, and Markdown document generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a PRD Markdown file locally and may use a default output path. <br>
Mitigation: Review or set the output path before generation. <br>
Risk: The workflow may continue into a follow-on design step after PRD generation. <br>
Mitigation: Pause the workflow if you do not want it to continue into the follow-on design step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lf951515851/gen-prd) <br>
- [README.md](artifact/README.md) <br>
- [prompt.md](artifact/prompt.md) <br>
- [prd-template.md](artifact/prd-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown PRD written to a local file, with conversational clarification and review prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output path is docs/prd/YYYY-MM-DD-{project-name}.md unless the user specifies another path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
