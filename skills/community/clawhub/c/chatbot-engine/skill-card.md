## Description: <br>
Chatbot Engine provides multi-turn dialogue, intent recognition, context management, and knowledge-base retrieval for conversational applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build chatbot workflows that classify user intent, manage multi-turn dialogue state, retrieve knowledge-base answers, and optionally connect to LLM providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency versions are not pinned, which can introduce supply-chain or compatibility drift. <br>
Mitigation: Install from a trusted package index and pin reviewed dependency versions before production deployment. <br>
Risk: Optional OpenAI or Anthropic providers can send prompts and recent conversation context outside the local environment. <br>
Mitigation: Use the mock or local provider for private testing, and enable external providers only after reviewing data-sharing requirements. <br>
Risk: Chat sessions and knowledge-base content may contain sensitive information if saved to shared paths. <br>
Mitigation: Avoid shared storage for sensitive sessions or knowledge bases, and sanitize content before persistence. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/openclaw/chatbot-engine) <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/chatbot-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text responses, Python code snippets, and Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use mock, local, OpenAI, or Anthropic providers; optional context history and knowledge-base content can affect responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
