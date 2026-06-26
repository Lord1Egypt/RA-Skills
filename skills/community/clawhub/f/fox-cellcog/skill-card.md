## Description: <br>
Any-to-any AI for agents that combines deep reasoning with multimodal inputs and outputs including research, videos, images, audio, dashboards, presentations, spreadsheets, and related deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinthqod](https://clawhub.ai/user/qinthqod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to send selected files and prompts to CellCog for cloud-based multimodal analysis and generation. It is intended for tasks such as research reports, dashboards, presentations, spreadsheets, audio, video, and other generated deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files may be uploaded to CellCog's cloud service. <br>
Mitigation: Reference only files that are approved for CellCog processing and avoid secrets or regulated data unless CellCog is authorized for that data. <br>
Risk: Tasks can consume CellCog credits and run asynchronously in the background. <br>
Mitigation: Use deliberate task prompts, monitor credit use, and reserve higher-cost modes for work that justifies the added expense. <br>
Risk: Remote-generated files can be written to user-specified local paths. <br>
Mitigation: Direct generated outputs to controlled project directories and review them before using them in workflows or startup locations. <br>


## Reference(s): <br>
- [Fox Cellcog on ClawHub](https://clawhub.ai/qinthqod/fox-cellcog) <br>
- [DeepResearch Bench Leaderboard](https://huggingface.co/spaces/muset-ai/DeepResearch-Bench-Leaderboard) <br>
- [CellCog](https://cellcog.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; generated task results may include downloaded files in requested formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CELLCOG_API_KEY and may create asynchronous cloud tasks that consume CellCog credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
