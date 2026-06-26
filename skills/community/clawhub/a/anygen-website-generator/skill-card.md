## Description: <br>
Website Generator helps agents create websites and landing pages, including product pages, portfolios, event pages, blogs, signup pages, app download pages, and campaign pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logictortoise](https://clawhub.ai/user/logictortoise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate websites and landing pages through the AnyGen CLI and website workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Website prompts and content may be sent to AnyGen for server-side generation. <br>
Mitigation: Use an approved AnyGen account and avoid sending sensitive or restricted content unless that transfer is authorized. <br>
Risk: The fallback install command auto-confirms installation of an additional workflow skill. <br>
Mitigation: Review and explicitly approve the anygen-workflow-generate skill before allowing fallback installation. <br>
Risk: The skill depends on an AnyGen API key and CLI authentication. <br>
Mitigation: Store the API key in the environment or approved secret storage and avoid exposing it in prompts, logs, or generated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/logictortoise/anygen-website-generator) <br>
- [AnyGen website](https://www.anygen.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated website output through AnyGen] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the AnyGen CLI and ANYGEN_API_KEY; may delegate website generation to the anygen-workflow-generate skill.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
