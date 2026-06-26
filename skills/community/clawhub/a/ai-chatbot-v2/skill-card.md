## Description: <br>
AI Chatbot Service provides a local customer-service chatbot with FAQ replies, intent recognition, sentiment handling, multi-turn chat, FAQ management, and basic handoff prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windy-001-crypto](https://clawhub.ai/user/windy-001-crypto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External support teams, operators, and developers can use this skill to answer common customer-service questions, classify support intent, detect negative sentiment, manage a lightweight FAQ, and produce scripted responses for commerce or internal helpdesk scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the chatbot's handoff text as a completed real-world complaint escalation. <br>
Mitigation: Use it only where a separate human escalation workflow exists, and make operators confirm that escalation outside the chatbot. <br>
Risk: Recent conversation snippets can appear in statistics output during a shared session. <br>
Mitigation: Avoid entering sensitive customer details and clear conversation history before sharing session output. <br>
Risk: FAQ and policy responses are local canned content and may not match a real organization's current customer-service policies. <br>
Mitigation: Review and replace the bundled FAQ content before deployment in a live support workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/windy-001-crypto/ai-chatbot-v2) <br>
- [Publisher profile](https://clawhub.ai/user/windy-001-crypto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style chatbot responses, command help, FAQ listings, statistics, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are generated locally from in-memory FAQ, intent, sentiment, and conversation-history state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
