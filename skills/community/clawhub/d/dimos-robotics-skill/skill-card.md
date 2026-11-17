## Description:

Build, review, and troubleshoot DimOS robotics applications, especially DimOS @skill methods, Module classes, Blueprints, MCP wiring, CLI runs, replay/simulation testing, and safe robot-control scaffolds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yichulau](https://clawhub.ai/user/yichulau)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to create, review, wire, and test DimOS robotics skills, modules, blueprints, MCP tools, and simulation or replay workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Robot-facing movement templates omit finite-number checks, so NaN or infinite numeric inputs could undermine movement limits.

Mitigation: Reject non-finite numeric values before range checks or state updates, and test generated movement skills in replay or simulation before exposing them through MCP or using real hardware.

Risk: Generated robot-control code can affect physical hardware if used outside simulation.

Mitigation: Require local supervision, a clear operating area, an accessible stop mechanism, and confirmed downstream controller safety checks before real-hardware use.

## Reference(s):

- [DimOS Quick Reference](resources/dimos_reference.md)
- [Safety and Testing Notes for DimOS Skills](resources/safety_and_testing.md)
- [ClawHub Skill Page](https://clawhub.ai/yichulau/skills/dimos-robotics-skill)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scaffolded DimOS skill-container files when the bundled helper script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
