## Description: <br>
NL emotion tracking + prompt injection via OpenClaw hook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tashfeenahmed](https://clawhub.ai/user/tashfeenahmed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers using OpenClaw can install this hook to track inferred user and agent emotion state across sessions and inject a compact emotion_state block into agent bootstrap context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inferred emotion history may be stored across sessions and inserted into future prompts. <br>
Mitigation: Review stored emotion-state.json files, establish a deletion process, and use the history and entry limit settings to minimize retained state. <br>
Risk: Conversation text may be sent to OpenAI or a configured classifier. <br>
Mitigation: Use external classifier settings only when approved for the workspace, and avoid enabling the hook for sensitive work without explicit privacy review. <br>
Risk: Emotion state from other agents may be included in the prompt context. <br>
Mitigation: Set EMOTION_MAX_OTHER_AGENTS to 0 when cross-agent emotion sharing is not desired. <br>


## Reference(s): <br>
- [Emotion State release page](https://clawhub.ai/tashfeenahmed/emotion-state) <br>
- [OpenAI API base URL used by optional classifier](https://api.openai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown installation and configuration guidance plus a runtime emotion_state text block.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The hook can persist inferred emotion history and inject recent entries and a decayed trend line into future prompts.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
