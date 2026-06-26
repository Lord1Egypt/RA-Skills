## Description: <br>
Chapter Outliner generates structured 15-beat Markdown chapter outlines for fiction projects using story outline, style, character, and chapter inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and writing agents use this skill to turn a fiction project directory and chapter number into a detailed chapter outline with beat structure, word allocation, character references, and style notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional LLM script can send outline, style, character, and chapter metadata from a writing project to DashScope when DASHSCOPE_API_KEY is configured. <br>
Mitigation: Use scripts/generate_outline.py for local-only outline templates, or run scripts/generate_outline_llm.py only after reviewing the project data and accepting provider data-sharing requirements. <br>
Risk: The server security verdict is suspicious because the documented local outliner includes an undocumented LLM script. <br>
Mitigation: Review the skill before installing and choose the local script unless remote LLM generation is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuzhihui886/chapter-outliner) <br>
- [DashScope chat completions endpoint used by optional LLM script](https://coding.dashscope.aliyuncs.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown chapter outline, optionally saved to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local script produces template-based outlines; optional LLM script can generate detailed JSON-backed Markdown outlines when DASHSCOPE_API_KEY is configured.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
