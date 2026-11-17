## Description:

Asf V4 gives OpenClaw agents governance checks, ownership proof generation, role-economics scoring, rework-risk prediction, hot-contract analysis, conflict resolution, and guarded optimization outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alshowse-tech](https://clawhub.ai/user/alshowse-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill in OpenClaw workflows to evaluate proposed architecture and contract changes, generate governance evidence, and receive risk or optimization guidance before agent work proceeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Governance and optimization decisions may depend on missing or unpinned core synthesizer code.

Mitigation: Bundle or pin the required core synthesizer implementation before relying on veto, ownership, scoring, risk, or optimizer results.

Risk: Caller-provided rules and unclear policy sources may bypass mandatory controls.

Mitigation: Require an explicit trusted policy source and prevent user-supplied rules from weakening hard vetoes, ownership rules, or security constraints.

Risk: Session logging and live optimization can affect runtime behavior or record operational data without clear user consent.

Mitigation: Make logging and optimizer behavior opt-in, document the effects before activation, and surface rollback or cooldown status in agent outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alshowse-tech/skills/anfsf-v1)
- [Publisher profile](https://clawhub.ai/user/alshowse-tech)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON-like tool and command results, Markdown guidance, TypeScript code snippets, shell commands, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include approval/veto results, ownership validation, scoring metrics, risk factors, conflict recommendations, optimization status, and configuration instructions.]

## Skill Version(s):

1.5.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
