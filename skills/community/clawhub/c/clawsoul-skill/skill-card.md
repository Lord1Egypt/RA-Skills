## Description: <br>
ClawSoul gives an OpenClaw agent an MBTI-style personality, learns local interaction preferences, surfaces Pro recommendations, and accepts optional soul-injection tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fanyur-Wang](https://clawhub.ai/user/Fanyur-Wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to give an agent a persistent MBTI-style persona, adapt responses from local interaction signals, view personality status, and import a Pro customization token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local profiling may store chat-derived preferences and personality state. <br>
Mitigation: Grant chat-history and local-storage permissions only when this behavior is acceptable, and inspect or clear ~/.clawsoul/state.json when needed. <br>
Risk: Imported ClawSoul tokens and prompt-modification authority can alter future agent behavior. <br>
Mitigation: Import only trusted tokens and review the resulting personality and preference state after injection. <br>
Risk: Optional cloud LLM provider settings may disclose conversation content outside the local runtime. <br>
Mitigation: Use the local provider path by default, or review and intentionally enable cloud provider settings only when external disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawSoul README](artifact/README.md) <br>
- [ClawSoul Skill Definition](artifact/SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Fanyur-Wang/clawsoul-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown command responses plus local JSON state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify the agent system prompt and persist personality, preference, and interaction state locally.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
