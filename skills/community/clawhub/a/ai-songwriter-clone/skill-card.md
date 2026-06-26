## Description: <br>
Generates new song lyrics and Suno generation requests from a user-provided reference song or artist and a new theme. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-hou-pe](https://clawhub.ai/user/jason-hou-pe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to transform a reference song or artist plus a new theme into structured song lyrics, style tags, and generated Suno audio links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated lyrics and song metadata are sent to a third-party API. <br>
Mitigation: Use the skill only with content appropriate for the external provider and review the provider's terms and data handling before use. <br>
Risk: Automatic generation and polling can create provider billing or approval-checkpoint concerns. <br>
Mitigation: Review the workflow before installation and add an approval checkpoint or cost control where needed. <br>
Risk: The script accepts KIE_API_KEY or SUNO_API_KEY from the environment. <br>
Mitigation: Use a dedicated KIE_API_KEY and avoid leaving unrelated SUNO_API_KEY values in the environment. <br>
Risk: The generator includes a hard-coded example.com callback URL. <br>
Mitigation: Remove or replace the callback URL before running the generator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason-hou-pe/ai-songwriter-clone) <br>
- [Publisher profile](https://clawhub.ai/user/jason-hou-pe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls] <br>
**Output Format:** [Markdown with generated lyrics, style tags, audio links, and inline shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses KIE_API_KEY or SUNO_API_KEY and polls the Kie.ai Suno generation API until audio metadata is returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
