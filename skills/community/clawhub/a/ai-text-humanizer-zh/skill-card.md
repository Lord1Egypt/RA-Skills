## Description: <br>
中文AI文本检测与改写工具。当用户需要检测AI生成文本、优化AI文本使其更自然、降低AI痕迹、文本去重、论文降重时使用。支持检测16+类AI特征，自动改写冗余表达，清理Markdown格式，移除chatbot痕迹，输出详细报告和AI概率分数。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runze123](https://clawhub.ai/user/runze123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, editors, students, and other external users can use this skill to analyze Chinese text for common AI-writing markers, rewrite rule-matched phrases, clean Markdown or chatbot artifacts, and compare before-and-after scores. Users should review output before publication because rule-based rewriting can remove or alter meaning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rewritten text can be inaccurate, less complete, or misleading because rule-based cleanup may remove wording or alter emphasis. <br>
Mitigation: Review rewritten text against the original before use, especially for academic, legal, compliance, or publication contexts. <br>
Risk: The skill can be misused to obscure AI authorship where disclosure or academic-integrity rules require transparency. <br>
Mitigation: Use it only where editing AI-assisted text is permitted, and preserve required AI-use disclosures. <br>
Risk: Command-line output paths may overwrite or place transformed text in unintended locations. <br>
Mitigation: Choose output paths deliberately and inspect generated files before sharing or replacing originals. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples; command-line scripts produce plain text, JSON reports, and output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local rule and synonym JSON files; no external service dependency is evidenced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
