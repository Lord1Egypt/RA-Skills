## Description: <br>
Anthropic PPTX helps agents create, inspect, edit, and QA PowerPoint presentations using guided workflows, PPTX generation references, and Office archive utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and agent users use this skill when a task involves .pptx files, including extracting presentation content, editing template-based decks, creating new decks, converting slides for visual QA, and validating final output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports suspicious posture because the skill bundles broader Office document mutation workflows beyond normal presentation guidance. <br>
Mitigation: Install only after reviewing the included workflows, and use the skill on copies of documents rather than originals. <br>
Risk: The security guidance warns that the LibreOffice helper can compile and preload native code from temporary storage, which is higher risk on shared systems. <br>
Mitigation: Run the skill in an isolated workspace or container, avoid sensitive files unless reviewed, and be cautious on shared hosts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liberalchang/anthropic-pptx) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Editing Presentations](artifact/editing.md) <br>
- [PptxGenJS Tutorial](artifact/pptxgenjs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or mutation of PPTX and related Office archive files; review generated documents before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
