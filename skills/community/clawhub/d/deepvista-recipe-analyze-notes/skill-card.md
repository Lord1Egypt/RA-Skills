## Description: <br>
Recipe that helps an agent search, retrieve, summarize, and find patterns across notes in a DeepVista knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingconan](https://clawhub.ai/user/jingconan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this recipe to analyze multiple DeepVista notes, identify recurring themes, summarize findings, and optionally save a confirmed synthesis as a new note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve and synthesize sensitive notes from a DeepVista knowledge base. <br>
Mitigation: Install only when the DeepVista CLI and service are trusted, and scope note searches explicitly to the notes needed for the task. <br>
Risk: Broad synthesis can include unintended note content if the selected note set is too large or imprecise. <br>
Mitigation: Review fetched content before broad synthesis when possible. <br>
Risk: The workflow can save an analysis as a new note. <br>
Mitigation: Only create a new analysis note after explicit user confirmation. <br>


## Reference(s): <br>
- [DeepVista CLI homepage](https://cli.deepvista.ai) <br>
- [ClawHub skill page](https://clawhub.ai/jingconan/deepvista-recipe-analyze-notes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks and structured summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose creating a new note only after user confirmation.] <br>

## Skill Version(s): <br>
0.1.0-alpha.21 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
