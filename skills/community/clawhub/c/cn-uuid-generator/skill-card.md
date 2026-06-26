## Description: <br>
Generates UUID v1, UUID v4, UUID v5, and short UUID values locally with Python standard-library tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate single or batch unique identifiers for application code, testing data, configuration, and automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: UUID v1 values can expose timestamp or machine-derived information when used in public or privacy-sensitive identifiers. <br>
Mitigation: Use UUID v4 by default for public, privacy-sensitive, or externally shared identifiers. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text UUID values or JSON arrays of generated UUIDs, with optional Markdown guidance from the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports count, UUID version, namespace/name for UUID v5, and short UUID output options.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
