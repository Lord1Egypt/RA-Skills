## Description: <br>
Generate UUIDs (v1, v4, v7) in bulk using AceToolz. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acetoolz](https://clawhub.ai/user/acetoolz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate one or more UUIDs or GUIDs through the AceToolz service, selecting UUID versions v1, v4, or v7 and a count from 1 to 10. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: UUID generation requests are sent to AceToolz, which may be unsuitable for sensitive or offline workflows. <br>
Mitigation: Use this skill only when outbound requests to AceToolz are acceptable; for sensitive or offline workflows, generate UUIDs locally. <br>
Risk: The skill supports only UUID versions v1, v4, and v7 and limits bulk generation to 1-10 UUIDs per request. <br>
Mitigation: Validate the requested version and count before calling the API, and direct unsupported requests to the full AceToolz tool. <br>


## Reference(s): <br>
- [AceToolz UUID Generator](https://www.acetoolz.com/generate/tools/uuid-generator) <br>
- [AceToolz OpenClaw UUID API](https://www.acetoolz.com/api/openclaw/uuid-generator) <br>
- [ClawHub skill listing](https://clawhub.ai/acetoolz/acetoolz-uuid) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with UUID code blocks and OS-specific shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports UUID versions v1, v4, and v7 with count limited to 1-10; requests are sent to AceToolz.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
