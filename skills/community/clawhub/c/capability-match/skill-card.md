## Description: <br>
AI-powered skill router that analyzes your request and recommends the best installed skill for the job. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viratkumar123](https://clawhub.ai/user/viratkumar123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to find an installed skill that best matches a natural-language task. It scans local skill descriptions and returns ranked recommendations with confidence scores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the local OpenClaw skills directory to build recommendations. <br>
Mitigation: Install only where reading local installed skill descriptions is acceptable. <br>
Risk: Skill recommendations may be incomplete or mismatched for sensitive or high-impact tasks. <br>
Mitigation: Treat recommendations as guidance and confirm the selected skill before use. <br>


## Reference(s): <br>
- [Capability Match on ClawHub](https://clawhub.ai/viratkumar123/capability-match) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown-like text with ranked recommendations and confidence scores] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw skill metadata; thresholds and maximum results are configurable by environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, _meta.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
