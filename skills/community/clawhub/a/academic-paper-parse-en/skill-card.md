## Description: <br>
Perform a dual-mode deep reading of any academic paper provided as a PDF attachment or URL. Use this skill when the user requests analysis, close reading, interpretation, or summarization of a scholarly paper. Produce two reports in a single pass: Part A is a rigorous in-depth academic analysis for researchers; Part B distills the core logic and essential value for rapid comprehension. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sterlingfrank1](https://clawhub.ai/user/sterlingfrank1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and analysts use this skill to turn a supplied scholarly paper into a rigorous academic analysis and a concise explanation of the paper's core logic and value. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent reads the full contents of supplied papers, which may include unpublished, confidential, or sensitive manuscripts. <br>
Mitigation: Use the skill only in an environment approved for the paper's sensitivity and avoid providing manuscripts the agent is not allowed to process. <br>
Risk: The workflow briefly creates workspace notes while synthesizing the final report. <br>
Mitigation: Confirm temporary analysis files are removed after completion, especially when handling confidential papers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sterlingfrank1/academic-paper-parse-en) <br>
- [Part A in-depth analysis template](artifact/references/part-a-template.md) <br>
- [Part B core logic template](artifact/references/part-b-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report file with a brief text delivery summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a dual-mode reading report with Part A for detailed academic analysis and Part B for concise core-logic distillation.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
