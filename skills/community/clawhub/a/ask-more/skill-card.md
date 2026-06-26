## Description: <br>
Multi-LLM consultation for complex questions that sends a confirmed, self-contained prompt to multiple configured models, compares their responses, and returns consensus, differences, conflicts, and actionable synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pongpong990909-prog](https://clawhub.ai/user/pongpong990909-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Ask-More to get second opinions, blind spot detection, and decision support on complex questions by consulting multiple configured model providers before synthesizing the results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the reviewed question or conversation summary to multiple configured AI providers. <br>
Mitigation: Review the packed prompt before confirming and avoid using the skill with highly sensitive content. <br>
Risk: Optional local run logging can retain run metadata. <br>
Mitigation: Disable logging or periodically delete local logs when retained run metadata is not desired. <br>
Risk: Consensus across models can still reflect shared model bias or incomplete evidence. <br>
Mitigation: Treat the report as decision support, review uncertainty labels and conflicts, and use human judgment for high-stakes decisions. <br>


## Reference(s): <br>
- [Prompt Templates](references/prompt-templates.md) <br>
- [Ask-More ClawHub Page](https://clawhub.ai/pongpong990909-prog/ask-more) <br>
- [Publisher Profile](https://clawhub.ai/user/pongpong990909-prog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional raw model comparisons, setup guidance, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normal mode synthesizes model responses into consensus, differences, conflicts, uncertainty labels, and next steps; compare mode returns side-by-side model responses without synthesis.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
