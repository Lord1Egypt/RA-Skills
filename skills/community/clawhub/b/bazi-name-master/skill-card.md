## Description: <br>
Helps agents handle BaZi-based Chinese baby naming by calculating or checking four-pillar charts, analyzing favorable elements, and evaluating candidate names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billin9](https://clawhub.ai/user/billin9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to support BaZi-informed Chinese baby naming, including birth-chart calculation, naming-direction analysis, candidate-name generation, and name scoring or ranking against a verified chart. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birth and naming details can be sensitive personal information. <br>
Mitigation: Collect only the details needed for chart verification and naming analysis, and avoid exposing or retaining user-provided birth data outside the current task. <br>
Risk: BaZi-based conclusions may be treated as deterministic or authoritative when they are traditional interpretive guidance. <br>
Mitigation: Present recommendations as cultural naming analysis, preserve uncertainty notes, and require chart verification before scoring or ranking names. <br>
Risk: The supporting script is invoked through local shell commands and the artifact examples include an absolute local path. <br>
Mitigation: Review the helper before execution, adjust the path to the installed artifact location, and run only the disclosed BaZi calculation script. <br>


## Reference(s): <br>
- [Bazi Name Master on ClawHub](https://clawhub.ai/billin9/bazi-name-master) <br>
- [Naming Principles](references/naming-principles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with optional JSON output from the BaZi calculation helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include birth-data checks, four-pillar chart details, favorable-element guidance, candidate-name explanations, fixed-dimension scores, rankings, and uncertainty notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
