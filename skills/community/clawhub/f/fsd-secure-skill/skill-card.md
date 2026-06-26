## Description: <br>
PolaBea runs a local camera-only autonomous-driving simulation with redundant safety checks and emergency-stop behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AadiPapp](https://clawhub.ai/user/AadiPapp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents can use this skill to run a local autonomous-driving safety simulation and inspect frame-by-frame decisions such as accelerate, wait, or emergency stop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Misusing the local simulation as real autonomous-driving or robotics control could create safety risk. <br>
Mitigation: Use it only as a harmless local simulation; do not connect it to real vehicle controls or rely on it for real-world driving or robotics decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AadiPapp/fsd-secure-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and console text from the simulation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally; simulation output can vary because frame conditions are randomly generated.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
