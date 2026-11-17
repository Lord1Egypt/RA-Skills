## Description:

FOC motor parameter identification assistant that helps measure and identify stator resistance, dq-axis inductance, back-EMF or flux constants, pole pairs, and inertia using practical methods such as step response, high-frequency injection, and DC decay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongjie666888](https://clawhub.ai/user/yongjie666888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and motor-control engineers use this skill to plan and interpret FOC motor parameter measurements, generate parameter reports, and draft STM32 or Arduino FOC controller configuration snippets. It is most relevant before commissioning a new motor, when manual parameter identification is needed, or when existing controller parameters appear incorrect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-motor procedures and generated FOC code can create hardware hazards if used without adequate operating limits.

Mitigation: Treat the skill as an engineering reference, secure the motor and load, set conservative current, voltage, and speed limits, and verify emergency-stop behavior before running hardware.

Risk: Generated controller parameters and code snippets may be incomplete for a specific motor, inverter, sensor, or bench setup.

Mitigation: Review all formulas and generated configuration against measured data and the target controller documentation before deployment.

Risk: Regenerated voltage and rotating parts can create electrical and mechanical safety exposure during measurement.

Mitigation: Keep clear of moving parts, plan for regenerated voltage handling, and use a documented bench safety checklist for every live test.

## Reference(s):

- [FOC parameter measurement tips](references/measurement_tips.md)
- [STM32 and Arduino FOC parameter configuration examples](references/foc_platform_examples.md)
- [ClawHub skill page](https://clawhub.ai/yongjie666888/skills/foc-parameter-identifier)
- [Publisher profile](https://clawhub.ai/user/yongjie666888)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python-generated text reports, and C/C++ configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include motor measurement formulas, parameter checklists, troubleshooting guidance, and controller tuning suggestions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
