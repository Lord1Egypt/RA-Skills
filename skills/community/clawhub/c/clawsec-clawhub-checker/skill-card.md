## Description: <br>
ClawHub reputation checker for clawsec-suite. Adds a standalone reputation gate before guarded skill installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Developers and security operators use this skill to add a ClawHub reputation check before guarded skill installation through clawsec-suite. It helps review scanner metadata, author and release signals, and low-reputation warnings before an install proceeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reputation scores and scanner summaries are heuristic and can produce false positives or false negatives. <br>
Mitigation: Review the target skill code and warning output before using --confirm-reputation, and keep the reputation threshold aligned with local policy. <br>
Risk: Reputation checks query ClawHub metadata during install review. <br>
Mitigation: Use the skill only where ClawHub metadata lookups are acceptable, and review network behavior before deployment. <br>
Risk: Optional advisory-hook wiring is a manual local customization. <br>
Mitigation: Run the setup helper to validate paths and review any hook changes before enabling reputation annotations. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/davida-ps/skills/clawsec-clawhub-checker) <br>
- [ClawSec homepage](https://clawsec.prompt.security/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include exit-code guidance and reputation warnings that require explicit operator confirmation.] <br>

## Skill Version(s): <br>
0.0.8 (source: server release, SKILL.md frontmatter, skill.json, changelog released 2026-06-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
