## Description: <br>
FOC motor-parameter identification assistant for measuring and identifying stator resistance, dq inductance, back-EMF or flux constant, pole pairs, and inertia using practical methods such as step response tests, high-frequency injection, and DC decay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongjie666888](https://clawhub.ai/user/yongjie666888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and motor-control engineers use this skill to plan FOC motor-parameter measurements, process measured data, and generate controller configuration examples for STM32 and Arduino FOC workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill involves electrical measurements and rotating machinery, so incorrect setup or unsafe test conditions can damage equipment or injure users. <br>
Mitigation: Treat the skill as engineering guidance, secure and guard the motor and load, keep clear of rotating parts, use rated instruments, set conservative voltage, current, and speed limits, account for back-EMF and bus overvoltage, and keep an emergency stop available. <br>
Risk: Parameter calculations and generated controller settings can be wrong if measurement data is noisy, incomplete, or collected with incorrect assumptions. <br>
Mitigation: Review results before applying them to hardware, repeat measurements where practical, and validate controller limits conservatively before increasing power or speed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yongjie666888/foc-parameter-identifier) <br>
- [FOC platform examples](references/foc_platform_examples.md) <br>
- [Measurement tips](references/measurement_tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands, formulas, generated reports, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Python-assisted calculations and generated STM32 or Arduino FOC parameter examples.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
