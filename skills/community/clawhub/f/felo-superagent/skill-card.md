## Description: <br>
Felo SuperAgent lets agents run Felo Open Platform SuperAgent conversations with SSE responses, LiveDoc continuity, style-library selection, and optional outputs such as images, documents, PPT, HTML, and X search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to connect an agent session to Felo SuperAgent for multi-turn chat, LiveDoc-backed workspace continuity, and generated assets or research artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, relevant conversation context, selected resource IDs, style data, thread IDs, and LiveDoc IDs may be sent to Felo. <br>
Mitigation: Use a dedicated Felo API key and avoid sending secrets, regulated data, or sensitive internal context. <br>
Risk: Broad reuse of thread and LiveDoc identifiers can mix separate workstreams or carry prior context into later requests. <br>
Mitigation: Start a new LiveDoc for separate or sensitive work and track thread and LiveDoc IDs deliberately. <br>
Risk: FELO_API_BASE overrides can redirect API traffic away from the default Felo endpoint. <br>
Mitigation: Use the default Felo API endpoint unless a trusted override is required, and inspect the environment before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangzhiming1999/felo-superagent) <br>
- [Felo SuperAgent API documentation](https://openapi.felo.ai/docs/api-reference/v2/superagent.html) <br>
- [Felo Open Platform documentation](https://openapi.felo.ai/docs/) <br>
- [Felo API key setup](https://felo.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text or JSON responses, with Markdown links for generated assets and shell commands for setup and usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FELO_API_KEY; may return thread and LiveDoc IDs, LiveDoc URLs, image URLs, generated artifact titles, and X search results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
