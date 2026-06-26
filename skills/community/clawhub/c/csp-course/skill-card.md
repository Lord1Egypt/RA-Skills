## Description: <br>
Creates C++ and CSP informatics lesson material packages, including game-style PPTX slides, DOCX lesson plans and worksheets, C++ examples, and standalone HTML practice games. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahao2001](https://clawhub.ai/user/ahao2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers and course creators use this skill to produce single C++/CSP lessons or batch-generate course materials from PDF textbooks for upper-primary through junior competition classes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated course files may be written to hardcoded or unintended local paths. <br>
Mitigation: Install in a dedicated workspace and replace the hardcoded C:/Users/ning/... output paths with the intended folder before running Node scripts. <br>
Risk: File-moving commands may move more files than intended when run in a busy directory. <br>
Mitigation: Review any Move-Item command and run the skill from a clean output folder that contains only generated lesson assets. <br>
Risk: The HTML game template imports Google Fonts, which can be unsuitable for offline or privacy-preserving use. <br>
Mitigation: Remove the Google Fonts import or replace it with local fonts when offline or privacy-preserving HTML output is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahao2001/csp-course) <br>
- [Interactive game template](references/game_template.html) <br>
- [Prime-number lesson reference](references/素数判断讲解.md) <br>
- [C++ code example](references/代码示例.cpp) <br>
- [PptxGenJS documentation](https://gitbrent.github.io/PptxGenJS/) <br>
- [docx documentation](https://docx.js.org/) <br>
- [pdfplumber](https://github.com/jsvine/pdfplumber) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance plus generated PPTX, DOCX, CPP, HTML, JSON, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local files; PDF batch mode depends on Python pdfplumber and Node.js packages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
