## Description: <br>
Provides a pure Python standard-library tool for converting Unix timestamps, formatting date-time values, and getting the current timestamp without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate or explain local timestamp conversion commands for Unix timestamps, formatted date-time strings, and Asia/Shanghai timezone defaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is tagged as requiring sensitive credentials even though the security evidence says no API key is needed. <br>
Mitigation: Do not provide secrets for normal use; verify any credential request against the local script behavior before running it. <br>
Risk: Promotional external links appear in the README-style skill text. <br>
Mitigation: Review external links before following them and treat them as publisher-provided references rather than required runtime dependencies. <br>
Risk: Invalid timezone names can fall back to default local timestamp behavior. <br>
Mitigation: Use valid IANA timezone names such as Asia/Shanghai and verify outputs when timezone precision matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-timestamp-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain text timestamp values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local timestamp conversions; no external services or API keys are required.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
