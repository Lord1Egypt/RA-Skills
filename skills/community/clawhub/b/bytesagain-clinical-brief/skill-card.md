## Description: <br>
Summarize clinical case notes into specialty briefs. Input: raw case notes or lab results. Output: structured specialty brief, differential diagnosis list, key findings summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians, clinical educators, and healthcare workflow builders can use this skill to draft structured clinical summaries, differential diagnosis lists, lab interpretations, case presentations, and specialty briefs from provided notes or lab values. Its output is a drafting aid for qualified review, not a substitute for clinical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical notes or lab values entered in terminal commands may appear in shell history, logs, screenshots, or terminal transcripts. <br>
Mitigation: Prefer de-identified inputs and use the skill only in environments where terminal history, logs, and transcripts are handled under appropriate privacy controls. <br>
Risk: Generated summaries, differential diagnoses, lab interpretations, or next steps may be incomplete or clinically incorrect. <br>
Mitigation: Treat outputs as draft text for review by qualified healthcare professionals and do not use them as standalone clinical decision support. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Terminal text with structured headings and bullet-style clinical sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local terminal output; users provide notes, symptoms, lab values, patient descriptors, or specialty names as command arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
