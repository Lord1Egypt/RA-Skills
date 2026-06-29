## Description: <br>
Use when judging an early product idea, MVP, AI tool, creator product, or launched demo with Baoqingtian-style demand evidence, verdicts, seven-day validation tasks, and a visual verdict card. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaohuadavidlee](https://clawhub.ai/user/shaohuadavidlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, founders, and product builders use this skill to evaluate early product ideas, MVPs, AI tools, creator products, and launched demos against concrete demand evidence. It produces a structured verdict, validation tasks, a visual HTML verdict card, and a detailed Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include sensitive or proprietary product details supplied in the case. <br>
Mitigation: Review the generated HTML and Markdown before sharing them publicly. <br>
Risk: The bundled renderer creates files in the output directory chosen by the user. <br>
Mitigation: Run the local Python renderer with an intended output path and inspect the created files before distributing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shaohuadavidlee/baoqingtian) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, Shell commands, Guidance] <br>
**Output Format:** [Structured case JSON rendered into an HTML verdict card and a Markdown verdict report, with generated file links returned to the user.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a case JSON matching the documented schema and writes outputs to a selected local directory.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
