## Description: <br>
Apifox Exporter automates Apifox API export with Playwright and converts exported OpenAPI JSON into organized plain-text interface documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzy05651666](https://clawhub.ai/user/zzy05651666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API teams use this skill to export Apifox project definitions, expand OpenAPI schemas, and generate module-grouped interface documentation for implementation or review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reuses a logged-in Apifox browser session and can export project API definitions. <br>
Mitigation: Use explicit Apifox-specific commands, verify the browser is on the intended team and project, and delete the saved browser profile when it is no longer needed. <br>
Risk: Default team and project values may point automation at the wrong Apifox workspace. <br>
Mitigation: Change the default team and project values before running the skill, or pass explicit team and project parameters for each export. <br>
Risk: Fallback export mode may process the newest JSON file in Downloads rather than the intended Apifox export. <br>
Mitigation: Avoid fallback mode unless the intended export is confirmed as the newest Downloads JSON file. <br>
Risk: Generated source JSON, debug screenshots, and Desktop documentation can contain sensitive API examples or project data. <br>
Mitigation: Review exported content before sharing and delete raw source JSON, debug screenshots, and Desktop exports when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zzy05651666/apifox-exporter) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Plain text API documentation generated from OpenAPI JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a raw source JSON file and a Desktop text export; browser automation may also create a persistent browser profile and debug screenshots.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence, package.json, skill.yaml, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
