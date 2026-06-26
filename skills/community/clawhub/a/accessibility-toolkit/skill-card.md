## Description: <br>
Friction-reduction patterns for agents helping humans with disabilities, including voice-first workflows, smart-home templates, and efficiency automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgtreadw](https://clawhub.ai/user/cgtreadw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to design accessibility-focused workflows that reduce repeated interaction, support voice-first operation, and generate smart-home automation patterns for people with physical disabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Smart-home examples include under-scoped safety-sensitive behavior such as automatic door unlocking. <br>
Mitigation: Require explicit opt-in, multi-factor presence checks, alerts, and fail-secure behavior before adapting lock or alarm automations. <br>
Risk: Example messaging can expose sensitive backup access codes. <br>
Mitigation: Use private placeholders or secure storage for access codes and avoid placing secrets in agent-visible status messages. <br>
Risk: Broad voice commands can trigger high-impact actions without enough review. <br>
Mitigation: Keep broad commands away from locks, alarms, purchases, and emergency actions unless narrowed and reviewed before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cgtreadw/accessibility-toolkit) <br>
- [Apple Accessibility](https://www.apple.com/accessibility/) <br>
- [Home Assistant Accessibility](https://www.home-assistant.io/docs/accessibility/) <br>
- [Apple Human Interface Guidelines: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with YAML, checklist, and command-oriented examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes accessibility workflow patterns, Home Assistant automation examples, audit checklists, and communication templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
