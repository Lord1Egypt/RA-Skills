## Description: <br>
Cycling Tracker Pro helps users record rides, analyze speed, plan routes, build training plans, and view cycling statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cyclists and fitness users use this skill for ride logging, speed analysis, route planning, training plans, and basic cycling statistics. Agents can use it to provide cycling-tracker guidance and example command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary describes this as a documentation-only skill, so the listed cycling commands may not exist in the user's environment. <br>
Mitigation: Confirm the cycling commands are implemented and tested before relying on them for ride tracking or analysis. <br>
Risk: The artifact metadata declares a curl binary requirement without explaining why network tooling is needed. <br>
Mitigation: Ask the publisher why curl is required and restrict any network use to trusted endpoints before executing related commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaising-openclaw1/cycling-tracker-pro) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only artifact; no executable tracker implementation is included.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
