## Description: <br>
Convert ASCII art diagrams to hand-drawn Excalidraw JSON files. Analyzes structure first, then generates incrementally module-by-module. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert ASCII architecture, flowchart, and system diagrams into Excalidraw files. It guides an agent through diagram analysis, layout planning, module-by-module JSON generation, and final file assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated diagrams and intermediate JSON files may persist sensitive architecture details under ~/.excalidraw/. <br>
Mitigation: Avoid highly sensitive diagrams unless you can manage or delete the saved local files afterward. <br>
Risk: Converted diagrams may omit or misrepresent relationships from complex ASCII inputs. <br>
Mitigation: Review the generated Excalidraw file before sharing or using it as technical documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyanbo2007/ascii-excalidraw) <br>
- [Excalidraw](https://excalidraw.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with JSON module snippets and shell commands; final artifacts are .excalidraw JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes final and intermediate files under ~/.excalidraw/ by default.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
