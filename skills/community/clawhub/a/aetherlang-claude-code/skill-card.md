## Description: <br>
Execute AetherLang V3 AI workflows from Claude Code using nine specialized engines for culinary, business, research, marketing, and strategic analyses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[contrario](https://clawhub.ai/user/contrario) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Claude Code users use this skill to send selected AetherLang flow code and queries to the AetherLang V3 API for structured culinary, business, research, marketing, forecasting, and data analysis results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected queries and AetherLang flow code are sent to an external provider endpoint. <br>
Mitigation: Send only the intended query and flow code, and do not include secrets, credentials, private file contents, or personal information unless that processing is intentional. <br>
Risk: The optional Pro tier AETHER_KEY could be exposed if it is hardcoded or included in prompts or logs. <br>
Mitigation: Keep AETHER_KEY in an environment variable and avoid committing, printing, or embedding it in flow code. <br>
Risk: Generated analysis from external AI workflows may be incomplete, outdated, or incorrect. <br>
Mitigation: Review the returned markdown before relying on it for business, research, culinary, or strategic decisions. <br>


## Reference(s): <br>
- [AetherLang API endpoint](https://api.neurodoc.app/aetherlang/execute) <br>
- [Publisher homepage and privacy policy](https://masterswarm.net) <br>
- [ClawHub skill page](https://clawhub.ai/contrario/aetherlang-claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with bash and Python examples plus JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The primary API result is read from result.final_output and is described by the artifact as Greek markdown.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
