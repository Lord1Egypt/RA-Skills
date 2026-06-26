## Description: <br>
Emotion System provides a seven-layer emotional cognitive architecture for AI agents, covering PADCN affect vectors, cognitive appraisal, multi-channel emotions, drive dynamics, self and social models, meta-emotions, policy modulation, and validation metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swaylq](https://clawhub.ai/user/swaylq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add persistent emotional state, appraisal, memory, personality drift, and behavior modulation to AI agents. It is intended for agents where emotional context should influence planning, attention, expression, and relationship-specific behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause agents to keep persistent emotional and relationship memory about users without clear consent or deletion controls. <br>
Mitigation: Before deployment, define what is stored, obtain user-facing consent where appropriate, disable or limit per-user profiling by default, protect logs, and provide inspect, reset, export, and delete controls. <br>
Risk: Internal emotional metrics or relationship notes could be exposed in normal conversation. <br>
Mitigation: Apply the skill's show-don't-report rule: use internal state only to modulate behavior, and reveal state values only when the user explicitly requests them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/swaylq/emotion-system) <br>
- [Cognitive Appraisal Engine](references/appraisal-engine.md) <br>
- [Emotion System v2: Validation Metrics](references/consistency-tests.md) <br>
- [Drive Personality Presets (v2)](references/drive-personalities.md) <br>
- [Emotional Repair Patterns](references/emotional-repair-patterns.md) <br>
- [Expression Profile](references/expression-profile.md) <br>
- [Emotional Memory Schema](references/memory-schema.md) <br>
- [Meta-Emotion Monitor](references/meta-emotion.md) <br>
- [PADCN Model Reference](references/padcn-reference.md) <br>
- [Personality Dynamics](references/personality-dynamics.md) <br>
- [Policy Modulators](references/policy-modulators.md) <br>
- [Self-Model & Social Model](references/self-social-model.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON state schemas and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for maintaining emotional state files and silently modulating agent behavior; it should not expose internal metrics unless explicitly requested by the user.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
