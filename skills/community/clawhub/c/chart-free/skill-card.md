## Description: <br>
chart-free helps agents generate local bar and line chart PNGs from inline labels and values using Python and matplotlib. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to create simple local PNG charts for reports, slides, and decision documents without relying on a cloud charting API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release claims local-only chart generation, but the security evidence flags API-key setup and an external callback parameter. <br>
Mitigation: Review the skill before installation in strict offline environments, avoid callback URLs, and do not provide sensitive chart data unless the publisher clarifies any network behavior. <br>
Risk: The security verdict is suspicious due to inconsistent offline behavior claims. <br>
Mitigation: Treat offline behavior as unverified until the publisher explains why an API key is required for a local matplotlib workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/chart-free) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated chart artifacts are PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for local filesystem storage under the chart workspace output directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
