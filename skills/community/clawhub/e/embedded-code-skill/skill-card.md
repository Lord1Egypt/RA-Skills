## Description:

Generate, rewrite, or review embedded C code for microcontrollers, drivers, and firmware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leon-2050](https://clawhub.ai/user/leon-2050)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and firmware engineers use this skill to generate, rewrite, or review embedded C modules, including register definitions, peripheral drivers, coding-standard checks, and platform-specific guidance for MCU and SoC targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly auto-trigger on common code-generation and review language, which may make it active outside intentional embedded C tasks.

Mitigation: Limit activation to explicit embedded C, firmware, driver, or microcontroller requests before installing it in a shared agent environment.

Risk: The rewrite workflow preserves original functional behavior by default, so existing safety or security defects in firmware may be carried forward.

Mitigation: Tell the agent whether to preserve behavior exactly or fix identified safety and security defects, then require human review of rewritten firmware.

Risk: Generated embedded code may affect hardware control, safety functions, or regulated compliance work.

Mitigation: Require domain review, hardware validation, and compliance checks before using generated code in safety-critical, industrial, automotive, aerospace, or military systems.

Risk: Architecture lookup and self-optimization behavior may use external research or alter skill behavior if enabled.

Mitigation: Require explicit approval before web research or self-optimization, and review any resulting guidance or skill changes before use.

Risk: Incorrect or missing peripheral base addresses can produce invalid firmware register access.

Mitigation: Require users to provide authoritative base addresses or chip documentation, and reject or escalate requests that would require fabricating register addresses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leon-2050/skills/embedded-code-skill)
- [English README](artifact/README_EN.md)
- [Primary Skill Definition](artifact/SKILL.md)
- [Coding Standards Reference](artifact/embedded-code-skill-standards/SKILL.md)
- [Architecture Patterns](artifact/embedded-code-skill-arch/SKILL.md)
- [Driver Templates](artifact/embedded-code-skill-drivers/SKILL.md)
- [Industry Domain Requirements](artifact/embedded-code-skill-domains/SKILL.md)

## Skill Output:

**Output Type(s):** [code, markdown, guidance]

**Output Format:** [Markdown with embedded C code blocks and review findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose module-level files such as module_reg.h, module.h, and module.c.]

## Skill Version(s):

0.0.2 (source: server release metadata, created 2026-04-17T14:43:09Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
