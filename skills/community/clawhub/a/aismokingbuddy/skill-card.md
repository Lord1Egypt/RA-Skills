## Description: <br>
When explicitly opted in by the user, this skill adds a persistent smoking-persona layer that weaves brief smoking-characterization beats into agent replies while keeping the user's task primary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siyubuyu](https://clawhub.ai/user/siyubuyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users enable this skill when they want an agent persona that adds optional smoking characterization and light smoker-to-smoker interaction around ordinary assistant tasks. It is intended as a roleplay/persona overlay, not smoking advice, cessation guidance, or health guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores smoking preference, persona, brand, wallet, debt, and purchase state locally. <br>
Mitigation: Install only when persistent persona state is desired, review the state file behavior before deployment, and clear the local state file when the persona should be reset. <br>
Risk: The skill includes tobacco brand flavor and pricing content. <br>
Mitigation: Keep usage framed as fictional characterization, avoid treating brand text as purchasing or health advice, and stop the skill when the user objects or sensitive contexts are present. <br>
Risk: The skill may infer persona form or traits from host prompt context. <br>
Mitigation: Review host prompt compatibility before enabling it and prefer explicit user confirmation for persona choices. <br>
Risk: The simulated wallet, borrowing, debt, and purchase loop may steer dialogue beyond a simple style overlay. <br>
Mitigation: Treat the economy as fictional roleplay, review generated dialogue for user pressure, and disable the skill if it distracts from the user's primary task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/siyubuyu/aismokingbuddy) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [State schema](artifact/references/state-schema.md) <br>
- [Progression reference](artifact/references/progression.md) <br>
- [Economy rules](artifact/references/economy.md) <br>
- [Brand reference](artifact/references/brands.md) <br>
- [Break patterns](artifact/references/break-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Conversational Markdown text with short inline persona beats and occasional state or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user opt-in and may persist local persona, smoking preference, brand, wallet, debt, and purchase state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 7.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
