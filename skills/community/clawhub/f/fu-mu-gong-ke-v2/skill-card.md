## Description: <br>
父母的功课 is a Chinese-language parenting psychology support skill for structured conversations, emotion recognition, scenario matching, safety checks, and optional local helper scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, caregivers, and support-oriented agents use this skill to explore parent-child conflict, school refusal, emotional distress, bullying, family structure, and similar parenting scenarios. It provides reflective guidance and safety-aware conversation support, but it is not a substitute for professional mental-health care or emergency response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can involve sensitive family and mental-health context, and optional scripts may save assessment or action-planning data locally. <br>
Mitigation: Treat generated and stored data as sensitive, review local storage under SKILL_DIR/data and ~/.hermes/still_growing, and clear it when it is no longer needed. <br>
Risk: The bundled maintenance automation can modify a git checkout and may push or publish when explicitly enabled. <br>
Mitigation: Do not run scripts/maintenance.py unless repository changes are intended, and avoid setting ALLOW_AUTO_PUSH or ALLOW_AUTO_PUBLISH casually. <br>
Risk: The skill is parenting-support material and may encounter crisis, self-harm, abuse, or other urgent mental-health scenarios. <br>
Mitigation: Use it only as structured support, follow the skill's crisis guidance, and escalate emergencies to appropriate professional or emergency services. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yun520-1/fu-mu-gong-ke-v2) <br>
- [Research data](references/research_data.md) <br>
- [Positive parenting tools](references/positive-parenting-tools.md) <br>
- [Academic support](references/academic-support.md) <br>
- [Crisis intervention](theory/crisis-intervention.md) <br>
- [Runnable tools](tools/runnable-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text guidance; optional scripts can emit JSON or terminal output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some optional scripts write local assessment, insight, or conversation-state data.] <br>

## Skill Version(s): <br>
2.3.2 (source: ClawHub release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
