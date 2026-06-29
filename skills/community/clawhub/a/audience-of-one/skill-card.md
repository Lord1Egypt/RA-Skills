## Description: <br>
Audience Of One helps an agent rewrite or diagnose AI-like writing by restoring three concrete coordinates: speaker, audience, and why the text matters now. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[damomhd](https://clawhub.ai/user/damomhd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, marketers, and product or engineering teams use this skill to make drafts, posts, scripts, reports, technical documents, emails, and similar text feel addressed to a specific reader while preserving facts and technical details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Style rewriting can alter meaning, factual details, technical terms, or responsibility if applied too aggressively. <br>
Mitigation: Review factual details, numbers, dates, names, commands, configuration, interfaces, and technical terminology after rewriting; preserve system or specification voice when appropriate. <br>
Risk: Missing speaker, audience, or purpose may lead to invented context if the source text does not provide enough material. <br>
Mitigation: Use placeholders and ask the author for concrete material when the original does not support a rewrite; do not fabricate experiences, numbers, citations, or provenance. <br>
Risk: The skill can be misused to misrepresent authorship or make synthetic text appear personally written. <br>
Mitigation: Use the skill only on text the user is allowed to edit, and avoid using it to conceal authorship or create misleading personal claims. <br>


## Reference(s): <br>
- [Server-resolved GitHub repository](https://github.com/DamomHd/audience-of-one) <br>
- [ClawHub skill page](https://clawhub.ai/damomhd/audience-of-one) <br>
- [Coordinates Diagnostic](references/coordinates-diagnostic.md) <br>
- [Scenarios](references/scenarios.md) <br>
- [Examples](references/examples.md) <br>
- [Evaluation Samples](references/evals.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with rewritten text, coordinate diagnostics, deletion suggestions, placeholders, or concise review notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for missing source material when the original text lacks enough evidence to fill speaker, audience, or purpose; long texts may receive a suggested deletion list rather than silent compression.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
