## Description: <br>
Runs a private editorial desk that turns daily information into a custom-section, calmly edited, source-linked A4 portrait PDF brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igloomatics](https://clawhub.ai/user/igloomatics) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use this skill to curate daily briefings, organize topics into editorial sections, and produce a polished A4 portrait PDF digest with source links. It is especially suited to recurring personal or team briefs across finance, technology, AI, games, products, and notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring delivery can run at the wrong time, write to the wrong location, or continue unexpectedly if schedule details are underspecified. <br>
Mitigation: Confirm cadence, exact time, timezone, output folder, preview requirement, and how to disable the scheduler before configuring recurring generation. <br>
Risk: A simple one-off summary may be over-formatted into a PDF product when the user only needs lightweight summarization. <br>
Mitigation: Use this skill when the user wants an editorial-style daily PDF brief; otherwise choose a more general summarization workflow. <br>
Risk: Sensitive or controversial source material could be amplified through dramatic wording or unnecessary detail. <br>
Mitigation: Keep the edition factual, calm, high level for sensitive topics, and avoid sensational, graphic, or instructional harmful details. <br>


## Reference(s): <br>
- [Daily Editor Skill Instructions](artifact/SKILL.md) <br>
- [PDF Target](artifact/pdf-target.md) <br>
- [Editorial Reference](artifact/reference.md) <br>
- [Scheduling Reference](artifact/schedule.md) <br>
- [Templates](artifact/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and optional HTML/CSS or shell commands for producing a single-file A4 portrait PDF] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source labels and links, schedule specifications, preview notes, and print-oriented layout guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
