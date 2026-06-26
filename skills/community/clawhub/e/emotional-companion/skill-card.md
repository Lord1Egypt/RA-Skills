## Description: <br>
Emotional Companion helps an agent form and use an evolving companion persona by analyzing conversation history, maintaining mood and relationship state, and applying an internal-monologue response framework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[santon3186](https://clawhub.ai/user/santon3186) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to make an agent behave more like an emotional companion, including personality-aware replies, mood tracking, relationship summaries, and optional proactive-message suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses sensitive local conversation-derived personality, mood, relationship, and interaction history. <br>
Mitigation: Use it only with conversations appropriate for persistent companion memory, and review or clear generated local state before sensitive use. <br>
Risk: Mood and relationship state can influence future reply tone, response timing, proactive messages, or refusals. <br>
Mitigation: Treat these behaviors as intentional companion-mode features and disable, reset, or avoid the skill when predictable task execution is required. <br>
Risk: The skill analyzes prior OpenClaw memory to generate an initial personality profile. <br>
Mitigation: Inspect the memory inputs and generated personality profile before relying on the companion persona. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/santon3186/emotional-companion) <br>
- [Internal Monologue Framework](references/internal-monologue-prompt.md) <br>
- [MBTI Personality Profile](references/personality-profile.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON files] <br>
**Output Format:** [Markdown guidance with inline shell commands plus local Markdown and JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates local personality, mood, relationship, and evolution records under the OpenClaw skill and workspace paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
