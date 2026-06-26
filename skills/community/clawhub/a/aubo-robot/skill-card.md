## Description: <br>
Controls AUBO collaborative robots over RTDE with Python and provides joint motion, Cartesian motion, IO control, and status interfaces for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qujingyang28](https://clawhub.ai/user/qujingyang28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Robotics developers and OpenClaw users can connect to an AUBO robot or ARCS simulator to send motion and IO commands, adjust speed, toggle digital outputs, and inspect robot status through a Python RTDE driver. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Motion and IO commands can affect a real AUBO robot or connected equipment. <br>
Mitigation: Install only for an authorized robot or simulator, test in simulation first, keep a human operator present, verify emergency-stop access, clear the workspace, and use reduced speed. <br>
Risk: The release needs review because current status readings may be placeholders and should not be treated as safety signals. <br>
Mitigation: Verify robot state through the robot controller or simulator before motion, and do not rely on placeholder joint, TCP pose, or mode readings for safety decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qujingyang28/aubo-robot) <br>
- [AUBO official site](https://www.aubo-robotics.cn/) <br>
- [AUBO developer portal](https://developer.aubo-robotics.cn/) <br>
- [AUBO SDK documentation](https://docs.aubo-robotics.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses robot connection settings such as host, port, speed, acceleration, joint positions, TCP poses, and IO states; generated commands may affect physical hardware.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
