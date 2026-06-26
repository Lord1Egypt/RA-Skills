## Description: <br>
Guides agents through ESPHome-specific documentation lookup, YAML/config authoring and review, component selection, troubleshooting, dashboard or node maintenance, and local note caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklouzal](https://clawhub.ai/user/kklouzal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and home automation operators use this skill for ESPHome-specific YAML authoring, configuration review, component selection, troubleshooting, and device maintenance grounded in official ESPHome documentation and local project notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local encyclopedia notes can accidentally capture Wi-Fi passwords, API keys, dashboard private URLs, tokens, or other sensitive operational details. <br>
Mitigation: Keep .ESPHome-Encyclopedia notes inside the intended project and redact or omit credentials, tokens, private URLs, recovery codes, and other secrets. <br>
Risk: ESPHome configuration, pin, package, substitution, framework, or OTA changes can affect device availability or behavior. <br>
Mitigation: Consult the relevant official ESPHome docs, inspect current configuration first, and review proposed config or OTA-impacting changes before applying them to devices. <br>


## Reference(s): <br>
- [ESPHome Components Documentation](https://esphome.io/components/) <br>
- [ESPHome Encyclopedia Workflow Notes](references/workflow.md) <br>
- [ESPHome Topic Map](references/topic-map.md) <br>
- [.ESPHome-Encyclopedia Cache Layout](references/cache-layout.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional YAML/code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace-local .ESPHome-Encyclopedia cache and notes; cache fetches are restricted to official ESPHome docs URLs.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
