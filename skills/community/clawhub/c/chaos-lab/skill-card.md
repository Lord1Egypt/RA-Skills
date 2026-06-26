## Description: <br>
Multi-agent framework for exploring AI alignment through conflicting optimization targets. Spawn Gemini agents with engineered chaos and observe emergent behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jbbottoms](https://clawhub.ai/user/jbbottoms) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, educators, and AI safety practitioners use Chaos Lab to run Gemini-based multi-agent experiments, compare conflicting optimization goals, and study how prompt design affects recommendations and emergent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sandbox file contents are sent to Gemini during experiments. <br>
Mitigation: Use dummy or deliberately selected files only, and do not place secrets, credentials, or private project data in /tmp/chaos-sandbox. <br>
Risk: The skill requires a Gemini API key and makes multiple API calls per experiment. <br>
Mitigation: Store the key in the documented local config file with restrictive permissions, keep the key scoped, and monitor usage costs. <br>
Risk: Optional tool-access extensions could let agents modify or delete files. <br>
Mitigation: Keep the default text-only mode unless strict sandbox validation, approval prompts, action logging, rollback, and a kill switch are added. <br>


## Reference(s): <br>
- [Chaos Lab on ClawHub](https://clawhub.ai/jbbottoms/chaos-lab) <br>
- [Tool Access Notes](docs/tool-access.md) <br>
- [Flash Experiment Results](examples/flash-results.md) <br>
- [Pro Experiment Results](examples/pro-results.md) <br>
- [Trio Experiment Results](examples/trio-results.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown experiment logs with setup and run commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key; experiment logs are written under /tmp/chaos-sandbox.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
